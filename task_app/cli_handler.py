import argparse

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs='?')
    parser.add_argument("--id", type=int)
    parser.add_argument("--title")
    parser.add_argument("--content")
    parser.add_argument("--status")
    parser.add_argument("--commands",
                        help='show list of commands',
                        action='store_true')
    parser.add_argument("--usages",
                        help='examples of use',
                        action='store_true')

    return parser.parse_args()