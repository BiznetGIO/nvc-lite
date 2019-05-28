"""
Usage:
  nvc <command> [<args>...]

Options:
  -h, --help                             display this help and exit
  -v, --version                          Print version information and quit

Commands:
  playbook                               Playbook Command
  variabel                               Variabel Command
  rm                                     Remove Command

Run 'nvc COMMAND --help' for more information on a command.
"""

from inspect import getmembers, isclass
from docopt import docopt, DocoptExit
from nvc import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import nvc.clis
    options = docopt(__doc__, version=VERSION, options_first=True)
    command_name = ""
    args = ""
    command_class = ""

    command_name = options.pop('<command>')
    args = options.pop('<args>')

    if args is None:
        args = {}

    try:
        module = getattr(nvc.clis, command_name)
        nvc.clis = getmembers(module, isclass)
        command_class = [command[1] for command in nvc.clis if command[0] != 'Base'][0]
    except AttributeError as e:
        print(e)
        raise DocoptExit()

    command = command_class(options, args)
    command.execute()


if __name__ == '__main__':
    main()