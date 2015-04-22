#if  ! __has_feature(objc_arc)
#error This file must be compiled with ARC. Use -fobjc-arc flag (or convert project to ARC).
#endif

#import "WNNotifierBase.h"

typedef void (*WNNotifierBaseExecuteWork)(WNNotifierBase* Self, dispatch_block_t work);

@implementation WNNotifierBase {
  NSMutableArray * _subscriptions;
  BOOL _isAtomic;
  WNNotifierBaseExecuteWork _executeWork;
  WNNotifierBaseEventBlock _onFirstSubscriptionAdded;
  WNNotifierBaseEventBlock _onLastSubscriptionRemoved;
}

- (instancetype)init
{
  return [self initAtomic:NO firstSubscriptionBlock:nil lastSubscriptionBlock:nil];
}

static void _executeWorkAtomic(WNNotifierBase* Self, dispatch_block_t work)
{
  @synchronized(Self->_subscriptions) {
    // do the work under a lock
    work();
  }
}

static void _executeWorkNonatomic(WNNotifierBase* Self, dispatch_block_t work)
{
  // just do the work:
  work();
}

-(instancetype)initAtomic:(BOOL)isAtomic
   firstSubscriptionBlock:(WNNotifierBaseEventBlock)firstSubscriptionBlock
    lastSubscriptionBlock:(WNNotifierBaseEventBlock)lastSubscriptionBlock
{
  self = [super init];
  if (self) {
    _subscriptions = [NSMutableArray array];
    _isAtomic = isAtomic;
    _onFirstSubscriptionAdded = [firstSubscriptionBlock copy];
    _onLastSubscriptionRemoved = [lastSubscriptionBlock copy];

    if (isAtomic) {
      _executeWork = _executeWorkAtomic;
    }
    else {
      _executeWork = _executeWorkNonatomic;
    }
  }
  return self;
}

- (void)addSubscription:(id)subscription
{
  if (!subscription) {
    return;
  }

  _executeWork(self, ^{
    const NSUInteger prevCount = _subscriptions.count;
    [_subscriptions addObject:subscription];

    if (_onFirstSubscriptionAdded && prevCount == 0 && _subscriptions.count == 1) {
      _onFirstSubscriptionAdded(subscription);
    }
  });
}

-(void)removeSubscription:(id)subscription
{
  if (!subscription) {
    return;
  }

  _executeWork(self, ^{
    const NSUInteger prevCount = _subscriptions.count;
    [_subscriptions removeObject:subscription];

    if (_onLastSubscriptionRemoved && prevCount != 0 && _subscriptions.count == 0) {
      _onLastSubscriptionRemoved(subscription);
    }
  });
}

-(void)enumerateSubscriptionsUsingBlock:(WNNotifierBaseEnumerateBlock)block
{
  dispatch_block_t work = ^{
    NSMutableArray * zombieSubscriptions = nil;

    for (id subscription in _subscriptions) {
      const bool isKeep = block(subscription);

      if (!zombieSubscriptions) {
        zombieSubscriptions = [NSMutableArray array];
      }
      if (!isKeep) {
        [zombieSubscriptions addObject:subscription];
      }
    }

    if (zombieSubscriptions) {
      // clean-up zombie subscriptions 
      // (listeners associated with that subscription, has been already deallocated:
      for (id zombieSubscription in zombieSubscriptions) {
        [self removeSubscription:zombieSubscription];
      }
    }
  };

  _executeWork(self, work);
}

@end

bool WNNotifierBaseNotify(
  id listener,
  dispatch_queue_t listenerQueue,
  WNNotifierBaseNotificationBlock notificationBlock)
{
  if (listener) {
    if (listenerQueue) {
      dispatch_async(listenerQueue, ^{
        notificationBlock(listener);
      });
    }
    else {
      notificationBlock(listener);
    }
  }

  return listener != nil;
}

id WNNotifierBaseConvertToNSNull(id object)
{
  static id nullObject = [NSNull null];
  if (object) {
    return object;
  }
  return nullObject;
}

