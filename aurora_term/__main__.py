"""Amazon Aurora Serverless interactive terminal.

Usage:
    aurora-term [--profile=<p>] [--cluster=<c>] [--secret=<s>] [DATABASE]
    aurora-term (-h | --help)
    aurora-term --version

Arguments:
    DATABASE        Database name.

Options:
    --profile=<p>   Use a specific profile from your credential file.
    --cluster=<c>   RDS cluster ARN.
    --secret=<s>    RDS secret manager ARN.
    -h --help       Show this screen.
    --version       Show version.
"""
import docopt

from aurora_term import __version__, config, terminal

args = docopt.docopt(__doc__, version=__version__)
prms = {k.lower().replace('--', ''): v for k, v in args.items() if v}
conf = config.Config(**prms)
terminal.Terminal().cmdloop()
