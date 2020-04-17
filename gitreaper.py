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

@contextmanager
def directoryAs(path):
    oldpwd=os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def get_temp_dir(project):
        return tempfile.mkdtemp(prefix=('gitreaper-'+ project + '-'))


def clean_temp_dir(tempdir):
        shutil.rmtree(tempdir)


def sync_entire_repo(project, upstream, downstream):
    tempdir=get_temp_dir(project)
    with directoryAs(tempdir):
        cmd = 'git clone --mirror ' + upstream + ' .'
        subprocess.call(cmd, shell=True)
        cmd = 'git push -f -u ' + downstream
        subprocess.call(cmd + " --all", shell=True)
        subprocess.call(cmd + " --tags", shell=True)
    clean_temp_dir(tempdir)


def sync_specific_branches(project, upstream, downstream, branches):
    tempdir=get_temp_dir(project)
    with directoryAs(tempdir):
        cmd = 'git clone ' + upstream + ' .'
        subprocess.call(cmd, shell=True)
        for branch in branches:
            cmd = 'git checkout ' + branch
            subprocess.call(cmd, shell=True)
            cmd = 'git push -f -u ' + downstream + ' ' + branch
            subprocess.call(cmd, shell=True)
    clean_temp_dir(tempdir)


class GitReaper(object):
    def __init__(self):
        return

    def parseConfigFile(self, configfile):
        with open(os.path.abspath(configfile)) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def sync(self, configfile, project):
        ymlconfig = ""
        ymlconfig = self.parseConfigFile(configfile)
        upstream_repo = ymlconfig[project]['upstream']
        downstream_repo = ymlconfig[project]['url']

        if "branches" in ymlconfig[project]:
            sync_specific_branches(project, upstream_repo, downstream_repo,
                                   ymlconfig[project]['branches'])
        else:
            sync_entire_repo(project, upstream_repo, downstream_repo)

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
