// @generated SignedSource<<9fcde047595929d6f844c3314632fccc>>
// signed with: https://github.com/korovkin/WNNotifier/notifier/sign.py
// @tool gen_notifier.py:0x4:471bcf800d560f9d899fa0afe9738f4e
// @input_hash Protocol001.h:2e7ebcd4171777918fff108fee802f9c

#if  ! __has_feature(objc_arc)
#error This file must be compiled with ARC. Use -fobjc-arc flag (or convert project to ARC).
#endif

#import <dispatch/dispatch.h>

#import "Protocol001Notifier.h"
#import <WNNotifier/WNNotifierBase.h>

@implementation Protocol001NotifierSubcription
- (instancetype)initWithListener:(id <Protocol001>)listener
                    listenerQueue:(dispatch_queue_t)listenerQueue
                  listenerContext:(id)listenerContext;
{
  self = [super init];
  if (self) {
    _listener = listener;
    _listenerQueue = listenerQueue;
    _listenerContext = listenerContext;
  }
  return self;
}
@end

@implementation Protocol001Notifier {
  WNNotifierBase* _baseImplementation;
}

/**
  Initialize an instance of the Protocol001Notifier with the given event blocks (can be nil).
  IMPORTANT:
    1. to avoid retain cycles, the addedFirst/removedLast blocks should not reference '__strong self'. '__weak self' is fine.
    2. rule of thumb: in case one of the addedFirst/removedLast blocks is provided, chances are the other block is needed as well.
  @param addedFirst a block to be invoked after the first subscription has been added
  @param removedLast a block to be invoked after the last subscription has been removed
 */
 - (instancetype)initWithFirstSubscriptionAdded:(Protocol001NotifierFirstSubscriptionAdded)addedFirst
                        lastSubscriptionRemoved:(Protocol001NotifierLastSubscriptionRemoved)removedLast
{
  self = [super init];
  if (self) {
    _baseImplementation = [[WNNotifierBase alloc] initAtomic:YES /* atomic */
                                                     firstSubscriptionBlock:addedFirst
                                                      lastSubscriptionBlock:removedLast];
  }
  return self;
}

 -(void)addSubscription:(Protocol001NotifierSubcription *)subscription
{
  [_baseImplementation addSubscription:subscription];
}

-(void)removeSubscription:(Protocol001NotifierSubcription *)subscription
{
  [_baseImplementation removeSubscription:subscription];
}
-(void)enumerateSubscriptionsUsingBlock:(Protocol001NotifierVisitor)visitor
{
  if (!visitor) {
    return;
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^bool(Protocol001NotifierSubcription * subscription) {
    visitor(subscription);
    return ((id<Protocol001>)subscription.listener) != nil;
  }];
}


- (void)a:(NSString *)a
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"a" : WNNotifierBaseConvertToNSNull((a)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol001NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol001> listener) {
                [listener a:a];
              });
  }];
}

- (void)b:(NSNumber *)b
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"b" : WNNotifierBaseConvertToNSNull((b)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol001NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol001> listener) {
                [listener b:b];
              });
  }];
}

- (void)c:(NSString *)c userContext:(id)userContext
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"c" : WNNotifierBaseConvertToNSNull((c)),
      @"userContext" : WNNotifierBaseConvertToNSNull((userContext)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol001NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol001> listener) {
                [listener c:c userContext:userContext ? userContext : subscription.listenerContext];
              });
  }];
}

- (void)d:(NSNumber *)n userContext:(id)userContext
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"d" : WNNotifierBaseConvertToNSNull((n)),
      @"userContext" : WNNotifierBaseConvertToNSNull((userContext)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol001NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol001> listener) {
                [listener d:n userContext:userContext ? userContext : subscription.listenerContext];
              });
  }];
}

- (void)e:(unsigned int)e
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"e" : WNNotifierBaseConvertToNSNull(@(e)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol001NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol001> listener) {
                [listener e:e];
              });
  }];
}

- (void)f:(float)f
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"f" : WNNotifierBaseConvertToNSNull(@(f)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol001NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol001> listener) {
                [listener f:f];
              });
  }];
}

- (void)g:(double)g
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"g" : WNNotifierBaseConvertToNSNull(@(g)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol001NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol001> listener) {
                [listener g:g];
              });
  }];
}

- (void)h:(double)h hh:(short)hh hhh:(float)hhh
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"h" : WNNotifierBaseConvertToNSNull(@(h)),
      @"hh" : WNNotifierBaseConvertToNSNull(@(hh)),
      @"hhh" : WNNotifierBaseConvertToNSNull(@(hhh)),
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol001NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol001> listener) {
                [listener h:h hh:hh hhh:hhh];
              });
  }];
}

- (void)i
{
  if (_eventProcessor) {
    _eventProcessor(_cmd,
      @{@"i" : [NSNull null],
    });
  }
  [_baseImplementation enumerateSubscriptionsUsingBlock:^(Protocol001NotifierSubcription * subscription) {
    return WNNotifierBaseNotify(
              subscription.listener,
              subscription.listenerQueue,
              ^(id<Protocol001> listener) {
                [listener i];
              });
  }];
}
@end

