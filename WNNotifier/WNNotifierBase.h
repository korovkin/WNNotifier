#import <Foundation/Foundation.h>
#import <dispatch/dispatch.h>

typedef bool (^WNNotifierBaseEnumerateBlock)(id subscription);
typedef void (^WNNotifierBaseEventBlock)(id subscription);

@interface WNNotifierBase : NSObject
 -(instancetype)init;
 -(instancetype)initAtomic:(BOOL)isAtomic
    firstSubscriptionBlock:(WNNotifierBaseEventBlock)firstSubscriptionBlock
     lastSubscriptionBlock:(WNNotifierBaseEventBlock)lastSubscriptionBlock;

 -(void)addSubscription:(id)subscription;
 -(void)removeSubscription:(id)subscription;
 -(void)enumerateSubscriptionsUsingBlock:(WNNotifierBaseEnumerateBlock)block;
@end

typedef void (^WNNotifierBaseNotificationBlock)(id listener);

bool WNNotifierBaseNotify(
  id listener,
  dispatch_queue_t listenerQueue,
  WNNotifierBaseNotificationBlock notificationBlock);

id WNNotifierBaseConvertToNSNull(id object);
