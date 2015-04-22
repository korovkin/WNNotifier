#import <Foundation/Foundation.h>
#import <WNNotifier/WNCodeGen.h>

@protocol Protocol002 <NSObject>

  WNNotifierGenerate({
    "enumerate" : true,
    "listener-ref" : "strong",
    "event-blocks" : true,
    "event-processor-block" : true
  });

-(void)ping:(NSString *)message;
-(void)printMessage:(NSString *)message line:(int)line;
@end
