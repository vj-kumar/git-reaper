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
import yaml
import tempfile
import shutil
import subprocess
from argparse import ArgumentParser
from contextlib import contextmanager

class GitReaper(object):
    def __init__(self):
        return

    def parseConfigFile(self, configfile):
        with open(os.path.abspath(configfile)) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    @contextmanager
    def directoryAs(self, path):
        oldpwd=os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(oldpwd)

    def sync(self, configfile, project):
        ymlconfig = ""
        tempdir = tempfile.mkdtemp(prefix=('gitreaper-'+ project + '-'))
        ymlconfig = self.parseConfigFile(configfile)
        with self.directoryAs(tempdir):
            cmd = 'git clone --mirror ' + ymlconfig[project]['upstream'] + ' .'
            subprocess.call(cmd, shell=True)
            cmd = 'git push -f -u ' + ymlconfig[project]['url']
            subprocess.call(cmd + " --all", shell=True)
            subprocess.call(cmd + " --tags", shell=True)
        shutil.rmtree(tempdir)

    def sendPatchUpstream(self, configfile, project):
        return

def main():
    reaper = GitReaper()
    parser = ArgumentParser()
    parser.add_argument('-c', "--config", dest='config_file',
                                help="Master configuration file",
                                action='store',
                                required=True)
    parser.add_argument('-p', "--project", dest='project',
                                help="Project to work on",
                                action='store',
                                required=True)
    parser.add_argument("--sync",
                                help="Sync fork with upstream",
                                action='store_true',
                                required=False)
    args = parser.parse_args()
    if args.sync:
        reaper.sync(args.config_file, args.project)

if __name__ == "__main__":
    main()
