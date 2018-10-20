#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright © 2018 PocketBudgetTracker. All rights reserverd.
Author: Approximator (alex@nls.la)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import logging
import argparse
import subprocess

logger = logging.getLogger('dev_script')
logging.basicConfig(
    format='%(asctime)s.%(msecs)-3d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level='INFO')

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(THIS_DIR)


def run_command(cmd):
    logger.info("Runing: {}".format(cmd))
    process = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, cwd=REPO_DIR)
    for line in iter(process.stdout.readline, b''):
        logger.info(line.decode().strip('\n'))
    process.wait()
    ret = process.returncode
    if ret != 0:
        raise Exception('Command returned non-zero exit status: {}'.format(ret))
    return ret


def get_file_list_in(dir_name, extension='.py'):
    files_found = []
    for dir_path, _, files in os.walk(dir_name):
        for filename in files:
            if extension is None or filename.endswith(extension):
                files_found.append(os.path.join(dir_path, filename))
    return files_found


def run(args):
    if args.what_to_run == 'yapf':
        logger.info('Running yapf...')
        run_command("yapf --version")
        files_to_format = get_file_list_in(os.path.join(REPO_DIR, args.directory))
        files_to_format.extend(get_file_list_in(os.path.join(REPO_DIR, 'tools')))
        for src_file in files_to_format:
            logger.info("Formatting file {}".format(src_file))
            run_command("yapf --style='{{based_on_style: google, column_limit: 120}}' -i {}".format(src_file))

    elif args.what_to_run == 'lint':
        logger.info('Running pylint...')
        run_command("pylint --version")
        run_command("pylint --rcfile={} {}".format(os.path.join(REPO_DIR, '.pylintrc'), args.directory))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', required=False, default='INFO', help='Log level')
    subparsers = parser.add_subparsers()

    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('what_to_run', choices=['lint', 'yapf'])
    parser_run.add_argument('--directory', required=False, default=os.path.join(REPO_DIR, 'sources'))
    # parser_run.set_defaults(func=run)

    args = parser.parse_args()
    run(args)
    return 0


if __name__ == '__main__':
    exit(main())
