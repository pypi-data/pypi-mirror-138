import argparse
from kAuto.create import create


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="version", action="store_true")
    parser.add_argument("-i", "--init", help="init", action="store_true")
    args = parser.parse_args()
    if args.version:
        print("1.0")
    if args.init:
        create()


if __name__ == "__main__":
    main()
