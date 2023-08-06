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

from git import Repo
from git.exc import InvalidGitRepositoryError
from datetime import datetime
from shutil import copy

WORK_FOLDER = 'work'
RESULTS_FOLDER = 'changes'
RESULT_FOLTER_STRFTIME = '%Y-%m-%d_%H%M%S.%f'
LAST_LINK = 'last_changes'
README_FILENAME = 'README.md'
README_CONTENTS = '# README\n\nThis is the repository "%%s".\n\nYou may look at the run results in the folder "%s"' \
                  ' or directly in "%s" to see the changed files after the latest run.\n\nFolder "%s" is the work ' \
                  'folder and no manual changes should be made here.' % (RESULTS_FOLDER, LAST_LINK, WORK_FOLDER)


class DeltaResultRepoInterface(object):
    def __init__(self, repo, work_directory_getter, current_result_directory_getter):
        self._repo = repo
        self.get_work_directory = work_directory_getter
        self.get_current_result_directory = current_result_directory_getter

    @staticmethod
    def _get_filename(filename, base_directory):
        new_filename = os.path.abspath(os.path.join(base_directory, filename))

        if os.path.commonpath([base_directory, new_filename]) != base_directory:
            raise AssertionError('Path traversal detected, aborting.')

        return new_filename

    def get_filename_in_work_directory(self, filename):
        return DeltaResultRepoInterface._get_filename(filename, self.get_work_directory())

    def get_filename_in_result_directory(self, filename):
        return DeltaResultRepoInterface._get_filename(filename, self.get_current_result_directory())


class DeltaResultRepo(object):
    def __init__(self, main_directory, title):
        self._main_directory = main_directory
        self._work_directory = os.path.join(main_directory, WORK_FOLDER)
        self._results_directory = os.path.join(main_directory, RESULTS_FOLDER)
        self._last_link = os.path.join(main_directory, LAST_LINK)
        self._title = title
        self._current_result_directory_name = None

    @property
    def _current_result_directory(self):
        return os.path.join(self._results_directory, self._current_result_directory_name)

    def _has_structure(self):
        result = os.path.exists(self._main_directory)

        if result:
            result = os.path.exists(self._work_directory) and os.path.exists(self._results_directory)

            if result:
                try:
                    Repo(self._work_directory)
                except InvalidGitRepositoryError:
                    result = False

        return result

    def _create_structure(self):
        print('[ ] Creating new repository directory "%s"...' % self._main_directory)

        if not os.path.exists(self._main_directory):
            os.mkdir(self._main_directory)

        os.mkdir(self._work_directory)
        os.mkdir(self._results_directory)

        print('[ ] Creating work repository')
        Repo.init(self._work_directory)

        print('[ ] Creating README.md')
        with open(os.path.join(self._main_directory, README_FILENAME), 'w') as readme:
            readme.write(README_CONTENTS % self._title)

    def _create_result_directory(self):
        if self._current_result_directory_name is not None:
            raise AssertionError('You may enter this class only once.')

        now = datetime.now()
        directory_name = now.strftime(RESULT_FOLTER_STRFTIME)

        self._current_result_directory_name = directory_name
        os.mkdir(self._current_result_directory)

        print('[I] Created result directory "%s"' % self._current_result_directory)

    def _link_result_directory(self):
        if os.path.islink(self._last_link):
            os.remove(self._last_link)

        os.symlink(self._current_result_directory, self._last_link, target_is_directory=True)

    def __enter__(self):
        if not self._has_structure():
            self._create_structure()

        self._create_result_directory()

        return DeltaResultRepoInterface(self, lambda: self._work_directory, lambda: self._current_result_directory)

    def _process_changed_path(self, path):
        directory, filename = os.path.split(path)

        if len(directory) == 0:
            copy(os.path.join(self._work_directory, path), os.path.join(self._current_result_directory))
        else:
            target_dir = os.path.join(self._current_result_directory, directory)
            os.makedirs(target_dir, exist_ok=True)

            copy(os.path.join(self._work_directory, path), target_dir)

        print('[ ] Copied changed file "%s" to result directory' % path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        repo = Repo(self._work_directory)

        if repo.is_dirty():
            for diff in repo.index.diff(None):
                diff_path = diff.b_path

                if not diff.deleted_file:
                    self._process_changed_path(diff_path)

                repo.index.add(diff_path)

        for untracked in repo.untracked_files:
            self._process_changed_path(untracked)

            repo.index.add(untracked)

        repo.index.commit('Execution %s' % self._current_result_directory_name)

        self._link_result_directory()
