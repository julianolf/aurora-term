import cmd
import enum
import json

from aurora_term import __version__, aurora, config


class Format(enum.Enum):
    DEFAULT = enum.auto()
    TABLE = enum.auto()
    JSON = enum.auto()


class Terminal(cmd.Cmd):
    _format = Format.DEFAULT
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

    def _format_default(self, data):
        if not data:
            return ''

        output = ['']

        for record in data:
            for key, value in record.items():
                output.append(f'{key}: {value}')
            output.append('')

        return '\n'.join(output)

    def _format_table(self, data):
        if not data:
            return ''

        header = list(data[0].keys())
        sizes = {h: len(h) for h in header}
        rows = []

        for record in data:
            row = []
            for key, value in record.items():
                sizes[key] = max(sizes[key], len(str(value)))
                row.append(value)
            rows.append(row)

        fmt = ' | '.join(['{:^' + str(s) + '}' for _, s in sizes.items()])
        div = '-+-'.join(['-' * s for _, s in sizes.items()])
        output = [fmt.format(*header), div] + [fmt.format(*r) for r in rows]
        return '\n'.join(output)

    def _format_json(self, data):
        return json.dumps(data, indent=2)

    def _format_output(self, data):
        if self._format == Format.TABLE:
            return self._format_table(data)

        if self._format == Format.JSON:
            return self._format_json(data)

        return self._format_default(data)

    def default(self, line):
        try:
            result = self.aurora.execute(line)
        except Exception as error:
            print(str(error))
        else:
            print(self._format_output(result))

    def do_format(self, arg):
        """Set output format. (formats: default, table, json)"""
        try:
            self._format = Format[arg.upper()]
        except KeyError:
            print(f'"{arg}" is not a valid format.')

    def do_quit(self, arg):
        """Quit aurora-term."""
        return True
