#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import logging

from os import getcwd
from sys import exit
from colorama import init

from entropeer import EntropyDigger, VERSION

# This tool will search a file or set of files for high entropy strings
# trufflehog/entro.py were heavily plundered in the making of this tool.

# TODO:
#  - parse binary file
#  - add option so choose the Block Size
#  - implement exclude extension for directroy scan

logging.basicConfig(level=logging.WARN, format='[%(levelname)s]: %(message)s')
init(autoreset=True)

def main():
    parser = argparse.ArgumentParser(prog="entropeer", description='Search files for strings with high shannon entropy.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--filename', type=str, metavar="FILE", help='File to search.')
    group.add_argument('-d', '--directory', type=str, default=getcwd(), help='Search all files in directory.')
    parser.add_argument('-r', '--recurse', action="store_true", help='Search directories recursively starting in the current directory. Use with -d')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-E', "--entropy", action="store_true", default=False, help="Enable entropy checks")
    mode.add_argument('-X', "--regex", action="store_true", default=True, help="Enable high signal regex checks")
    parser.add_argument("--rules", dest="rules", default=None, help="Load external rules from json list file")
    parser.add_argument('-M', "--match-only", dest="match", action="store_true", default=False, help="Print only the matching string")
    parser.add_argument('-v', '--verbose', action="store_true", help='Verbose output')
    parser.add_argument('-t', '--threads', type=int, default=0, help='Number of threads/processes to start')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s v' + VERSION)
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger('').setLevel(logging.INFO)

    if args.rules is not None:
        args.entropy = False
        args.regex = True

    conf = {
        'verbose': args.verbose,
        'threads': args.threads,
        'rulefile': args.rules,
        'match': args.match
    }

    try:
        EntropyDigger(args.filename, args.directory, args.recurse, args.entropy, conf=conf)
    except KeyboardInterrupt:
        logging.info('Exiting')
        pass
    except Exception as e:
        print(e)
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
