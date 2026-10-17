      >>SOURCE FORMAT FREE
*> The Computer Language Benchmarks Game: mandelbrot
*> COBOL (GnuCOBOL) port by the Institut du Numerique Responsable,
*> following the sequential reference algorithm: 50 iterations, escape
*> when |z|^2 > 4, binary PBM (P4) output, eight pixels per byte.
IDENTIFICATION DIVISION.
PROGRAM-ID. mandelbrot.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 ARG-TEXT          PIC X(20).
01 N                 PIC S9(9) COMP-5.
01 X                 PIC S9(9) COMP-5.
01 Y                 PIC S9(9) COMP-5.
01 ITER              PIC S9(4) COMP-5.
01 BYTE-VALUE        PIC S9(4) COMP-5.
01 BIT-COUNT         PIC S9(4) COMP-5.
01 ROW-LEN           PIC S9(9) COMP-5.
01 ROW-POS           PIC S9(9) COMP-5.
01 CR                COMP-2.
01 CI                COMP-2.
01 ZR                COMP-2.
01 ZI                COMP-2.
01 TR                COMP-2.
01 TI                COMP-2.
01 SIZE-TEXT         PIC Z(8)9.
01 ROW-BUF           PIC X(4096).
01 ESCAPED           PIC 9.

PROCEDURE DIVISION.
MAIN-PARA.
    ACCEPT ARG-TEXT FROM ARGUMENT-VALUE
    MOVE 200 TO N
    IF ARG-TEXT NOT = SPACES
        COMPUTE N = FUNCTION NUMVAL(ARG-TEXT)
    END-IF
    IF N < 1 OR N > 32768
        DISPLAY "n must be between 1 and 32768" UPON SYSERR
        MOVE 1 TO RETURN-CODE
        STOP RUN
    END-IF
    MOVE N TO SIZE-TEXT
    DISPLAY "P4"
    DISPLAY FUNCTION TRIM(SIZE-TEXT) " " FUNCTION TRIM(SIZE-TEXT)
    COMPUTE ROW-LEN = (N + 7) / 8
    PERFORM VARYING Y FROM 0 BY 1 UNTIL Y >= N
        COMPUTE CI = 2.0 * Y / N - 1.0
        MOVE 0 TO BYTE-VALUE BIT-COUNT ROW-POS
        PERFORM VARYING X FROM 0 BY 1 UNTIL X >= N
            COMPUTE CR = 2.0 * X / N - 1.5
            MOVE 0 TO ZR ZI TR TI ESCAPED
            PERFORM VARYING ITER FROM 1 BY 1
                    UNTIL ITER > 50 OR ESCAPED = 1
                COMPUTE ZI = 2.0 * ZR * ZI + CI
                COMPUTE ZR = TR - TI + CR
                COMPUTE TR = ZR * ZR
                COMPUTE TI = ZI * ZI
                IF TR + TI > 4.0
                    MOVE 1 TO ESCAPED
                END-IF
            END-PERFORM
            COMPUTE BYTE-VALUE = BYTE-VALUE * 2
            IF ESCAPED = 0
                ADD 1 TO BYTE-VALUE
            END-IF
            ADD 1 TO BIT-COUNT
            IF BIT-COUNT = 8
                PERFORM EMIT-BYTE
            END-IF
        END-PERFORM
        IF BIT-COUNT > 0
            PERFORM UNTIL BIT-COUNT = 8
                COMPUTE BYTE-VALUE = BYTE-VALUE * 2
                ADD 1 TO BIT-COUNT
            END-PERFORM
            PERFORM EMIT-BYTE
        END-IF
        DISPLAY ROW-BUF(1:ROW-LEN) WITH NO ADVANCING
    END-PERFORM
    STOP RUN.

EMIT-BYTE.
    ADD 1 TO ROW-POS
    MOVE FUNCTION CHAR(BYTE-VALUE + 1) TO ROW-BUF(ROW-POS:1)
    MOVE 0 TO BYTE-VALUE BIT-COUNT.
