import cmd

from aurora_term import __version__, aurora, config


class Terminal(cmd.Cmd):
    intro = f'aurora-term ({__version__})\nType "help" or "?" for help.\n'

    def __init__(self, conf=config.Config()):
        super().__init__()
        self.config = conf
        self.prompt = f'{self.config.database}=# '
        self.aurora = aurora.Aurora(
            profile=self.config.profile,
            cluster_arn=self.config.cluster,
            secret_arn=self.config.secret,
            database=self.config.database,
        )

    def default(self, line):
        try:
            result = self.aurora.execute(line)
        except Exception as error:
            print(str(error))
        else:
            print(result)

    def do_quit(self, arg):
        """Quit aurora-term."""
        return True
