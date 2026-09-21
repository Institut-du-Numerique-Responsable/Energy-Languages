compile:
	/usr/bin/clang -pipe -Wall -O3 -march=native -D_FILE_OFFSET_BITS=64 -I/opt/homebrew/Cellar/apr/1.7.6/include/apr-1 binarytrees.gcc-3.c -o binarytrees.gcc-3.gcc_run -lapr-1 -lm

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./binarytrees.gcc-3.gcc_run 21" C binary-trees

run:
	./binarytrees.gcc-3.gcc_run 21

mem:
	/usr/bin/time -v ./binarytrees.gcc-3.gcc_run 21
