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
import string
import hashlib
import parse_objc as parser
import sign

#### tool version:
VERSION = parser.VERSION
VERSION_STR = sign.source_file_signature(__file__, VERSION)

#### shortcuts:
ID = parser.KEY_ID
pretty_json = parser.pretty_json
pretty_pprint = parser.pretty_pprint
log = parser.log
log_info = parser.log_info

################## Templates ############################
#########################################################

####
notifier_initializer_declaration_event_blocks_template = """
 /**
  Initialize an instance of the ${notifier_name} with the given event blocks (can be nil).
  IMPORTANT:
    1. to avoid retain cycles, the addedFirst/removedLast blocks should not reference '__strong self'. '__weak self' is fine.
    2. rule of thumb: in case one of the addedFirst/removedLast blocks is provided, chances are the other block is needed as well.
  @param addedFirst a block to be invoked after the first subscription has been added
  @param removedLast a block to be invoked after the last subscription has been removed
 */
 - (instancetype)initWithFirstSubscriptionAdded:(${notifier_name}FirstSubscriptionAdded)addedFirst
                        lastSubscriptionRemoved:(${notifier_name}LastSubscriptionRemoved)removedLast
""".strip()

####
notifier_initializer_declaration_template = """
 /**
  Initialize an instance of the ${notifier_name}
 */
 - (instancetype)init
""".strip()

####
notifier_initializer_implementation_event_blocks_template = """
{
  self = [super init];
  if (self) {
    _baseImplementation = [[WNNotifierBase alloc] initAtomic:${is_notifier_atomic} /* atomic */
                                                     firstSubscriptionBlock:addedFirst
                                                      lastSubscriptionBlock:removedLast];
  }
  return self;
}

- (instancetype)init
{
  NSAssert(NO,
        @"ERROR: please use: initWithFirstSubscriptionAdded:lastSubscriptionRemoved: to init this object");

  return nil;
}
""".strip()

####
notifier_initializer_implementation_template = """
{
  self = [super init];
  if (self) {
    _baseImplementation = [[WNNotifierBase alloc] initAtomic:${is_notifier_atomic}
                                                     firstSubscriptionBlock:nil
                                                      lastSubscriptionBlock:nil];
  }
  return self;
}
""".strip()

####
enumerator_typedef_template = """
typedef void (^${notifier_name}Visitor)(${notifier_name}Subcription* subscription)
""".strip()

####
first_subscription_added_typedef_template = """
typedef void (^${notifier_name}FirstSubscriptionAdded)(${notifier_name}Subcription* subscription)
""".strip()

####
last_subscription_removed_typedef_template = """
typedef void (^${notifier_name}LastSubscriptionRemoved)(${notifier_name}Subcription* subscription)
""".strip()

####
event_processor_typedef_template = """
typedef void (^${notifier_name}EventProcessor)(SEL selector, NSDictionary* arguments)
""".strip()

####
event_processor_property_template = """
  /**
    a block to process the notified events as a sequence of (SEL, NSDictionary* arguments) tuples.
    a perfect use case for this feature is a file / network logger of events.

    IMPORTANT: 1. even though this is a 'readwrite' property,
               it's unadvised to write this property more than once.
               2. to avoid a retain cycle, the block should avoid
               referencing '__strong self', and prefer '__weak self' instead.
  */
  @property (copy, readwrite) ${notifier_name}EventProcessor eventProcessor;
""".strip()


###
notifier_interface_template = """
@interface ${notifier_name} : NSObject <${listener_name}>
 ${notifier_initializer_declaration};
 /**
   Register the given subscription object ${listener_name} to be notified.
   The notifications will be delivered to subscription->listener
   for the lifecycle of the provided subscription object.

   IMPORTANT: This API is NOT idempotent.
   @param subscription - subscription object to be added.
 */
 -(void)addSubscription:(${notifier_name}Subcription *)subscription;
 /**
   Unregister the given subscription object ${listener_name} from being notified.
   @param subscription - subscription object to be removed
 */
 -(void)removeSubscription:(${notifier_name}Subcription *)subscription;
 ${enumerator_declaration}
 ${event_processor_property}
@end
""".strip()

###
notifier_subscription_listener_context_property_template = """
  @property (atomic, readonly, ${listener_context_ref}) id listenerContext
""".strip()

###
notifier_subscription_initializer_declaration_with_context_template = """
 - (instancetype)initWithListener:(id <${listener_name}>)listener
                    listenerQueue:(dispatch_queue_t)listenerQueue
                  listenerContext:(id)listenerContext
""".strip()

###
notifier_subscription_initializer_declaration_no_context_template = """
 - (instancetype)initWithListener:(id <${listener_name}>)listener
                    listenerQueue:(dispatch_queue_t)listenerQueue
""".strip()

###
notifier_subscription_interface_template = """
@interface ${notifier_name}Subcription : NSObject
 ${notifier_subscription_initializer_declaration}
 @property (atomic, readonly, ${listener_ref}) id <${listener_name}> listener;
 @property (atomic, readonly, strong) dispatch_queue_t listenerQueue;
 ${notifier_subscription_listener_context_property}
@end
"""

###
notifier_subscription_implementation_template = """
@implementation ${notifier_name}Subcription

${notifier_subscription_initializer_declaration}
{
  self = [super init];
  if (self) {
    _listener = listener;
    _listenerQueue = listenerQueue;
    ${notifier_subscription_implementation_extension}
  }
  return self;
}

@end
""".strip()

####
typedefs_template = """
${enumerator_typedef}${first_subscription_added_typedef}${last_subscription_removed_typedef}
${event_processor_typedef}
""".strip()

####
documentation_header_template = """
/**
 Purpose:
 ========
 Notifier for the ${listener_name} protocol defined in: ${listener_base_filename}

 Annotations Used:
 =================
 ${annotation_as_json_string}
*/
""".strip()

####
file_template_notifier_h = """
// @tool ${generated_by}
// @input_hash ${input_file_hash}

#import <Foundation/Foundation.h>
#import <dispatch/dispatch.h>

#import "${listener_name}.h"

${documentation_header}

@class ${notifier_name}Subcription;

${typedefs}${notifier_interface}${notifier_subscription_interface}

""".strip()

####
file_template_notifier_m = """
// @tool ${generated_by}
// @input_hash ${input_file_hash}

#if  ! __has_feature(objc_arc)
#error This file must be compiled with ARC. Use -fobjc-arc flag (or convert project to ARC).
#endif

#import <dispatch/dispatch.h>

#import "${notifier_name}.h"
#import <WNNotifier/WNNotifierBase.h>

${notifier_subscription_implementation}

@implementation ${notifier_name} {
  WNNotifierBase* _baseImplementation;
}

${notifier_initializer_declaration}
${notifier_initializer_implementation}

 -(void)addSubscription:(${notifier_name}Subcription *)subscription
{
  [_baseImplementation addSubscription:subscription];
}

-(void)removeSubscription:(${notifier_name}Subcription *)subscription
{
  [_baseImplementation removeSubscription:subscription];
}
${enumerator_implementation}
${protocol_implementation}
@end
""".strip()

####
enumerator_implementation_template = """
-(void)enumerateSubscriptionsUsingBlock:(${notifier_name}Visitor)visitor
{
  if (!visitor) {
    return;
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^bool(${notifier_name}Subcription * subscription) {
    visitor(subscription);
    return ((id<${listener_name}>)subscription.listener) != nil;
  }];
}
""".strip()

####
enumerator_declaration_template = """
 /**
   Enumerate the current subscriptions collection with the given visitor block.
   @param visitor - the block to be used to enumerate the current set of subscriptions
 */
-(void)enumerateSubscriptionsUsingBlock:(${notifier_name}Visitor)visitor;
""".strip()


####
method_event_processor_implementation_template = """
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{${event_dictionary_content}
    });
  }
""".strip()

####
method_required_implementation_template = """
${mdeclaration}
{
  ${method_event_processor_implementation}
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(${notifier_name}Subcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<${listener_name}> listener) {
                [listener ${minvocation}];
              });
  }];
}
""".strip()

####
method_optional_implementation_template = """
${mdeclaration}
{
  ${method_event_processor_implementation}
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(${notifier_name}Subcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<${listener_name}> listener) {
                if ([listener respondsToSelector:@selector(${mselector})]) {
                  [listener ${minvocation}];
                }
              });
  }];
}
""".strip()

####
def verify_annotation(annotation):
 log_info("annotation, %s" % annotation)
 if annotation["atomic"] not in (True , False):
   raise Exception("atomic : can only be 'true' or 'false', not, %s" % annotation["atomic"])
 if annotation["listener-ref"] not in ("weak" , "strong"):
   raise Exception("listener-ref : can only be 'weak' or 'strong', not, %s" % annotation["listener-ref"])
 if annotation["event-blocks"] not in (True, False):
   raise Exception("event-blocks : can only be 'True' or 'False', not, %s" % annotation["event-blocks"])
 if annotation["event-processor-block"] not in (True, False):
   raise Exception("event-processor-block : can only be 'True' or 'False', not, %s" % annotation["event-processor-block"])
 if annotation["enumerate"] not in (True, False):
   raise Exception("enumerate : can only be 'True' or 'False', not, %s" % annotation["enumerate"])
 if len(annotation["listener-context-keyword"]) > 0 and not annotation["listener-context-keyword"].isalpha():
   raise Exception("listener-context-keyword : should be a all alpha word, not, %s" % annotation["listener-context-keyword"])
 if annotation["listener-context-ref"] not in ("weak", "strong", ""):
   raise Exception("listener-context-ref : can only be 'weak' or 'strong' or '', not, %s" % annotation["listener-context-ref"])

####
def gen_event_processor_implementation(annotation, method):
  """
    generate an event dictionary for the given 'method'
  """
  event_dictionary_content = []
  for keyword in method['mkeywords']:
    keyword_name = keyword["keyword"]
    keyword_type = keyword["type"]
    if keyword.has_key("arg") and keyword['arg']:
      at = ""
      if keyword_type["name"] in parser.primitive_type_names():
        at = "@"
      keyword_arg  = "WNNotifierBaseConvertToNSNull(" + at + "(" + keyword["arg"] + ")" + ")"
    else:
      keyword_arg  = "[NSNull null]"
    event_dictionary_content.append(
        string.Template("""@"${keyword_name}" : ${keyword_arg}, """)
                      .substitute(
                        { "keyword_name" : keyword_name,
                          "keyword_arg"  : keyword_arg}))
  event_dictionary_content = "\n      ".join(event_dictionary_content)
  method_event_processor_implementation = string.Template(
      method_event_processor_implementation_template).substitute(
          event_dictionary_content=event_dictionary_content)
  return method_event_processor_implementation

####
def gen_notifier_v2_for_protocol(options, filename, objects, prot_object):
  parser.protocol_methods_update_decorations(prot_object)
  output_dir, base_filename = os.path.split(filename)

  listener_name = prot_object["name"]
  notifier_name = listener_name + "Notifier"

  if options.notifier_name:
    notifier_name = options.notifier_name

  # get the annotation:
  annotation_default = {
    "atomic"       : False,
    "listener-ref" : "weak",
    "event-blocks" : False,
    "enumerate"    : False,
    "listener-context-keyword" : "",
    "listener-context-ref" : "",
    "event-processor-block" : False
  }
  annotation = annotation_default.copy()
  if "json" in prot_object["WNNotifierGenerate"]:
    annotation.update(prot_object["WNNotifierGenerate"]["json"])
  verify_annotation(annotation)

  protocol_implementation = ""
  methods = prot_object["methods"]

  # build up the implementation, method by method
  for method in methods:
    # default template params:
    template_params = {}

    # override the argument for listener-context-keyword
    override_arg_for_keywords = {}
    keyword_name = annotation["listener-context-keyword"]
    if len(keyword_name):
      keyword_arg = "%s ? %s : subscription.listenerContext" % (
          keyword_name,
          keyword_name)
      override_arg_for_keywords = {keyword_name : keyword_arg}

    # build a declaration, invocation and a selector for this method:
    (mdeclaration, minvocation, mselector) = parser.protocol_method_recostruct(
                            method,
                            override_arg_for_keywords)

    # generate the event processor code:
    method_event_processor_implementation = ""
    if annotation["event-processor-block"]:
      method_event_processor_implementation = \
        gen_event_processor_implementation(annotation, method)

    # function implementation:
    template_string = method_required_implementation_template
    if method["decoration"] == ["@optional"]:
      template_string = method_optional_implementation_template
    template_string = template_string.strip()

    # template parameters:
    template_params.update({
      "listener_name" : listener_name,
      "notifier_name" : notifier_name,
      "mdeclaration" : mdeclaration,
      "minvocation" : minvocation,
      "mselector" : mselector,
      "method_event_processor_implementation" : method_event_processor_implementation,
    })

    # method implementation:
    method_implementation = parser.remove_empty_lines(
      string.Template(template_string).substitute(template_params))

    # keep going:
    protocol_implementation += "\n\n" + method_implementation

  # hash the input file:
  input_file_hash = base_filename + ":" + sign.sign_data(open(filename, "r").read())

  is_notifier_atomic = "NO"
  if annotation["atomic"]:
    is_notifier_atomic = "YES"

  # requested ref types:
  listener_ref = annotation["listener-ref"]
  listener_context_ref = annotation["listener-context-ref"]

  # embed the annotations into the generated file:
  annotation_as_json_string = "WNNotifierGenerate(%s)" % pretty_json(annotation)

  # basic params:
  template_params.update({
    "generated_by"                   : VERSION_STR,
    "notifier_name"                 : notifier_name,
    "listener_name"                  : listener_name,
    "is_notifier_atomic"            : is_notifier_atomic,
    "listener_ref"                   : listener_ref,
    "listener_context_ref"           : listener_context_ref,
    "annotation_as_json_string"      : annotation_as_json_string,
    "listener_base_filename"         : base_filename
  })

  # enumerators:
  enumerator_implementation = ""
  enumerator_declaration = ""
  enumerator_typedef = ""
  if annotation["enumerate"]:
    enumerator_implementation = string.Template(enumerator_implementation_template).substitute(template_params)
    enumerator_declaration = string.Template(enumerator_declaration_template).substitute(template_params)
    enumerator_typedef = string.Template(enumerator_typedef_template).substitute(template_params) + ";\n"

  # event blocks:
  notifier_initializer_declaration = ""
  notifier_initializer_implementation = ""
  declaration_template = notifier_initializer_declaration_template
  implementation_template = notifier_initializer_implementation_template
  first_subscription_added_typedef = ""
  last_subscription_removed_typedef = ""
  if annotation["event-blocks"]:
    declaration_template = notifier_initializer_declaration_event_blocks_template
    implementation_template = notifier_initializer_implementation_event_blocks_template
    first_subscription_added_typedef = string.Template(first_subscription_added_typedef_template).substitute(template_params) + ";\n"
    last_subscription_removed_typedef = string.Template(last_subscription_removed_typedef_template).substitute(template_params) + ";\n"
  notifier_initializer_declaration = string.Template(declaration_template).substitute(template_params)
  notifier_initializer_implementation = string.Template(implementation_template).substitute(template_params)

  notifier_subscription_listener_context_property = ""
  notifier_subscription_implementation_extension = ""
  notifier_subscription_initializer_declaration = string.Template(
              notifier_subscription_initializer_declaration_no_context_template).substitute(template_params) + ";"
  if len(annotation["listener-context-ref"]):
    notifier_subscription_listener_context_property = string.Template(
              notifier_subscription_listener_context_property_template).substitute(template_params) + ";"
    notifier_subscription_initializer_declaration = string.Template(
              notifier_subscription_initializer_declaration_with_context_template).substitute(template_params) + ";"
    notifier_subscription_implementation_extension = "_listenerContext = listenerContext;"

  # event processors:
  event_processor_typedef = ""
  event_processor_property = ""
  if annotation["event-processor-block"]:
    event_processor_typedef = string.Template(event_processor_typedef_template).substitute(template_params) + ";"
    event_processor_property = string.Template(event_processor_property_template).substitute(template_params)

  # populate the templates, and write the files:
  template_params.update({
    "protocol_implementation"              : protocol_implementation,
    "input_file_hash"                      : input_file_hash,

    # enumerator:
    "enumerator_implementation"            : enumerator_implementation,
    "enumerator_declaration"               : enumerator_declaration,
    "enumerator_typedef"                   : enumerator_typedef,

    # initializer:
    "notifier_initializer_declaration"    : notifier_initializer_declaration,
    "notifier_initializer_implementation" : notifier_initializer_implementation,
    "first_subscription_added_typedef"     : first_subscription_added_typedef,
    "last_subscription_removed_typedef"    : last_subscription_removed_typedef,

    # listener context:
    "notifier_subscription_listener_context_property" : notifier_subscription_listener_context_property,
    "notifier_subscription_initializer_declaration"   : notifier_subscription_initializer_declaration,
    "notifier_subscription_implementation_extension"  : notifier_subscription_implementation_extension,

    # event processor:
    "event_processor_typedef"        : event_processor_typedef,
    "event_processor_property"       : event_processor_property,
  })

  # subscription object implementation:
  notifier_subscription_implementation = parser.remove_empty_lines(
      string.Template(
        notifier_subscription_implementation_template).substitute(
          template_params))

  template_params.update({
    "notifier_subscription_implementation"   : notifier_subscription_implementation,
  })

  # subscription object interface:
  notifier_subscription_interface = string.Template(
    notifier_subscription_interface_template).substitute(
      template_params)
  # notifier interface:
  notifier_interface = string.Template(
    notifier_interface_template).substitute(
      template_params)
  # typedef section:
  typedefs = string.Template(
    typedefs_template).substitute(
      template_params)
  # doc header:
  documentation_header = string.Template(
    documentation_header_template).substitute(
      template_params)
  # clear out some spaces:
  notifier_subscription_interface = parser.remove_empty_lines(notifier_subscription_interface) + "\n\n"
  notifier_interface = parser.remove_empty_lines(notifier_interface) + "\n\n"
  typedefs = parser.remove_empty_lines(typedefs)
  if len(typedefs):
    typedefs += "\n\n"

  # extend the template params:
  template_params.update({
    "notifier_subscription_interface"     : notifier_subscription_interface,
    "notifier_interface"                  : notifier_interface,
    "typedefs"                             : typedefs,
    "documentation_header"                 : documentation_header
  })

  # write the files:
  parser.write_class_files( output_dir,
                        notifier_name,
                        string.Template(file_template_notifier_h).substitute(template_params),
                        string.Template(file_template_notifier_m).substitute(template_params))

####
def get_objects_with_id(objects, id):
  ret = []
  for object in objects:
    if object[ID] == id:
      ret.append(object)
  return ret

####
def gen_notifier_v2(options, filename):
  in_data, in_lines = parser.read_file(filename)
  objects = parser.process_input_lines(options, in_lines)
  objects = objects["objects"]
  log_info("objects = \n%s" % pretty_pprint(objects))
  protocols = get_objects_with_id(objects, "protocol")

  # has to contain a protocol:
  if len(protocols) <= 0 or len(protocols) > 1:
    raise Exception("file, %s, doesn't cotain a protocol" % filename)

  for prot_object in protocols:
    log_info("prot = %s" % pretty_json(prot_object))
    gen_notifier_v2_for_protocol(options, filename, objects, prot_object)

####
def main():
  oparser = optparse.OptionParser(usage="\n %prog <options> <protocol h file1>")
  oparser.add_option("", "--version",
                    action="store_true",
                    help="print version number",
                    dest="version", default=False)
  oparser.add_option("", "--verbose",
                    action="store_true",
                    help="print more information while testing",
                    dest="verbose",
                    default=False)
  oparser.add_option("", 
                    "--notifier_name",
                    help="set (override) the name of the notifier to be <notifier_name> (default <ProtocolName>Notifier)",
                    dest="notifier_name",
                    default=None)
  (options, filenames) = oparser.parse_args()

  parser.log_info_enabled = options.verbose
  parser.log_info("generating notifier...")

  log_info("filenames   = %s" % str(filenames))
  log_info("options     = %s" % str(options))

  if options.version:
    print(VERSION_STR)
    sys.exit(0)

  if options.notifier_name and len(filenames) > 1:
    raise Exception("--notifier_name can not be set when more than one fiename is specified")

  for filename in filenames:
    log("generating "+ filename)
    gen_notifier_v2(options, filename)

####
if __name__ == "__main__":
  main()

