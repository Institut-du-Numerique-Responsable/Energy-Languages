compile:
	cobc -x -O2 -o revcomp.cobol_run revcomp.cob

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./revcomp.cobol_run < ../../revcomp-input25000000.txt" COBOL reverse-complement

run:
	./revcomp.cobol_run < ../../revcomp-input25000000.txt

mem:
	/usr/bin/time -v ./revcomp.cobol_run < ../../revcomp-input25000000.txt

valgrind:
	valgrind --tool=massif --stacks=yes ./revcomp.cobol_run < ../../revcomp-input25000000.txt

clean:
	rm -f revcomp.cobol_run
