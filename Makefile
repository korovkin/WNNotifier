
SRC = \
			test/Protocol001Notifier.mm \
			test/Protocol002Notifier.mm \
			WNNotifier/WNNotifierBase.mm \
			test/main.mm

COMPILE = clang++ -DNS_BLOCK_ASSERTIONS=1 -g -O2 -x objective-c++ -arch x86_64 -fobjc-arc -I . -framework Foundation

all: gen compile test

gen:
	notifier/gen_notifier.py test/Protocol001.h
	notifier/gen_notifier.py test/Protocol002.h

compile:
	$(COMPILE) $(SRC) -o test/runTests

clean: 
	rm -rfv test/runTests.dSYM test/runTests

.phony:

test: .phony
	test/runTests
