# Template script for building processing
#
# This python file is copied to local if it does not exist
# 
# Generally, we want to perform the following steps
#
# 1) Read the default input file
# 2) Run a script or scripts against that file, storing the result
# 3) Open eQuest to see the result
# 4) Restore the original file
# 5) Update the scripts and repeat
#
# Accordingly, this file acts as a wrapper to the series of scripts
# to be executed. It has safety measures built in to prevent lost data.
# Leave all of the content below, and populate the list of scripts to be
# performed.

import time
import os
import shutil

BACKUP_DIR = 'backup_process'

SCRIPTS = [

    ] 

def make_backup(fn):

    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)

    dst = BACKUP_DIR + os.sep + fn + time.strftime('_%y%m%d-%H%M%S.inp')
    shutil.copy(fn, dst)

    return dst    

def main():

    if not SCRIPTS:
        print 
        print '    Configure p.py'
        print 
        i = raw_input('  >>')
        os.system('p.py')
        return

    input_file = os.getcwd().split(os.sep)[-1] + '.inp'
    backup = make_backup(input_file)
    
    for script in SCRIPTS:
        os.system('python ' + script)
    
    if raw_input('Open eQuest - enter "save" to retain changes') == 'save':
        if not raw_input('You sure?') == 'y':
            pass
        else:
            shutil.copy(backup, input_file)
    else:
        shutil.copy(backup, input_file)

if __name__ == '__main__':
    main()