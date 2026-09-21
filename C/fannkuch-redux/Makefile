compile:
	/usr/bin/clang -pipe -Wall -O3 -march=native -std=c99 fannkuchredux.gcc-5.c -o fannkuchredux.gcc-5.gcc_run

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./fannkuchredux.gcc-5.gcc_run 12" C fannkuch-redux

run:
	./fannkuchredux.gcc-5.gcc_run 12

mem:
	/usr/bin/time -v ./fannkuchredux.gcc-5.gcc_run 12
