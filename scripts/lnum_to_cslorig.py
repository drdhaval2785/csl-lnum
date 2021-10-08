# This Python file uses the following encoding: utf-8
"""
Usage:
python lnum_to_cslorig.py dictId lnum
python lnum_to_cslorig.py skd 15140
"""
from __future__ import print_function
import re
import codecs
import sys
import os
import difflib
import shutil


if __name__ == "__main__":
    dictId = sys.argv[1]
    lnum = sys.argv[2]
    inputfile = os.path.join('..', 'v02', dictId, lnum + '.txt')
    fin = codecs.open(inputfile, 'r', 'utf-8')
    changedentry = fin.read()
    fin.close()
    tempfile = os.path.join('temp.txt')
    tfout = codecs.open(tempfile, 'w', 'utf-8')
    cslfile = os.path.join('..', '..', 'csl-orig', 'v02', dictId, dictId + '.txt')
    cslfin = codecs.open(cslfile, 'r', 'utf-8')
    pre = ''
    post = ''
    entry = ''
    entryStart = False
    entryEnd = False
    for lin in cslfin:
		# Decide whether the text is before, during or after entry.
        if lin.startswith('<L>' + lnum + '<'):
            entryStart = True
        elif entryStart and lin.startswith('<L>'):
            entryEnd = True
        # Append to pre, entry or post depending thereon.
        if not entryStart and not entryEnd:
            pre += lin
        if entryStart and not entryEnd:
            entry += lin
        if entryEnd:
            post += lin
    originallines = entry.splitlines(keepends=True)
    changedlines = changedentry.splitlines(keepends=True)
    if originallines == changedlines:
        print("No diff. Nothing to do. Exiting.")
        exit(0)
    else:
        d = difflib.unified_diff(originallines, changedlines)
        sys.stdout.writelines(d)
        print()
        print()
        userinput = input('Above changes would be made. Do you want to continue? y/n : ')
        if userinput in ['y', 'Y']:
            tempfile = os.path.join('temp.txt')
            tfout = codecs.open(tempfile, 'w', 'utf-8')
            tfout.write(pre + changedentry + post)
            tfout.close()
            shutil.copy(tempfile, cslfile)
            os.remove(tempfile)
            print('Changes incorporated in csl-orig repository.')
