import argparse
from podcaster.commands import script, record

def main():
    parser = argparse.ArgumentParser()
    cmd_parser = parser.add_subparsers(dest='command')

    script_subparser = cmd_parser.add_parser('script')
    script_subparser.add_argument('filename', help='The filename to process', nargs='?')
    script_subparser.add_argument('--duet', action='store_true', help='Use duet')

    script_subparser = cmd_parser.add_parser('record')
    script_subparser.add_argument('filename', help='The filename to process', nargs='?')
    script_subparser.add_argument('--duet', action='store_true', help='Use duet')

    args = parser.parse_args()
    if args.command == 'script':
        script(args.filename, args.duet)
    elif args.command == 'record':
        record(args.filename, args.duet)

