// @generated SignedSource<<f4866862d8cee6115f42534db4dc8baf>>

// signed with: https://github.com/korovkin/WNNotifier/notifier/sign.py
// @tool gen_notifier.py:0x4:293e46c30415394be7d0a542d3f14a22
// @input_hash Protocol002.h:32600966df58ccdacd53753b89df0880

#if  ! __has_feature(objc_arc)
#error This file must be compiled with ARC. Use -fobjc-arc flag (or convert project to ARC).
#endif

#import <dispatch/dispatch.h>

#import "Protocol002Notifier.h"
#import <WNNotifier/WNNotifierBase.h>

@implementation Protocol002NotifierSubcription
- (instancetype)initWithListener:(id <Protocol002>)listener
                    listenerQueue:(dispatch_queue_t)listenerQueue;
{
  self = [super init];
  if (self) {
    _listener = listener;
    _listenerQueue = listenerQueue;
  }
  return self;
}
@end

@implementation Protocol002Notifier {
  WNNotifierBase* _baseImplementation;
}

/**
  Initialize an instance of the Protocol002Notifier with the given event blocks (can be nil).
  IMPORTANT:
    1. to avoid retain cycles, the addedFirst/removedLast blocks should not reference '__strong self'. '__weak self' is fine.
    2. rule of thumb: in case one of the addedFirst/removedLast blocks is provided, chances are the other block is needed as well.
  @param addedFirst a block to be invoked after the first subscription has been added
  @param removedLast a block to be invoked after the last subscription has been removed
 */
 - (instancetype)initWithFirstSubscriptionAdded:(Protocol002NotifierFirstSubscriptionAdded)addedFirst
                        lastSubscriptionRemoved:(Protocol002NotifierLastSubscriptionRemoved)removedLast
{
  self = [super init];
  if (self) {
    _baseImplementation = [[WNNotifierBase alloc] initAtomic:NO /* atomic */
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

 -(void)addSubscription:(Protocol002NotifierSubcription *)subscription
{
  [_baseImplementation addSubscription:subscription];
}

-(void)removeSubscription:(Protocol002NotifierSubcription *)subscription
{
  [_baseImplementation removeSubscription:subscription];
}
-(void)enumerateSubscriptionsUsingBlock:(Protocol002NotifierVisitor)visitor
{
  if (!visitor) {
    return;
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^bool(Protocol002NotifierSubcription * subscription) {
    visitor(subscription);
    return ((id<Protocol002>)subscription.listener) != nil;
  }];
}


- (void)ping:(NSString *)message
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"ping" : WNNotifierBaseConvertToNSNull((message)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol002NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol002> listener) {
                [listener ping:message];
              });
  }];
}

- (void)printMessage:(NSString *)message line:(int)line
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"printMessage" : WNNotifierBaseConvertToNSNull((message)),
      @"line" : WNNotifierBaseConvertToNSNull(@(line)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol002NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol002> listener) {
                [listener printMessage:message line:line];
              });
  }];
}
@end

