// @generated SignedSource<<4c5395f36da84a5b9279b7cd93da2ad7>>

// signed with: https://github.com/korovkin/WNNotifier/notifier/sign.py
// @tool gen_notifier.py:0x4:293e46c30415394be7d0a542d3f14a22
// @input_hash Protocol002.h:32600966df58ccdacd53753b89df0880

#import <Foundation/Foundation.h>
#import <dispatch/dispatch.h>

#import "Protocol002.h"

/**
 Purpose:
 ========
 Notifier for the Protocol002 protocol defined in: Protocol002.h

 Annotations Used:
 =================
 WNNotifierGenerate({
  "atomic": false,
  "enumerate": true,
  "event-blocks": true,
  "event-processor-block": true,
  "listener-context-keyword": "",
  "listener-context-ref": "",
  "listener-ref": "strong"
})
*/

@class Protocol002NotifierSubcription;

typedef void (^Protocol002NotifierVisitor)(Protocol002NotifierSubcription* subscription);
typedef void (^Protocol002NotifierFirstSubscriptionAdded)(Protocol002NotifierSubcription* subscription);
typedef void (^Protocol002NotifierLastSubscriptionRemoved)(Protocol002NotifierSubcription* subscription);
typedef void (^Protocol002NotifierEventProcessor)(SEL selector, NSDictionary* arguments);

@interface Protocol002Notifier : NSObject <Protocol002>
 /**
  Initialize an instance of the Protocol002Notifier with the given event blocks (can be nil).
  IMPORTANT:
    1. to avoid retain cycles, the addedFirst/removedLast blocks should not reference '__strong self'. '__weak self' is fine.
    2. rule of thumb: in case one of the addedFirst/removedLast blocks is provided, chances are the other block is needed as well.
  @param addedFirst a block to be invoked after the first subscription has been added
  @param removedLast a block to be invoked after the last subscription has been removed
 */
 - (instancetype)initWithFirstSubscriptionAdded:(Protocol002NotifierFirstSubscriptionAdded)addedFirst
                        lastSubscriptionRemoved:(Protocol002NotifierLastSubscriptionRemoved)removedLast;
 /**
   Register the given subscription object Protocol002 to be notified.
   The notifications will be delivered to subscription->listener
   for the lifecycle of the provided subscription object.
   IMPORTANT: This API is NOT idempotent.
   @param subscription - subscription object to be added.
 */
 -(void)addSubscription:(Protocol002NotifierSubcription *)subscription;
 /**
   Unregister the given subscription object Protocol002 from being notified.
   @param subscription - subscription object to be removed
 */
 -(void)removeSubscription:(Protocol002NotifierSubcription *)subscription;
 /**
   Enumerate the current subscriptions collection with the given visitor block.
   @param visitor - the block to be used to enumerate the current set of subscriptions
 */
-(void)enumerateSubscriptionsUsingBlock:(Protocol002NotifierVisitor)visitor;
 /**
    a block to process the notified events as a sequence of (SEL, NSDictionary* arguments) tuples.
    a perfect use case for this feature is a file / network logger of events.
    IMPORTANT: 1. even though this is a 'readwrite' property,
               it's unadvised to write this property more than once.
               2. to avoid a retain cycle, the block should avoid
               referencing '__strong self', and prefer '__weak self' instead.
  */
  @property (copy, readwrite) Protocol002NotifierEventProcessor eventProcessor;
@end

@interface Protocol002NotifierSubcription : NSObject
 - (instancetype)initWithListener:(id <Protocol002>)listener
                    listenerQueue:(dispatch_queue_t)listenerQueue;
 @property (atomic, readonly, strong) id <Protocol002> listener;
 @property (atomic, readonly, strong) dispatch_queue_t listenerQueue;
@end

