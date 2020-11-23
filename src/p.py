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
# Accordingly, this file acts as a wrapper to process.py

import os
import sys
import shutil
import utils
import subprocess

def main():

    if not os.path.exists('process.py'):
        print '\n  First run, configuring...'
        print '\n    Which client?'
        print
        client = utils.choices(['dmi', 'tnz', 'smma', 'none'])
        print '\n    copying seed file to local dir'
        shutil.copy(utils.client_seed_file(client), os.getcwd())
        print '\n    copying template process.py to local dir'
        process_py_path = os.path.dirname(utils.__file__) + os.sep + 'process.py'
        shutil.copy(process_py_path, os.getcwd())
        print '\n  All set. Will open process.py'
        print
        raw_input('  >>')
        subprocess.Popen('"C:\Program Files\Just Great Software\EditPad Pro 8\EditPadPro8.exe" process.py')
    else:
        backup = 'backup.inp'
        input_file = utils.input_file_name()
        if os.path.exists(input_file):
            shutil.copy(input_file, backup)
        cmd ='python process.py ' + ' '.join(sys.argv[1:])
        os.system(cmd)
        try:
            raw_input('Open eQuest - press enter to continue')
        finally:
            if os.path.exists(BACKUP):
                shutil.copy(backup, input_file)

if __name__ == '__main__':
    main()