compile:
	cobc -x -O2 -o nbody.cobol_run nbody.cob

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./nbody.cobol_run 50000000" COBOL n-body

run:
	./nbody.cobol_run 50000000

mem:
	/usr/bin/time -v ./nbody.cobol_run 50000000

valgrind:
	valgrind --tool=massif --stacks=yes ./nbody.cobol_run 50000000

clean:
	rm -f nbody.cobol_run
