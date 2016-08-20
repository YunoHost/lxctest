import argparse

from .lxctest import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='YAML file with configuration')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    main(args.filename, args.debug)
