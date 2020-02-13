#!/usr/bin/env python3
# Author: Vijai Kumar K <vijaikumar.kanagarajan@gmail.com>
# Dt: 13 Feb 2020
#        ...
#       |0 0|
#        \_/
#
#    GIT REAPER BOT

import os
import sys
from argparse import ArgumentParser

class GitReaper(object):
    def __init__(self, argv):
        self.config_file = ""
        self.project = ""
        self.__setupArgParser()
        self.__parserArgs(argv)

    def __setupArgParser(self):
        self.__parser = ArgumentParser()
        self.__parser.add_argument('-c', "--config", dest='config_file',
                                    help="Master configuration file",
                                    action='store',
                                    required=True)
        self.__parser.add_argument('-p', "--project", dest='project',
                                    help="Project to work on",
                                    action='store',
                                    required=True)
        self.__parser.add_argument("--sync",
                                    help="Sync fork with upstream",
                                    action='store_true',
                                    required=False)

    def __parserArgs(self, argv):
        argv = self.__parser.parse_args()
        self.config_file = argv.config_file
        self.project = argv.project
        self.command =argv.sync

    def execute(self):
        print(self.config_file)
        print(self.project)
        print(self.command)

def main(argv):
    reaper = GitReaper(argv)
    reaper.execute()

if __name__ == "__main__":
    main(sys.argv)
