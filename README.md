<<<<<<< HEAD
# WNNotifier

Strongly Typed ObjC Notifications
(code generator)


# Example

## Define a strongly typed protocol:

``` ObjectiveC
@protocol Protocol002 <NSObject>
  WNNotifierGenerate({
    "enumerate" : true,
    "listener-ref" : "strong",
    "event-blocks" : true,
    "event-processor-block" : true
  });
  -(void)ping:(NSString *)message;
@end
```

## Generate code for your notifier:

``` bash
notifier/gen_notifier.py test/Protocol002.h
0.0036, PRNT,  generating test/Protocol002.h
0.0086, PRNT,  writing, test/Protocol002Notifier.h
0.0091, PRNT,  writing, test/Protocol002Notifier.mm
```

## Listeners
``` ObjectiveC
// listener:
@interface TestListener : NSObject <Protocol002>
@end
@implementation TestListener
-(void)ping:(NSString*)message {
}
@end
TestListener* listener = [TestListener new];
```

## Notifier: 

``` ObjectiveC
Protocol002Notifier* notifier = [[Protocol002Notifier alloc] init];
[notifier addSubscription:[[Protocol002NotifierSubcription alloc] initWithListener:listener]];
```

## Issue a strongly typed notification to all listeners:
``` ObjectiveC
[notifier ping:@"hello"];
```
=======
# line.py


Usage:
```
Usage: line.py [options]

   Process the stdin line by line. apply the following operators on each line.

Options:
  -h, --help         show this help message and exit
  --version          print version number
  --Prefix=PREFIX    prefix each line with the given string
  --Postfix=POSTFIX  postfix each line with the given string
  --Grep=GREP        output lines containing the given RE
  --Splice=SPLICE    Output the given RE
  --Replace=REPLACE  Replace --Replace RE with --With
  --With=WITH        Replace --Replace RE with --With
```


Examples:

```
cat lines.txt
A
B
C

cat lines.txt | ./line.py --Prefix "prefix: " --Postfix ": postfix"
prefix: A: postfix
prefix: B: postfix
prefix: C: postfix

 # cat lines.txt | ./line.py --Splice "A|B"
A
B

``
>>>>>>> adding line.py

