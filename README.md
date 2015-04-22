# WNNotifier
Strongly Typed ObjC Notifications
(code generator)

# Example
1. define a protocol:
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
2. code generate a notifier:
```
notifier/gen_notifier.py test/Protocol002.h
0.0036, PRNT,  generating test/Protocol002.h
0.0086, PRNT,  writing, test/Protocol002Notifier.h
0.0091, PRNT,  writing, test/Protocol002Notifier.mm
```
3. listeners:
```
// listener:
@interface TestListener : NSObject <Protocol002>
@end
@implementation TestListener
-(void)ping:(NSString*)message {
}
@end
TestListener* listener = [TestListener new];
```
4. notifier:
```
Protocol002Notifier* notifier = [[Protocol002Notifier alloc] init];
[notifier addSubscription:[[Protocol002NotifierSubcription alloc] initWithListener:listener]];
```
5. issue a strongly typed notification to all listeners:
```
 [notifier ping:@"hello"];
```

# Enjoy.
