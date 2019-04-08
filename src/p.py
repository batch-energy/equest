# Template script for building processing
#
# This python file is copied to local if it does not exist
#
# Generally, we want to perform the following steps
#
# 1) Read the default input file
# 2) Run process.py against that file, storing the result
# 3) Open eQuest to see the result
# 4) Restore the original file
# 5) Update the scripts and repeat
#
# Accordingly, this file acts as a wrapper to process.py to be exexuted
# It has safety measures built in to prevent lost data. Leave all of the
# content below, and adjust process.py

import time
import os
import shutil
import utils

BACKUP_DIR = 'backup_process'

def make_backup(fn):

    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)

    dst = BACKUP_DIR + os.sep + fn + time.strftime('_%y%m%d-%H%M%S.inp')
    shutil.copy(fn, dst)

    return dst

def main():

    if not os.path.exists('process.py'):
        print
        print '  First run, configuring...'
        print
        print '    Which client?'
        print
        client = utils.choices(['dmi', 'tnz', 'smma', 'none'])
        print
        print '    copying seed file to local dir'
        shutil.copy(utils.client_seed_file(client), os.getcwd())
        print
        print '    copying template process.py to local dir'
        process_py_path = os.path.dirname(utils.__file__) + os.sep + 'process.py'
        shutil.copy(process_py_path, os.getcwd())
        print

        print '  All set. Will open process.py'
        print
        raw_input('  >>')

        os.system('process.py')

        return

    input_file = utils.input_file_name()

    need_backup = os.path.exists(input_file)
    if need_backup:
        backup = make_backup(input_file)

    os.system('python process.py')

    try:
        raw_input('Open eQuest - press enter to continue')
    finally:
        if need_backup:
            shutil.copy(backup, input_file)

if __name__ == '__main__':
    main()