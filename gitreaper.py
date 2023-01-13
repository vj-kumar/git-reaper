#!/usr/bin/env python3
#
# SPDX-License-Identifier: MIT
#
# Copyright 2020, Vijai Kumar K
#
# Author:
#  Vijai Kumar K <vijaikumar.kanagarajan@gmail.com>
#
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
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def confirm_user(question):
    reply = input(question).strip()
    if reply == "YES":
        return True
    else:
        return False


def get_temp_dir(project):
    return tempfile.mkdtemp(prefix=("gitreaper-" + project + "-"))


def clean_temp_dir(tempdir):
    shutil.rmtree(tempdir)


def sync_entire_repo(project, upstream, downstream):
    tempdir = get_temp_dir(project)
    with directoryAs(tempdir):
        cmd = "git clone --mirror " + upstream + " ."
        subprocess.call(cmd, shell=True)
        cmd = "git push -f -u " + downstream
        subprocess.call(cmd + " --all", shell=True)
        subprocess.call(cmd + " --tags", shell=True)
    clean_temp_dir(tempdir)


def sync_specific_branches(
    project, upstream, downstream, branches, force=False
):
    tempdir = get_temp_dir(project)
    with directoryAs(tempdir):
        cmd = "git clone " + upstream + " ."
        subprocess.call(cmd, shell=True)
        for branch in branches:
            cmd = "git checkout " + branch
            subprocess.call(cmd, shell=True)
            cmd = "git push -u " + downstream + " " + branch
            if force:
                cmd = cmd + " -f"
            subprocess.call(cmd, shell=True)
    clean_temp_dir(tempdir)


class GitReaper(object):
    def __init__(self):
        return

    def parseConfigFile(self, configfile):
        with open(os.path.abspath(configfile)) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def _repo_sync(self, project, ymlconfig, reverse):
        upstream_repo = ymlconfig[project]["upstream"]
        downstream_repo = ymlconfig[project]["url"]
        flags = ymlconfig[project].get("flags") or ""
        force = False
        if "force" in flags:
            force = True

        if reverse:
            if "reverse" not in flags:
                print(
                    "set 'flags: [reverse]' " +
                    "for {} to sync from downstream to upstream".format(
                        project
                    )
                )
                sys.exit(1)
            upstream_repo = ymlconfig[project]["url"]
            downstream_repo = ymlconfig[project]["upstream"]
            message = "CAUTION: REVERSE PUSH DETECTED"
            print("=" * len(message))
            print("\033[91m{}\033[00m".format(message))
            print("=" * len(message))
            question = upstream_repo + "==>" + downstream_repo + " YES/NO: "
            try:
                if not confirm_user(question):
                    sys.exit("sync aborted")
            except KeyboardInterrupt:
                sys.exit("\nsync aborted")

        if "branches" in ymlconfig[project]:
            question = (
                upstream_repo
                + " ==> "
                + downstream_repo
                + str(ymlconfig[project]["branches"])
                + " YES/NO: "
            )
            question = "\033[91mBRANCH SYNC:\033[00m{}".format(question)
            try:
                if not confirm_user(question):
                    sys.exit("sync aborted")
            except KeyboardInterrupt:
                sys.exit("\nsync aborted")
            sync_specific_branches(
                project,
                upstream_repo,
                downstream_repo,
                ymlconfig[project]["branches"],
                force
            )
        else:
            question = (
                upstream_repo
                + " ==> "
                + downstream_repo
                + " YES/NO: "
            )
            question = "\033[91mBRANCH SYNC:\033[00m{}".format(question)
            try:
                if not confirm_user(question):
                    sys.exit("sync aborted")
            except KeyboardInterrupt:
                sys.exit("\nsync aborted")
            sync_entire_repo(project, upstream_repo, downstream_repo)

    def sync(self, configfile, project, reverse):
        ymlconfig = ""
        ymlconfig = self.parseConfigFile(configfile)
        if project is None:
            for project_entry in ymlconfig:
                self._repo_sync(project_entry, ymlconfig, reverse)
        else:
            self._repo_sync(project, ymlconfig, reverse)

    def sendPatchUpstream(self, configfile, project):
        return


def main():
    reaper = GitReaper()
    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        help="Master configuration file",
        action="store",
        required=True,
    )
    parser.add_argument(
        "--sync",
        help="Sync fork with upstream",
        action="store_true",
        required=True,
    )
    parser.add_argument(
        "-R",
        "--reverse",
        help="""Reverse sync direction.
                Sync downstream to upstream.
                It requires reverse to be set in flags field.
                """,
        action="store_true",
        required=False,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-p",
        "--project",
        dest="project",
        help="Project to work on",
        action="store",
    )
    group.add_argument(
        "-a",
        "--all",
        help="Sync all projects",
        action="store_true",
    )
    args = parser.parse_args()
    if args.sync:
        reaper.sync(args.config_file, args.project, args.reverse)


if __name__ == "__main__":
    main()
