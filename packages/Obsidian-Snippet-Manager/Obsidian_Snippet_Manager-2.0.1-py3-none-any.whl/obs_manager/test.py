import argparse

class _HelpAction(argparse._HelpAction):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()

        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)]
        # there will probably only be one subparser_action,
        # but better save than sorry
        for subparsers_action in subparsers_actions:
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                print("{}".format(choice))
                print(subparser.format_help())

        parser.exit()


# create the parser for the "command_1" command
parser = argparse.ArgumentParser(
    description="Git pull and copy the css files in .obsidian/snippet",
    add_help=False
    )
parser.add_argument('--help', action=_HelpAction, help='show this help message and exit')
subparser = parser.add_subparsers(dest='cmd')
parser_clone = subparser.add_parser(
    'clone', help="Clone a repository and add the snippet to Obsidian"
    )
parser_clone.add_argument(
    "repository",
    help="Clone a new repository",
    action="store",
    )
parser_clone.add_argument(
    "--excluded",
    "--e",
    "--no",
    help='Exclude this repository from update',
    action='store_true'
    )
parser_update = subparser.add_parser('update', help='Update a specific CSS snippet.')
parser_update.add_argument(
    "repository_name",
    help="The repo you want to update",
    action="store",
    )
parser_config = subparser.add_parser('config', help='Edit the configuration file')

parser_list = subparser.add_parser('list', help='List all Github Repository you cloned.')
parser_exclude = subparser.add_parser("exclude", help='Exclude repository from update')
parser_exclude.add_argument(
    "exclude", help="Exclude repository from update", action="store", nargs="+"
    )
args = parser.parse_args()

print(args.cmd, args.exclude)