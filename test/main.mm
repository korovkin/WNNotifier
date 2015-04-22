#import <Foundation/Foundation.h>

#import "Protocol002Notifier.h"
  
#define LOG_LINE() NSLog(@"  calling: %s", __FUNCTION__);

@interface TestListener : NSObject <Protocol002>
  @property (atomic) NSString* msg;
@end

@implementation TestListener

-(id)init {
  self = [super init];
  LOG_LINE();
  return self;
}

-(void)ping:(NSString*)message {
  self.msg = [message copy];
  LOG_LINE();
}

-(void)printMessage:(NSString *)message line:(int)line {
  LOG_LINE();
  NSLog(@"printMessage: %@ line: %d", message, line);
}

- (void) dealloc {
  LOG_LINE();
}

@end

int main(int argc, char** argv) {
  @autoreleasepool {
    NSMutableArray* listeners = [NSMutableArray new];

    Protocol002Notifier* notifier = 
          [[Protocol002Notifier alloc] initWithFirstSubscriptionAdded:nil
                                              lastSubscriptionRemoved:nil];

    for (int i = 0; i < 3; ++i) {
      TestListener* listener = [TestListener new];
      Protocol002NotifierSubcription* subscription = 
       [[Protocol002NotifierSubcription alloc] initWithListener:listener listenerQueue:nil];
      [notifier addSubscription:subscription];
      [listeners addObject:listener];
    }

    [notifier ping:@"just saying,"];
    [notifier ping:@"hello"];
    [notifier printMessage:@"this is a message" line:__LINE__];

    for (TestListener* l in listeners) {
      NSAssert([l.msg isEqualToString:@"hello"], @"message lost");
    }
  }

  NSLog(@"tests: all ok.");

  return EXIT_SUCCESS;
}
