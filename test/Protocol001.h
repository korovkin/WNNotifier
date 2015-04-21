#import <Foundation/Foundation.h>
#import <WNNotifier/WNCodeGen.h>

@protocol Protocol001 <NSObject>

  WNNotifierGenerate({
    "atomic" : true,
    "enumerate" : true,
    "listener-ref" : "strong",
    "event-blocks" : true,
    "event-processor-block" : true,
    "listener-context-keyword" : "userContext",
    "listener-context-ref" : "strong"
  });

-(void)a:(NSString *)a;
-(void)b:(NSNumber *)b;
-(void)c:(NSString *)c userContext:(id)userContext;
-(void)d:(NSNumber *)n userContext:(id)userContext;
-(void)e:(unsigned int)e;
-(void)f:(float)f;
-(void)g:(double)g;
-(void)h:(double)h hh:(short)hh hhh:(float)hhh;
-(void)i;
@end
