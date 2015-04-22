#pragma once

/**
 *    "atomic" : true / false
 *            locking mechanism will be used to to access the listeners container
 *            (making addSubscription / removeSubscription thread safe)
 *            default value: false
 *
 *    "listener-ref" : "weak" / "strong"
 *            the notifier will be referencing listeners with a **weak** reference
 *            default value: "weak"
 *
 *    "event-blocks" : true
 *            code-gen event blocks: onAddedFirstSubscription, onRemovedLastSubscription
 *            default value: false
 *
 *    "event-processor-block" : true
 *            code-gen event block: to serialize the announcement into a (SEL, NSDictionary*) tuple
 *            default value: false
 *
 *    "enumerate" : true
 *            code-gen subscription enumeration routines: enumerateSubscriptionsUsingBlock (default: no)
 *
 *    "listener-context-keyword" : <name>
 *            name of the user context keyword where user context will be delivered to
 *            default value: None (listenerContext is disabled)
 *
 *    "listener-context-ref" : "weak" / "strong"
 *            the notifier will be referencing listener's context with a **strong** reference
 *            default value: "strong"
 *
 */
#define WNNotifierGenerate(...)
