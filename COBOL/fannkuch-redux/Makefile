compile:
	cobc -x -O2 -o fannkuchredux.cobol_run fannkuchredux.cob

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./fannkuchredux.cobol_run 12" COBOL fannkuch-redux

run:
	./fannkuchredux.cobol_run 12

mem:
	/usr/bin/time -v ./fannkuchredux.cobol_run 12

valgrind:
	valgrind --tool=massif --stacks=yes ./fannkuchredux.cobol_run 12

clean:
	rm -f fannkuchredux.cobol_run
