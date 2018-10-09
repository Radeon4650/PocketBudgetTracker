#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import subprocess
import sys


modules_dir = os.path.dirname(__file__)
req_file_name = 'requirements.txt'


class Installer(object):
    python_path = os.path.dirname(sys.executable)
    pip_path = os.path.join(python_path, 'pip')

    def __init__(self, upgrade=False):
        print('Python location prefix is {}'.format(self.python_path))
        self.upgrade = upgrade

    def _pip_install(self, install_args=[]):
        args = [self.pip_path, 'install']
        args += install_args

        if self.upgrade:
            args.append('--upgrade')

        if subprocess.call(args):
            print("ERROR: installing of [{}] failed".format(' '.join(args)))

    def install(self, name):
        print("Installing [%s]" % name)
        self._pip_install([name])

    def install_modules_deps(self):
        print('Search for submodules into {} dir'.format(modules_dir))

        modules = next(os.walk(modules_dir))[1]
        print('Found modules {}'.format(modules))

        for module in modules:
            dep_file = os.path.join(modules_dir, module, req_file_name)
            if os.path.isfile(dep_file):
                self._pip_install(['--requirement', dep_file])
            else:
                print('Module does not have {} file'.format(req_file_name))


if __name__ == '__main__':

    installer = Installer(True)

    # Upgrade pip
    installer.install('pip')

    # Install all modules dependencies
    installer.install_modules_deps()

    sys.exit(0)
