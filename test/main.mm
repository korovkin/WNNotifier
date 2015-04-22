#import <Foundation/Foundation.h>

#import "Protocol002.h"
#import "Protocol002Notifier.h"
  
#define LOG_LINE() NSLog(@"calling, %s", __FUNCTION__);

@interface TestListener : NSObject <Protocol002>
  @property (atomic) NSString* msg;
@end

@implementation TestListener

-(id)init
{
  self = [super init];
  LOG_LINE();
  return self;
}

-(void)ping:(NSString*)message
{
  LOG_LINE();
  NSLog(@"message, %@", message);
  self.msg = [message copy];
}

- (void) dealloc
{
  LOG_LINE();
}
@end

int main(int argc, char** argv) 
{
  NSLog(@"hello");
  NSLog(@"-----");

  NSMutableArray* listeners = [NSMutableArray new];

  Protocol002Notifier* notifier = [[Protocol002Notifier alloc] 
                            initWithFirstSubscriptionAdded:nil
                            lastSubscriptionRemoved:nil];

  for (int i = 0; i < 4; ++i) {
    TestListener* listener = [TestListener new];
    listener.msg = @"x";
    Protocol002NotifierSubcription* subscription = 
     [[Protocol002NotifierSubcription alloc] initWithListener:listener listenerQueue:nil];
    [notifier addSubscription:subscription];
    [listeners addObject:listener];
  }

  [notifier ping:@"hello"];
  [notifier ping:@"hello"];

  for (TestListener* l in listeners) {
    assert(YES == [l.msg isEqualToString:@"hello"]);
  }

  NSAssert(0, @"");


  return EXIT_SUCCESS;
}
