#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def secondWordKey(endWords):
    """Returns second word to be used as key for custom sort by second words
    """
    thisMatch = re.search(r"-\w+-(\w+).jpg", endWords)
    secondWord = thisMatch.group(1)
    #print secondWord #TESTING
    return secondWord

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  inLog = open(filename, 'rU')
  logText = inLog.read()
  urlList = re.findall(r"GET (\S*puzzle\S*) HTTP", logText)
  for index in xrange(len(urlList)):
      urlList[index] = "http://code.google.com/" + urlList[index]
  url2Freq = {}
  for thisURL in urlList:
      if thisURL in url2Freq:
          url2Freq[thisURL] += 1
      else:
          url2Freq[thisURL] = 1
  urlFiltered = url2Freq.keys()
  secondWordList = re.findall(r"/\w*?-\w+-\w+.jpg", " ".join(urlFiltered))
  #print("Second word present: " + str(len(secondWordList) == len(urlFiltered))) #TESTING
  if len(secondWordList) == len(urlFiltered):
      orderedURLList = sorted(urlFiltered, key = secondWordKey)
  else:
      orderedURLList = sorted(urlFiltered)
  #print orderedURLList #TESTING
  return orderedURLList
  
def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  imgIndex = 0
  if not(os.path.exists(dest_dir)):
      os.makedirs(dest_dir)
  for thisURL in img_urls:
      #print thisURL #TESTING
      outFile = dest_dir + "/img" + str(imgIndex)
      print("Retrieving: img" + str(imgIndex))
      urllib.urlretrieve(thisURL, outFile)
      imgIndex += 1
  indexFOut = open(dest_dir + "/index.html", 'w')
  indexFOut.write("<verbatim>\n<html>\n<body>\n")
  for thisIndex in xrange(imgIndex): #already +1 from last loop before
      indexFOut.write('<img src="' + os.path.abspath(dest_dir + "/img" + str(thisIndex)) + '">')
  indexFOut.write("\n</body>\n</html>\n")
  indexFOut.close()
  
def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
