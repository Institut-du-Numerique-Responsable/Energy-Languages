compile:
	cobc -x -O2 -o binarytrees.cobol_run binarytrees.cob

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./binarytrees.cobol_run 21" COBOL binary-trees

run:
	./binarytrees.cobol_run 21

mem:
	/usr/bin/time -v ./binarytrees.cobol_run 21

valgrind:
	valgrind --tool=massif --stacks=yes ./binarytrees.cobol_run 21

clean:
	rm -f binarytrees.cobol_run
