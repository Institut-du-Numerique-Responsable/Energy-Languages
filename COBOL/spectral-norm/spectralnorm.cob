      >>SOURCE FORMAT FREE
*> The Computer Language Benchmarks Game: spectral-norm
*> COBOL (GnuCOBOL) port by the Institut du Numerique Responsable,
*> following the sequential reference algorithm.
IDENTIFICATION DIVISION.
PROGRAM-ID. spectralnorm.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 ARG-TEXT          PIC X(20).
01 N                 PIC S9(9) COMP-5.
01 I                 PIC S9(9) COMP-5.
01 J                 PIC S9(9) COMP-5.
01 ITER              PIC S9(4) COMP-5.
01 IJ                PIC S9(18) COMP-5.
01 DENOM             PIC S9(18) COMP-5.
01 PARTIAL           COMP-2.
01 VBV               COMP-2.
01 VV                COMP-2.
01 RESULT            COMP-2.
01 RESULT-OUT        PIC 9.9(9).
01 VECTORS.
   05 U              COMP-2 OCCURS 10000 TIMES.
   05 V              COMP-2 OCCURS 10000 TIMES.
   05 W              COMP-2 OCCURS 10000 TIMES.

PROCEDURE DIVISION.
MAIN-PARA.
    ACCEPT ARG-TEXT FROM ARGUMENT-VALUE
    MOVE 100 TO N
    IF ARG-TEXT NOT = SPACES
        COMPUTE N = FUNCTION NUMVAL(ARG-TEXT)
    END-IF
    IF N < 1 OR N > 10000
        DISPLAY "n must be between 1 and 10000" UPON SYSERR
        MOVE 1 TO RETURN-CODE
        STOP RUN
    END-IF
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE 1 TO U(I)
    END-PERFORM
    PERFORM VARYING ITER FROM 1 BY 1 UNTIL ITER > 10
        PERFORM ATA-TIMES-U
        PERFORM ATA-TIMES-V
    END-PERFORM
    MOVE 0 TO VBV VV
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE VBV = VBV + U(I) * V(I)
        COMPUTE VV = VV + V(I) * V(I)
    END-PERFORM
    COMPUTE RESULT = FUNCTION SQRT(VBV / VV)
    COMPUTE RESULT-OUT ROUNDED = RESULT
    DISPLAY RESULT-OUT
    STOP RUN.

*> A(i, j) = 1 / ((i + j)(i + j + 1) / 2 + i + 1) with zero-based i, j.
*> The integer denominator is computed exactly before one division.

*> V = At (A U), using W as the intermediate vector.
ATA-TIMES-U.
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE 0 TO PARTIAL
        PERFORM VARYING J FROM 1 BY 1 UNTIL J > N
            COMPUTE IJ = I + J - 2
            COMPUTE DENOM = IJ * (IJ + 1) / 2 + I
            COMPUTE PARTIAL = PARTIAL + U(J) / DENOM
        END-PERFORM
        MOVE PARTIAL TO W(I)
    END-PERFORM
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE 0 TO PARTIAL
        PERFORM VARYING J FROM 1 BY 1 UNTIL J > N
            COMPUTE IJ = I + J - 2
            COMPUTE DENOM = IJ * (IJ + 1) / 2 + J
            COMPUTE PARTIAL = PARTIAL + W(J) / DENOM
        END-PERFORM
        MOVE PARTIAL TO V(I)
    END-PERFORM.

*> U = At (A V), using W as the intermediate vector.
ATA-TIMES-V.
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE 0 TO PARTIAL
        PERFORM VARYING J FROM 1 BY 1 UNTIL J > N
            COMPUTE IJ = I + J - 2
            COMPUTE DENOM = IJ * (IJ + 1) / 2 + I
            COMPUTE PARTIAL = PARTIAL + V(J) / DENOM
        END-PERFORM
        MOVE PARTIAL TO W(I)
    END-PERFORM
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE 0 TO PARTIAL
        PERFORM VARYING J FROM 1 BY 1 UNTIL J > N
            COMPUTE IJ = I + J - 2
            COMPUTE DENOM = IJ * (IJ + 1) / 2 + J
            COMPUTE PARTIAL = PARTIAL + W(J) / DENOM
        END-PERFORM
        MOVE PARTIAL TO U(I)
    END-PERFORM.
