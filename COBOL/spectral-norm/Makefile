compile:
	cobc -x -O2 -o spectralnorm.cobol_run spectralnorm.cob

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "./spectralnorm.cobol_run 5500" COBOL spectral-norm

run:
	./spectralnorm.cobol_run 5500

mem:
	/usr/bin/time -v ./spectralnorm.cobol_run 5500

valgrind:
	valgrind --tool=massif --stacks=yes ./spectralnorm.cobol_run 5500

clean:
	rm -f spectralnorm.cobol_run
