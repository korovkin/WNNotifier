#!/usr/bin/python

import json
import parcon
import operator
import pprint
import os
import sys
import getopt
import re
import optparse
import md5
import hashlib

import version

###
def sign_data(data_to_sign):
  m = hashlib.md5()
  m.update(data_to_sign)
  signature = m.hexdigest()
  return signature

####
def source_file_signature(filename, version_number = version.VERSION):
  FILENAME = os.path.splitext(os.path.split(filename)[1])[0] + ".py"
  DIRECTORY = os.path.split(filename)[0]
  s = sign_data(open(os.path.join(DIRECTORY,FILENAME)).read())
  return "%s:%s:%s" % (FILENAME, hex(version_number), s)

#### tool version:
VERSION_STR = source_file_signature(__file__)

#### initial signature toke that i have to use
SIGNATURE_TOKEN = '<<SignedSource::*O*zOeWoEQle#+L!plEphiEmie@IsG>>'

#### a signature header (prefixed to the signed file):
header_template = """// @generated %s
// signed with: https://github.com/korovkin/WNNotifier/notifier/sign.py
"""

#####
def sign(options, data):
  """
    sign the given, yield a signature that can be verified by phabricator and lint
    Replaces the followin string in the input file:
      // @generated <<SignedSource::*O*zOeWoEQle#+L!plEphiEmie@IsG>>
    With:
      // @generated SignedSource<<md5 of the whole file including the previous line>>
  """
  data_to_sign = (header_template % SIGNATURE_TOKEN) + data
  signature = sign_data(data_to_sign)
  signature = "SignedSource<<%s>>" % signature
  signed_data = (header_template % signature) + data
  return (signed_data, data_to_sign)

#####
def write_data_to_sign(options, data_to_sign, filename):
  if options.store_signed_data:
    open(filename + ".to.sign", "w").write(data_to_sign)

#####
def main():
  parser = optparse.OptionParser(usage="\n python %prog <options> <source file1>...\n   or \n python %prog <options> < file.in > file.out")

  parser.add_option("", "--version",
                    action="store_true",
                    help="print version number",
                    dest="version",
                    default=False)
  parser.add_option("", "--store_signed_data",
                    action="store_true",
                    help="store ",
                    dest="store_signed_data",
                    default=False)
  (options, filenames) = parser.parse_args()

  if options.version:
    print(VERSION_STR)
    sys.exit(0)

  if filenames == []:
    sys.stderr.write(os.path.split(__file__)[1] + " warning: reading input from stdin...\n")
    data = sys.stdin.read()
    signed_data, data_to_sign = sign(options, data)
    print signed_data,
    write_data_to_sign(options, data_to_sign, "data_to_sign.to.sign")
  else:
    for filename in filenames:
      data = open(filename, "r").read()
      signed_data, data_to_sign = sign(options, data)
      open(filename, "w").write(signed_data)
      print "signed, ", filename
      write_data_to_sign(options, data_to_sign, filename + ".to.sign")

#####
if __name__ == "__main__":
  main()

