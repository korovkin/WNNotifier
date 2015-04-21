#!/usr/bin/python

import json
import time
import parcon
import operator
import pprint
import os
import sys
import getopt
import re
import optparse

import sign
import version

###########################################################################
###########################################################################
## logging:
SEP = "=" * 120
COLOR_PURPLE  = '\033[95m'
COLOR_BLUE    = '\033[94m'
COLOR_GREEN   = '\033[92m'
COLOR_RED     = '\033[91m'
COLOR_RESET   = '\033[0m'

def pretty_json(x):
  return json.dumps(x, indent=2, sort_keys=True)

def pretty_pprint(x):
  return pprint.pformat(x)

def pretty_filename():
  return os.path.split(__file__)[1]

def ASSERT(condition):
  if not condition:
    raise AssertionError

S = time.time()
log_info_enabled = False
log_enabled = False

###
def log(s):
  global S
  t = time.time()
  print "OBJC_TEST: %.4lf, PRNT, " % (t - S), s

###
def log(s):
  global S
  t = time.time()
  print "%.4lf, PRNT, " % (t - S), s

###
def log_info(s):
  global S
  global log_info_enabled
  if not log_info_enabled: return
  t = time.time()
  print "." * 120
  print "%.4lf, INFO, " % (t - S), s

#### tool version:
VERSION = version.VERSION
VERSION_STR = sign.source_file_signature(__file__, VERSION)

###########################################################################
###########################################################################
KEY_ID = "_id"
KEY_OBJECTS = "objects"
###########################################################################
###########################################################################

NO_NAME = "_no_name_"
A_NUMBER = parcon.Word(parcon.digit_chars)
W = parcon.Word(parcon.alpha_chars + "._+~ ")
INT = parcon.SignificantLiteral("int")
LONG = parcon.SignificantLiteral("long")
SHORT = parcon.SignificantLiteral("short")
CHAR = parcon.SignificantLiteral("char")
UNSIGNED = parcon.SignificantLiteral("unsigned")
UNSIGNED_INT = (UNSIGNED + INT)[lambda x: " ".join(x)]
UNSIGNED_LONG = (UNSIGNED + LONG)[lambda x: " ".join(x)]
UNSIGNED_SHORT = (UNSIGNED + SHORT)[lambda x: " ".join(x)]
UNSIGNED_CHAR = (UNSIGNED + CHAR)[lambda x: " ".join(x)]
UNSIGNED_LONG_LONG = (UNSIGNED + LONG + LONG)[lambda x: " ".join(x)]
LONG_LONG = (LONG + LONG)[lambda x: " ".join(x)]
FLOAT = parcon.SignificantLiteral("float")
DOUBLE = parcon.SignificantLiteral("double")
VOID = parcon.SignificantLiteral("void")

#########################################################################
# WNAME - a literal
#########################################################################
WNAME = (UNSIGNED_LONG_LONG
          | LONG_LONG
          | UNSIGNED_CHAR
          | UNSIGNED_INT
          | UNSIGNED_LONG
          | UNSIGNED_SHORT
          | FLOAT
          | DOUBLE
          | INT
          | LONG
          | CHAR
          | SHORT
          | VOID
          | parcon.Word(parcon.alpha_chars + parcon.digit_chars + "_"))

WNAME_SEP_BY_COMMA = (WNAME + parcon.ZeroOrMore("," + WNAME))[lambda x: [x[0]] + x[1]]
UNTIL_NEW_LINE = (parcon.Exact(parcon.OneOrMore(parcon.CharNotIn('\n'))
                              + '\n'))[parcon.concat]
UNTIL_SEMICOLON = parcon.Exact(parcon.OneOrMore(parcon.CharNotIn(';')) + ';')[parcon.concat]
WANY = parcon.Word(parcon.alphanum_chars + "_/!@#$%^&*()_+=-")
STAR = parcon.SignificantLiteral("*")
AMPERSAND = parcon.SignificantLiteral("&")

#########################################################################
# a type, for example 'NSString*' / unsigned int / int
#########################################################################

def TYPE_toDict(x):
  name = x[0]
  ptr_operators = x[1]
  d = dict()
  d[KEY_ID] = "type"
  d["name"] = x[0]
  d["ptr_operators"] = x[1]
  return d

TYPE = (WNAME+parcon.ZeroOrMore(STAR | AMPERSAND))[lambda x: TYPE_toDict(x)]

#########################################################################
#########################################################################

SLASH = "/"
SLASHSLASH = "//"
NEWLINE = "\n"
WHITESPACE = parcon.Word(parcon.whitespace)
QUOTE = parcon.Word("\"")
PATH = (W | (SLASH + W)) + parcon.ZeroOrMore(SLASH + W)
POUND = parcon.Literal("#")
OPEN = "("
CLOSE = ")"
SEMICOLON = parcon.Word(";") + parcon.ZeroOrMore(parcon.Word(";"))
COLON = ":"
MINUS = parcon.Word("-")
PLUS = parcon.Word("+")
STRING_BETWEEN_ROUND_BRACKETS = parcon.Exact(OPEN + parcon.OneOrMore(parcon.CharNotIn(')')) + CLOSE)[parcon.concat]

def INCLUDE_toDict(x):
  d = dict()
  d[KEY_ID] = x[0]
  d["path"] = [x[2]] + x[3]
  d["name"] = os.path.sep.join(d["path"])
  return d

INCLUDE_LIT = (parcon.SignificantLiteral("include")|parcon.SignificantLiteral("import"))
INCLUDE_PATH = ((parcon.SignificantLiteral("<")
                  + PATH
                 + parcon.SignificantLiteral(">"))
                 | (QUOTE
                    + PATH
                    + QUOTE))

INCLUDE = (POUND + INCLUDE_LIT + INCLUDE_PATH)[lambda x: INCLUDE_toDict(x)]

def METHOD_KEYWORD_toDict(x):
  t = None
  arg_name = None
  if len(x)>0 and len(x[1])>0 and len(x[1][0])>0:
    t = x[1][0][0]
    arg_name = x[1][0][1]
  d = dict()
  d[KEY_ID] = "mkeyword"
  d["keyword"] = x[0]
  d["type"] = t
  d["arg"] = arg_name
  return d

def METHOD_KEYWORDS_toDict(x):
  l = [x[0]]
  for a in x[1]:
    l.append(a)
  return l

def METHOD_DECLARE_toDict(x):
  d = dict()
  d[KEY_ID] = "method_declare"
  d["decoration"] = x[0]
  d["mprefix"] = x[1]
  d["mreturn_type"] = x[2]
  d["mkeywords"] = x[3]
  return d

def METHOD_PREFIX_toDict(x):
  d = dict()
  d[KEY_ID] = "mprefix"
  d["prefix"] = x[0]
  return d

METHOD_RETURN_TYPE = (OPEN + TYPE + CLOSE)
METHOD_KEYWORD = (WNAME + parcon.ZeroOrMore(COLON + OPEN + TYPE + CLOSE + WNAME))[lambda x: METHOD_KEYWORD_toDict(x)]
METHOD_KEYWORDS = (METHOD_KEYWORD + parcon.ZeroOrMore(METHOD_KEYWORD))[lambda x: METHOD_KEYWORDS_toDict(x)]
METHOD_PREFIX = (PLUS | MINUS)[lambda x: METHOD_PREFIX_toDict(x)]
METHOD_ACCESS = parcon.ZeroOrMore(parcon.SignificantLiteral("@required") | parcon.SignificantLiteral("@optional"))
METHOD_DECLARE = (METHOD_ACCESS + METHOD_PREFIX + METHOD_RETURN_TYPE + METHOD_KEYWORDS + SEMICOLON)[lambda x: METHOD_DECLARE_toDict(x)]

def COMMENT_LINE_toString(x):
  d = dict()
  d[KEY_ID] = "comment_line"
  d["_text"] = x
  return d

COMMENT_LINE = (parcon.Literal(SLASHSLASH) + UNTIL_NEW_LINE)[lambda x: COMMENT_LINE_toString(x)]

def COMMENT_MULTI_LINE_toString(x):
  d = dict()
  d[KEY_ID] = "comment_multi_line"
  d["_text"] = "".join(x)
  return d

COMMENT_MULTI_LINE = (parcon.SignificantLiteral("/*")
                        + parcon.Exact(parcon.ZeroOrMore(parcon.Except(parcon.AnyChar(),parcon.Literal("*/"))))
                        + parcon.SignificantLiteral("*/"))[lambda x: COMMENT_MULTI_LINE_toString(x)]

COMMENT_MULTI_LINE = ((parcon.Literal("/*")|parcon.Literal("/**"))
                        + parcon.Exact(parcon.ZeroOrMore(parcon.Except(parcon.AnyChar(), parcon.Literal("*/"))))
                        + parcon.Literal("*/"))[lambda x: COMMENT_MULTI_LINE_toString(x)]
COMMENTS = (COMMENT_MULTI_LINE | COMMENT_LINE)

#########################################################################
#########################################################################

def WNNotifierGenerate_toDict(x):
  print "haimg: " + str(x)
  d = {}
  d[KEY_ID] = x[0]
  d["string"] = x[1]
  d["json"] = json.loads(x[1])
  return d


WNNotifierGenerate = ( parcon.SignificantLiteral("WNNotifierGenerate")
                         + STRING_BETWEEN_ROUND_BRACKETS
                         + SEMICOLON)[lambda x: WNNotifierGenerate_toDict(x)]

def protocol_methods_update_decorations(prot_object):
  """ fill in @required / @optional decorations for each method in prot_object """
  methods = prot_object["methods"]
  dec_state = "@required"
  for m in methods:
    if m.has_key("decoration") and len(m["decoration"]) > 0:
      dec_state = m["decoration"]
    m["decoration"] = dec_state

def type_reconstruct(type_object):
  ptr_operators = ""
  if len(type_object["ptr_operators"]) > 0:
    ptr_operators = " " + "".join(type_object["ptr_operators"])
  return "%s%s" % (
    type_object["name"],
    ptr_operators
   )

def protocol_method_recostruct(method, override_arg_for_keywords = {}):
  mkeywords = method["mkeywords"]
  mreturn_type = method["mreturn_type"]
  mprefix = method["mprefix"]
  mdeclaration = "%s (%s)" % (
      mprefix["prefix"],
      type_reconstruct(mreturn_type)
    )
  minvocation = ""
  mselector = ""
  space_between_keyword = ""
  for keyword in mkeywords:
    keyword_name = keyword["keyword"]
    keyword_arg = keyword["arg"]

    # space between keywords:
    mdeclaration += space_between_keyword
    minvocation += space_between_keyword
    mselector += ""
    # append a keyword:
    mdeclaration += "%s" % (keyword_name)
    minvocation += "%s" % (keyword_name)
    mselector += "%s" % (keyword_name)
    # append an argument in case it exists:
    if keyword_arg:
      mdeclaration += ":(%s)%s" % (
        type_reconstruct(keyword["type"]),
        keyword_arg)

      if override_arg_for_keywords.has_key(keyword_name):
        keyword_arg = override_arg_for_keywords[keyword_name]

      minvocation += ":%s" % (
        keyword_arg)
      mselector += ":"
    else:
      pass
    # next iteration, start from a space
    space_between_keyword = " "
  return (mdeclaration, minvocation, mselector)

def PROTOCOL_toDict(x):
  d = dict()
  d["name"] = x[1]
  d[KEY_ID] = "protocol"
  d["methods"] = []
  d["super"] = NO_NAME
  d["WNNotifierGenerate"] = x[3]
  if x[2] == NO_NAME:
    d[KEY_ID] = "protocol_forward_declare"
    return d
  if (len(x[2]) > 0):
    d["super"] = x[2][0]
  d["methods"] = filter(lambda x : x[KEY_ID] == "method_declare", x[4])
  return d

PROTOCOL = (parcon.SignificantLiteral("@protocol") + WNAME
              + parcon.Optional(parcon.Repeat(("<" + WNAME + ">"),0,1)
                         + parcon.Optional(WNNotifierGenerate, "")
                         + parcon.ZeroOrMore(METHOD_DECLARE | COMMENTS)
                         + parcon.SignificantLiteral("@end"), NO_NAME)
              + parcon.Optional(SEMICOLON))[lambda x: PROTOCOL_toDict(x)]

#########################################################################
#########################################################################

def AT_CLASS_DECLARE_toDict(x):
  d = dict()
  d[KEY_ID] = "@class"
  d["names"] = x[1]
  return d

AT_CLASS_DECLARE = (parcon.SignificantLiteral("@class")
            + WNAME_SEP_BY_COMMA
            + parcon.Optional(SEMICOLON))[lambda x: AT_CLASS_DECLARE_toDict(x)]

#########################################################################
#########################################################################

def PROPERTY_toDict(x):
  d = dict()
  d[KEY_ID] = "prop_declare"
  d["properties"] = x[1]
  d["type"] = x[2]
  d["name"] = x[3]
  return d

PROPERTY = (parcon.SignificantLiteral("@property")
                                  + OPEN
                                  + WNAME_SEP_BY_COMMA
                                  + CLOSE
                                  + TYPE + WNAME + parcon.SignificantLiteral(";"))[lambda x: PROPERTY_toDict(x)]

#########################################################################
#########################################################################

def FUNCTION_ARGUMENT_toDict(x):
  d = dict()
  d[KEY_ID] = "farg"
  d["arg_type"] = x[0]
  d["name"] = x[1]
  return d

def FUNCTION_ARGUMENTS_toDict(x):
  arguments = [x[0]]
  arguments.extend(x[1])
  return arguments

def FUNCTION_toDict(x):
  d = dict()
  d[KEY_ID] = "fdeclaration"
  d["freturn_type"] = x[2]
  d["name"] = x[3]
  arguments = []
  d["farguments"] = x[4]
  return d

FUNCTION_ARGUMENT = (TYPE + parcon.Optional(WNAME, NO_NAME))[lambda x: FUNCTION_ARGUMENT_toDict(x)]
FUNCTION_ARGUMENTS = (( FUNCTION_ARGUMENT
                          + parcon.ZeroOrMore("," + FUNCTION_ARGUMENT)
                          ))[lambda x: FUNCTION_ARGUMENTS_toDict(x)]

FUNCTION_DECLARATION = (parcon.Optional(parcon.SignificantLiteral("extern"), "")
          + parcon.Optional(parcon.SignificantLiteral("\"C\""), "")
          + TYPE + WNAME
          + OPEN
          + parcon.Optional(FUNCTION_ARGUMENTS, [])
          + CLOSE
          + SEMICOLON)[lambda x: FUNCTION_toDict(x)]
#########################################################################
#########################################################################

def STRUCT_MEMBER_toDict(x):
  d = dict()
  d[KEY_ID] = "member"
  d["type"] = x[0]
  d["name"] = x[1]
  d["size"] = x[2]
  return d

def STRUCT_toDict(x):
  d = dict()
  d[KEY_ID] = x[0]
  d["content"] = x[1]
  return d

STRUCT_MEMBER_SIZE = parcon.Literal(":") + A_NUMBER
STRUCT_MEMBER = (TYPE+WNAME+parcon.Optional(STRUCT_MEMBER_SIZE, -1)+SEMICOLON)[lambda x: STRUCT_MEMBER_toDict(x)]
STRUCT = ((parcon.SignificantLiteral("class") | parcon.SignificantLiteral("struct"))
            + "{"
            + parcon.ZeroOrMore((parcon.SignificantLiteral("protected:")
                                  | parcon.SignificantLiteral("public:")
                                  | parcon.SignificantLiteral("private:")
                                  | FUNCTION_DECLARATION
                                  | STRUCT_MEMBER))
            + "}"
            + parcon.Optional(parcon.Literal(";")))[lambda x: STRUCT_toDict(x)]

#########################################################################
#########################################################################

def ENUM_toDict(x):
  d = dict()
  d[KEY_ID] = "enum"
  d["text"] = x
  return d

ENUM_VAL = (WNAME
              + parcon.Optional(parcon.Literal("=") + parcon.Word(" \t<>0123456789()"))
              + parcon.Optional(parcon.Literal(",")) + parcon.Optional(COMMENTS))
ENUM_VALS = parcon.Literal("{") + parcon.ZeroOrMore(ENUM_VAL) + parcon.Literal("}")
ENUM = (parcon.SignificantLiteral("enum")
              + parcon.Optional(WNAME)
              + ENUM_VALS
              + parcon.Optional(parcon.Literal(";")))[lambda x: ENUM_toDict(x)]

#########################################################################
#########################################################################

def TYPEDEF_toDict(x):
  d = dict()
  d[KEY_ID] = x[0]
  d["name"] = x[2]
  d["content"] = x[1]
  return d

def NS_OPTIONS_toDict(x):
  d = dict()
  d[KEY_ID] = x[0]
  d["type"] = x[1]
  d["name"] = x[2]
  return d;

NS_OPTIONS = ((parcon.SignificantLiteral("NS_OPTIONS") | parcon.SignificantLiteral("NS_ENUM"))
                          + parcon.Literal("(")
                            + WNAME
                            + parcon.Literal(",") + WNAME
                          + parcon.Literal(")")
                          + ENUM_VALS)[lambda x: NS_OPTIONS_toDict(x)]

TYPEDEF = (parcon.SignificantLiteral("typedef")
                      + (NS_OPTIONS | STRUCT | TYPE | ENUM)
                      + parcon.Optional(WNAME, NO_NAME) + ";")[lambda x: TYPEDEF_toDict(x)]

#########################################################################
#########################################################################

def DEFINE_toDict(x):
  d = dict()
  d[KEY_ID] = x[0]
  d["name"] = x[1]
  d["content"] = x[2]
  return d

UNTIL_NEW_LINE_OR_EMPTY = (parcon.Exact(parcon.ZeroOrMore(parcon.CharNotIn('\n'))
                              + parcon.Literal('\n')))[parcon.concat]

DEFINE = (parcon.SignificantLiteral('#')
            + (parcon.SignificantLiteral('define')
               | parcon.SignificantLiteral('undef')
               | parcon.SignificantLiteral('ifdef')
               | parcon.SignificantLiteral('ifndef')
               | parcon.SignificantLiteral('endif')
               | parcon.SignificantLiteral('else')
               | parcon.SignificantLiteral('if')
            )
            + UNTIL_NEW_LINE_OR_EMPTY)[lambda x: DEFINE_toDict(x)]

#########################################################################
#########################################################################

def INTERFACE_toDict(x):
  d = dict()
  d[KEY_ID] = "interface"
  d["super"] = x[3]
  d["protocols"] = x[4]
  d["name"] = x[1]
  properties = []
  methods = []

  for i in x[5]:
    if i[KEY_ID] == "method_declare":
      methods.append(i)
    if i[KEY_ID] == "prop_declare":
      properties.append(i)

  d["properties"] = properties;
  d["methods"] = methods
  d["declares"] = x[5]
  return d

INTERFACE = (parcon.SignificantLiteral("@interface") + WNAME
                    + parcon.Optional(parcon.SignificantLiteral(":") + WNAME)
                    + parcon.Optional("<" + WNAME_SEP_BY_COMMA + ">")
                    + parcon.ZeroOrMore(METHOD_DECLARE | COMMENTS | PROPERTY)
                    + parcon.SignificantLiteral("@end"))[lambda x: INTERFACE_toDict(x)]

#########################################################################
#########################################################################

def STOP_PARSING(x):
  print SEP
  print SEP
  print "stop parsing due to : ", x
  print SEP
  print SEP
  sys.exit(0)

PARSER_STOP = (parcon.SignificantLiteral("//@stop_parsing"))[lambda x: STOP_PARSING(x)]

#########################################################################
#########################################################################
### Objective C header file grammar:

OBJC_FILE_H = parcon.ZeroOrMore( PARSER_STOP
                          | DEFINE
                          | ENUM
                          | TYPEDEF
                          | INTERFACE
                          | PROTOCOL
                          | AT_CLASS_DECLARE
                          | COMMENTS
                          | INCLUDE
                          | FUNCTION_DECLARATION
                          )

#########################################################################
#########################################################################

###
def logError(l):
  if (not l.endswith("\n")):
    l += "\n"
  sys.stderr.write("ERROR: " + l)

###
def spliceRE(string, searchRE):
  r = re.compile(searchRE)
  res = r.search(string)
  found = None
  if res != None:
      found = res.groups(0)
  return found

###
def process_input(options):
  in_lines = sys.stdin.read().split("\n")
  return process_input_lines(options, in_lines)

###
def process_input_lines(options, in_lines):
  """ process the given in_lines (the content of an objective c header
      file. output a json object describing that input
      """
  isError = False
  in_data = "\n".join(in_lines)

  # this has to be done for some inputs:
  in_data = in_data.replace("\\\n", "")

  # remove the comments:
  in_data = filter_comments(in_data) + "\n"
  in_lines = in_data.split("\n")

  # always end with a newline:
  in_data += "\n"

  # debug nasty inputs:
  # print SEP
  # print "in_lines : ", pretty_json(in_lines)
  # print SEP
  # print "in_data : ", in_data
  # print SEP

  objects = []
  try:
    objects = OBJC_FILE_H.parse_string(in_data)
  except parcon.ParseException as e:
    logError("failed to parse the input")
    error_pos = int(spliceRE(str(e), "Parse failure: At position (\d*):")[0])
    logError(str(e))
    logError(SEP)
    prevLines = []
    C = 0
    L = 0
    for line in in_lines:
      if (C+len(line)-1 >= error_pos):
        logError("parse error: line, %d, error_pos, %d" % (L, C))
        logError(SEP)
        for prevLine in prevLines:
          logError(prevLine)
        logError("%s" % (line))
        logError(((" " * (((error_pos-C))-1))) + COLOR_RED + "^ - this is the error" + COLOR_RESET)
        logError(((" " * (((error_pos-C))-1))) + COLOR_RED + "---------------------" + COLOR_RESET)
        if (L+1 < len(in_lines)):
          logError (in_lines[L+1])
        if (L+2 < len(in_lines)):
          logError (in_lines[L+2])
        break
      C += len(line)
      L += 1
      prevLines.append(line)
      while len(prevLines) > 4:
        prevLines.pop(0)
    logError(SEP)
    logError(SEP)
    sys.exit(10)
  output = dict()
  output["version"] = hex(VERSION) # enforce 0x... version number
  output["objects"] = objects
  return output

###
def read_file(filename):
  in_data = open(filename, "r").read()
  in_lines = in_data.split("\n")
  return (in_data, in_lines)

###
def write_source_file(filename, text, is_sign=True):
  # always end a file with a newline
  if not text.endswith("\n\n"):
    text += "\n\n"
  # remove trailing white spaces
  text = remove_trailing_white_space(text)
  # sign the source file, in case it was requested:
  if is_sign:
    text = parse_simple_objc_sign.sign(text)[0]
  log("writing, %s" % filename)
  open(filename, "w").write(text)

###
def write_class_files(output_dir, class_name, h_file_data, m_file_data):
  # generate filenames:
  h_filename = os.path.join(output_dir, class_name + ".h")
  m_filename = os.path.join(output_dir, class_name + ".mm")
  # write the files:
  write_source_file(h_filename, h_file_data)
  write_source_file(m_filename, m_file_data)

###
def remove_empty_lines(text):
  ret = "\n".join(filter(lambda x : not (len(x.strip()) == 0), text.split("\n")))
  return ret.strip()

###
def remove_trailing_white_space(text):
  lines = text.split("\n")
  lines = map(lambda x : x.rstrip(), lines)
  return "\n".join(lines)

###
def filter_comments(input):
  output = input
  output = re.sub("(//.*)", '', output)
  output = re.sub("(/\*.*?\*/)", '', output, flags=re.DOTALL)
  return output

###
def primitive_type_names():
  return ( "char"
           , "unsigned char"
           , "int"
           , "short"
           , "short int"
           , "long"
           , "long long"
           , "long long int"
           , "float"
           , "double"
           , "unsigned int"
           , "unsigned short"
           , "unsigned long"
           , "unsigned long long"
           , "unsigned long long int"
           , "NSInteger"
           , "NSUInteger"
           , "uint8_t"
           , "uint16_t"
           , "uint32_t"
           , "int8_t"
           , "int16_t"
           , "int32_t"
           )

###
if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("", "--version",
                      action="store_true",
                      help="print version number",
                      dest="version", default=False)
    (options, args) = parser.parse_args()
    if options.version:
      print(VERSION_STR)
      sys.exit(0)
    else:
      output = process_input(options)
      print(json.dumps(output, indent=2))
    sys.exit()

