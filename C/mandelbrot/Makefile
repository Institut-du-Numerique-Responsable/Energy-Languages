compile:
	/usr/bin/clang -pipe -Wall -O3 -march=native -mno-fma -fno-finite-math-only -mfpmath=sse -msse2 mandelbrot.gcc-6.c -o mandelbrot.gcc-6.gcc_run

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./mandelbrot.gcc-6.gcc_run 16000" C mandelbrot

run:
	./mandelbrot.gcc-6.gcc_run 16000

mem:
	/usr/bin/time -v ./mandelbrot.gcc-6.gcc_run 16000
