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

```
notifier/gen_notifier.py test/Protocol002.h
0.0036, PRNT,  generating test/Protocol002.h
0.0086, PRNT,  writing, test/Protocol002Notifier.h
0.0091, PRNT,  writing, test/Protocol002Notifier.mm
```

## Listeners
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

## Notifier: 

```
Protocol002Notifier* notifier = [[Protocol002Notifier alloc] init];
[notifier addSubscription:[[Protocol002NotifierSubcription alloc] initWithListener:listener]];
```

## Issue a strongly typed notification to all listeners:
```
[notifier ping:@"hello"];
```

