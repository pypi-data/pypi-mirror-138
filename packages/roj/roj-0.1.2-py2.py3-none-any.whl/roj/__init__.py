"""roj (run on jail) runs a command on a local or remote jail.

If no command is given, by default it runs a login shell.
"""

from __future__ import annotations
import argparse
import logging
import os
import shlex
import subprocess
import sys
from typing import Optional

__version__ = "0.1.2"

logger = logging.getLogger(__name__)


class FatalError(RuntimeError):
    """Fatal error, which causes program to exit with the given message."""


class RunOnJail:
    __argparser: Optional[argparse.ArgumentParser] = None
    __args: Optional[argparse.Namespace] = None
    logger = logger.getChild('RunOnJail')

    def __init__(self, *poargs, **kwargs):
        super().__init__(*poargs, **kwargs)
        self.__logger = self.logger.getChild(str(id(self)))

    def main(self):
        try:
            if self.args.debug:
                logging.getLogger().setLevel(logging.DEBUG)
            if self.args.jail is None:
                self.__logger.debug("listing jails")
                jails = list(self.list_jails())
                names = {name for jid, name in jails}
                for jid, name in jails:
                    if not self.args.full and name.startswith('ioc-'):
                        abbrev_name = name[4:]
                        if abbrev_name not in names:
                            name = abbrev_name
                    print(f"{jid} {name}")
                return 0
            self.__logger.debug("looking for jail %s", self.args.jail)
            jid, name = self.find_jail()
            self.__logger.debug("found jail %s (%s)", jid, name)
            ssh_tty = self.args.tty
            if self.args.command:
                command = ['jexec', '-U', self.args.user, jid]
                command.extend(self.args.command)
                if ssh_tty is None:
                    ssh_tty = False
            else:
                command = ['jexec', '-U', 'root', jid,
                           'login', '-f', self.args.user]
                if ssh_tty is None:
                    ssh_tty = True
            command = self.wrap_argv(command, ssh_tty=ssh_tty)
            self.__logger.debug("running: %r", command)
            os.execvp(command[0], command)
        except FatalError as e:
            print(f"{self.argparser.prog}: {e}", file=sys.stderr)
            try:
                return e.args[1]
            except IndexError:
                return 1

    def list_jails(self):
        with self.popen(['jls', 'jid', 'name'],
                        stdout=subprocess.PIPE) as popen:
            for line in popen.stdout:
                jid, name = line.decode().rstrip('\n').split(' ', 1)
                yield jid, name

    def find_jail(self):
        jids = {name: jid for jid, name in self.list_jails()}
        self.__logger.debug("jids=%r", jids)
        names = [self.args.jail]
        if not self.args.full:
            names.append('ioc-' + self.args.jail)
        for name in names:
            try:
                return jids[name], name
            except KeyError:
                pass
        raise FatalError(f"jail {self.args.jail} not found")

    def popen(self, args, *poargs, **kwargs):
        argv = self.wrap_argv(args)
        self.__logger.debug("running: %r", argv)
        return subprocess.Popen(argv, *poargs, **kwargs)

    def wrap_argv(self, argv, ssh_tty=False):
        if not self.args.host:
            return argv
        else:
            tty_flag = '-t' if ssh_tty else '-T'
            return ['ssh', tty_flag, self.args.host,
                    ' '.join(shlex.quote(arg) for arg in argv)]

    @property
    def args(self):
        if self.__args is None:
            self.__args = self.argparser.parse_args()
        return self.__args

    @property
    def argparser(self):
        if self.__argparser is None:
            parser = argparse.ArgumentParser()
            parser.add_argument('--host', '-H', metavar='<HOST>',
                                help="""jail host; passed to OpenSSH ssh(1) so
                                        ssh_config(5) aliases also work.
                                        Empty string denotes local jails (no
                                        SSH).  Defaults to the value of
                                        $ROJ_HOST environment variable.""")
            user = parser.add_mutually_exclusive_group()
            user.add_argument('--user', '-u', metavar='<USER>',
                              help="""username (in jail) or uid to run as""")
            tty = parser.add_mutually_exclusive_group()
            tty.add_argument('--tty', '-t',
                             action='store_const', dest='tty', const=True,
                             help="""allocate TTY when running remotely""")
            tty.add_argument('--no-tty', '-T',
                             action='store_const', dest='tty', const=False,
                             help="""do not allocate TTY when running
                                     remotely""")
            parser.add_argument('--debug', action='store_true',
                                help="""enable debug logging""")
            parser.add_argument('--full', '-F',
                                action='store_const', const=True,
                                help="""expect/list full jail names with
                                        "ioc-" prefix intact""")
            parser.add_argument('jail', metavar='<JAIL>', nargs='?',
                                help="""the jail name; the "ioc-" prefix can
                                        be omitted for iocage compatibility,
                                        unless --full/-F is given""")
            parser.add_argument('command', metavar='<ARG>', nargs='*',
                                help="""command and its arguments to run in
                                        the jail; if not specified, login -f
                                        <USER> is assumed, to get a login
                                        shell""")
            parser.set_defaults(user='root',
                                host=os.environ.get('ROJ_HOST'),
                                full=False)
            self.__argparser = parser
        return self.__argparser


def main():
    return RunOnJail().main()


if __name__ == '__main__':
    logging.basicConfig()
    sys.exit(main() or 0)
