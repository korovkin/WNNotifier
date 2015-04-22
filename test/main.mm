#import "Protocol001.h"
#import "Protocol001Notifier.h"
  
#define LOG_LINE() NSLog(@"calling, %s", __FUNCTION__);

@interface TestListener : NSObject <Protocol001>
@end

@implementation TestListener

-(id)init
{
  self = [super init];
  LOG_LINE();
  return self;
}

-(void)a:(NSString *)a 
{
  LOG_LINE();
}

-(void)b:(NSNumber *)b
{
  LOG_LINE();
}

-(void)c:(NSString *)c userContext:(id)userContext
{
  LOG_LINE();
}

-(void)d:(NSNumber *)n userContext:(id)userContext
{
  LOG_LINE();
}

-(void)e:(unsigned int)e
{
  LOG_LINE();
}

-(void)f:(float)f
{
  LOG_LINE();
}

-(void)g:(double)g
{
  LOG_LINE();
}

-(void)h:(double)h hh:(short)hh hhh:(float)hhh
{
  LOG_LINE();
}

-(void)i
{
  LOG_LINE();
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

  Protocol001Notifier* notifier = [[Protocol001Notifier alloc] 
    initWithFirstSubscriptionAdded:nil
    lastSubscriptionRemoved:nil];
  notifier = [[Protocol001Notifier alloc] init];

  for (int i = 0; i < 4; ++i) {
    TestListener* listener = [TestListener new];

    Protocol001NotifierSubcription* subscription = 
     [[Protocol001NotifierSubcription alloc] initWithListener:listener
                  listenerQueue:nil
                  listenerContext:nil];
    [notifier addSubscription:subscription];
  }

  [notifier a:@""];
  [notifier a:@""];


  
  return EXIT_SUCCESS;
}
