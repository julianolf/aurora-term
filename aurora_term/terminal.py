import cmd

from aurora_term import __version__


class Terminal(cmd.Cmd):
    intro = f'aurora-term ({__version__})\nType "help" or "?" for help.\n'
    prompt = '=# '

    def do_quit(self, arg):
        """Quit aurora-term."""
        return True
