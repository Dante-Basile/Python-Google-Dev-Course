#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess
import collections

"""Copy Special exercise
"""

def get_special_paths(directory):
    """Return the absolute paths to all files in the dir matching the pattern
    """
    fileNames = os.listdir(directory)
    #print fileNames #TESTING
    specialPaths = []
    for thisName in fileNames:
        if re.search(r"__\w+__", thisName):
            specialPaths.append(os.path.abspath(os.path.join(directory, thisName)))
    #print specialPaths #TESTING
    return specialPaths

def checkDupFileNames(absPaths):
    """Take list of all matched absolute file paths, check if files name same
    """
    fileList = []
    for thisPath in absPaths:
        fileList.append(os.path.basename(thisPath))
    fileCounter = collections.Counter()
    for thisFile in fileList:
        fileCounter[thisFile] += 1
    if sum(fileCounter.values()) > len(fileCounter.values()):
        return 1
    else:
        return 0


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  if tozip and todir:
    print("ERROR: these tags cannot be used together")
    sys.exit(2)
  absPaths = []
  for thisArg in args[:]:
    absPaths += get_special_paths(thisArg)
  if checkDupFileNames(absPaths):
    print("ERROR: contains duplicate files")
  elif todir:
    if not(os.path.exists(todir)):
      os.makedirs(todir)
    for thisPath in absPaths:
      shutil.copy(thisPath, todir)
  elif tozip:
    print("Command I'm going to do:" + " ".join(["zip", "-j", tozip] + absPaths))
    subprocess.check_call(["zip", "-j", tozip] + absPaths)
  else:
    for thisPath in absPaths:
      print(thisPath)
    
  
if __name__ == "__main__":
  main()
