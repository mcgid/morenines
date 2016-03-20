import argparse
import os

import morenines.create
import morenines.verify
import morenines.remote
import morenines.push

def main():
    args = parse_arguments()

    if args.command == 'create':
        morenines.create.create(args.root_path)
    elif args.command == 'verify':
        morenines.verify.verify(args.root_path, args.index_path)
    elif args.command == 'push':
        remotes = [morenines.remote.FakeRemote(None)]
        morenines.push.push(args.root_path, args.index_path, remotes)


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', choices=['create', 'verify', 'push'])

    parser.add_argument('--index', dest='index_path')

    parser.add_argument('root_path', nargs='?', default=os.getcwd())

    return parser.parse_args()

if __name__ == '__main__':
    main()

