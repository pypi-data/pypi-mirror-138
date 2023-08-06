#!/usr/bin/env python3
#
# Copyright (c) Andrea Micheloni 2022
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import subprocess
import argparse
from shutil import which
from . import DeltaResultRepo


def main():
    parser = argparse.ArgumentParser(prog='deltaresult',
                                     description='Tracks changes for multiple script runs with similar results')
    parser.add_argument('-e', '--exec', help='the command to execute', required=True)
    parser.add_argument('-a', '--arg', help='argument to the command to execute (can be repeated)', action='append')
    parser.add_argument('-d', '--dir', help='main directory', required=True)
    parser.add_argument('-t', '--title', help='the program title (for the README.md)', required=False,
                        default='deltaresult repository')

    args = parser.parse_args()

    resolved_executable = which(args.exec)

    if resolved_executable is None:
        parser.error('[E] The command "%s" does not exist or is not executable.' % args.exec)
    else:
        resolved_executable = os.path.abspath(resolved_executable)

        with DeltaResultRepo(os.path.abspath(args.dir), args.title) as repo:
            if args.arg is not None and len(args.arg) > 0:
                execution = [resolved_executable] + args.arg
            else:
                execution = resolved_executable

            print('[ ] Executing "%s"...' % execution)

            process = subprocess.Popen(execution, cwd=repo.get_work_directory())
            result = process.wait()

            print('[I] The command exited with error code %s' % result)

            return result
