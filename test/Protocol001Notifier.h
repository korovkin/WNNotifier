// @generated SignedSource<<0be85a0e4b135aa78a811330e4ecceee>>

// signed with: https://github.com/korovkin/WNNotifier/notifier/sign.py
// @tool gen_notifier.py:0x4:293e46c30415394be7d0a542d3f14a22
// @input_hash Protocol001.h:2e7ebcd4171777918fff108fee802f9c

#import <Foundation/Foundation.h>
#import <dispatch/dispatch.h>

#import "Protocol001.h"

/**
 Purpose:
 ========
 Notifier for the Protocol001 protocol defined in: Protocol001.h

 Annotations Used:
 =================
 WNNotifierGenerate({
  "atomic": true,
  "enumerate": true,
  "event-blocks": true,
  "event-processor-block": true,
  "listener-context-keyword": "userContext",
  "listener-context-ref": "strong",
  "listener-ref": "strong"
})
*/

@class Protocol001NotifierSubcription;

typedef void (^Protocol001NotifierVisitor)(Protocol001NotifierSubcription* subscription);
typedef void (^Protocol001NotifierFirstSubscriptionAdded)(Protocol001NotifierSubcription* subscription);
typedef void (^Protocol001NotifierLastSubscriptionRemoved)(Protocol001NotifierSubcription* subscription);
typedef void (^Protocol001NotifierEventProcessor)(SEL selector, NSDictionary* arguments);

@interface Protocol001Notifier : NSObject <Protocol001>
 /**
  Initialize an instance of the Protocol001Notifier with the given event blocks (can be nil).
  IMPORTANT:
    1. to avoid retain cycles, the addedFirst/removedLast blocks should not reference '__strong self'. '__weak self' is fine.
    2. rule of thumb: in case one of the addedFirst/removedLast blocks is provided, chances are the other block is needed as well.
  @param addedFirst a block to be invoked after the first subscription has been added
  @param removedLast a block to be invoked after the last subscription has been removed
 */
 - (instancetype)initWithFirstSubscriptionAdded:(Protocol001NotifierFirstSubscriptionAdded)addedFirst
                        lastSubscriptionRemoved:(Protocol001NotifierLastSubscriptionRemoved)removedLast;
 /**
   Register the given subscription object Protocol001 to be notified.
   The notifications will be delivered to subscription->listener
   for the lifecycle of the provided subscription object.
   IMPORTANT: This API is NOT idempotent.
   @param subscription - subscription object to be added.
 */
 -(void)addSubscription:(Protocol001NotifierSubcription *)subscription;
 /**
   Unregister the given subscription object Protocol001 from being notified.
   @param subscription - subscription object to be removed
 */
 -(void)removeSubscription:(Protocol001NotifierSubcription *)subscription;
 /**
   Enumerate the current subscriptions collection with the given visitor block.
   @param visitor - the block to be used to enumerate the current set of subscriptions
 */
-(void)enumerateSubscriptionsUsingBlock:(Protocol001NotifierVisitor)visitor;
 /**
    a block to process the notified events as a sequence of (SEL, NSDictionary* arguments) tuples.
    a perfect use case for this feature is a file / network logger of events.
    IMPORTANT: 1. even though this is a 'readwrite' property,
               it's unadvised to write this property more than once.
               2. to avoid a retain cycle, the block should avoid
               referencing '__strong self', and prefer '__weak self' instead.
  */
  @property (copy, readwrite) Protocol001NotifierEventProcessor eventProcessor;
@end

@interface Protocol001NotifierSubcription : NSObject
 - (instancetype)initWithListener:(id <Protocol001>)listener
                    listenerQueue:(dispatch_queue_t)listenerQueue
                  listenerContext:(id)listenerContext;
 @property (atomic, readonly, strong) id <Protocol001> listener;
 @property (atomic, readonly, strong) dispatch_queue_t listenerQueue;
 @property (atomic, readonly, strong) id listenerContext;
@end

