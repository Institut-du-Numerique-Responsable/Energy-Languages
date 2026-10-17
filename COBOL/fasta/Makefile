compile:
	cobc -x -O2 -o fasta.cobol_run fasta.cob

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./fasta.cobol_run 25000000" COBOL fasta

run:
	./fasta.cobol_run 25000000

mem:
	/usr/bin/time -v ./fasta.cobol_run 25000000

valgrind:
	valgrind --tool=massif --stacks=yes ./fasta.cobol_run 25000000

clean:
	rm -f fasta.cobol_run
