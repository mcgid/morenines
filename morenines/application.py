import argparse
import os

import morenines.create
import morenines.verify

def main():
    args = parse_arguments()

    if args.command == 'create':
        morenines.create.create(args.root_path)
    elif args.command == 'verify':
        morenines.verify.verify(args.root_path, args.index_path)

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', choices=['create', 'verify'])

    parser.add_argument('--index', dest='index_path')

    parser.add_argument('root_path', nargs='?', default=os.getcwd())

    return parser.parse_args()

if __name__ == '__main__':
    main()

