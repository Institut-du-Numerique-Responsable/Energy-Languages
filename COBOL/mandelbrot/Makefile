compile:
	cobc -x -O2 -o mandelbrot.cobol_run mandelbrot.cob

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./mandelbrot.cobol_run 16000" COBOL mandelbrot

run:
	./mandelbrot.cobol_run 16000

mem:
	/usr/bin/time -v ./mandelbrot.cobol_run 16000

valgrind:
	valgrind --tool=massif --stacks=yes ./mandelbrot.cobol_run 16000

clean:
	rm -f mandelbrot.cobol_run
