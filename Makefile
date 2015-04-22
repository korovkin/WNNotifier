
SRC = test/Protocol001Notifier.mm \
			WNNotifier/WNNotifierBase.mm \
			test/main.mm

all: gen compile

gen:
	notifier/gen_notifier.py test/Protocol001.h

compile:
	clang++ -g -x objective-c++ -arch x86_64 -fobjc-arc -I . -framework Foundation $(SRC) -o test/runTests

clean: 
	rm -rfv test/runTests.dSYM test/runTests
