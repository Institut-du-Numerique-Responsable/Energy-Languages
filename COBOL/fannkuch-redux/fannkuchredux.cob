      >>SOURCE FORMAT FREE
*> The Computer Language Benchmarks Game: fannkuch-redux
*> COBOL (GnuCOBOL) port by the Institut du Numerique Responsable,
*> following the sequential reference algorithm (single thread).
IDENTIFICATION DIVISION.
PROGRAM-ID. fannkuchredux.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 ARG-TEXT          PIC X(20).
01 N                 PIC S9(4) COMP-5.
01 R                 PIC S9(4) COMP-5.
01 I                 PIC S9(4) COMP-5.
01 LO                PIC S9(4) COMP-5.
01 HI                PIC S9(4) COMP-5.
01 K                 PIC S9(4) COMP-5.
01 TMP               PIC S9(4) COMP-5.
01 PERM0             PIC S9(4) COMP-5.
01 FLIPS             PIC S9(9) COMP-5.
01 MAX-FLIPS         PIC S9(9) COMP-5 VALUE 0.
01 CHECKSUM          PIC S9(18) COMP-5 VALUE 0.
01 PERM-COUNT        PIC S9(18) COMP-5 VALUE 0.
01 DONE-FLAG         PIC 9 VALUE 0.
   88 DONE           VALUE 1.
01 NEXT-FLAG         PIC 9 VALUE 0.
   88 NEXT-FOUND     VALUE 1.
01 TABLES.
   05 PERM1          PIC S9(4) COMP-5 OCCURS 16 TIMES.
   05 PERM           PIC S9(4) COMP-5 OCCURS 16 TIMES.
   05 CNT            PIC S9(4) COMP-5 OCCURS 16 TIMES.
01 OUT-NUM           PIC -(18)9.

PROCEDURE DIVISION.
MAIN-PARA.
    ACCEPT ARG-TEXT FROM ARGUMENT-VALUE
    MOVE 7 TO N
    IF ARG-TEXT NOT = SPACES
        COMPUTE N = FUNCTION NUMVAL(ARG-TEXT)
    END-IF
    IF N < 1 OR N > 16
        DISPLAY "n must be between 1 and 16" UPON SYSERR
        MOVE 1 TO RETURN-CODE
        STOP RUN
    END-IF
    *> PERM1(i) holds the zero-based value at position i - 1.
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE PERM1(I) = I - 1
    END-PERFORM
    MOVE N TO R
    PERFORM UNTIL DONE
        PERFORM UNTIL R = 1
            MOVE R TO CNT(R)
            SUBTRACT 1 FROM R
        END-PERFORM
        PERFORM COUNT-FLIPS
        IF FLIPS > MAX-FLIPS
            MOVE FLIPS TO MAX-FLIPS
        END-IF
        IF FUNCTION MOD(PERM-COUNT, 2) = 0
            ADD FLIPS TO CHECKSUM
        ELSE
            SUBTRACT FLIPS FROM CHECKSUM
        END-IF
        PERFORM NEXT-PERMUTATION
        ADD 1 TO PERM-COUNT
    END-PERFORM
    MOVE CHECKSUM TO OUT-NUM
    DISPLAY FUNCTION TRIM(OUT-NUM)
    MOVE N TO OUT-NUM
    DISPLAY "Pfannkuchen(" FUNCTION TRIM(OUT-NUM) ") = " NO ADVANCING
    MOVE MAX-FLIPS TO OUT-NUM
    DISPLAY FUNCTION TRIM(OUT-NUM)
    STOP RUN.

COUNT-FLIPS.
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE PERM1(I) TO PERM(I)
    END-PERFORM
    MOVE 0 TO FLIPS
    MOVE PERM(1) TO K
    PERFORM UNTIL K = 0
        *> Reverse the first K + 1 elements.
        MOVE 1 TO LO
        COMPUTE HI = K + 1
        PERFORM UNTIL LO >= HI
            MOVE PERM(LO) TO TMP
            MOVE PERM(HI) TO PERM(LO)
            MOVE TMP TO PERM(HI)
            ADD 1 TO LO
            SUBTRACT 1 FROM HI
        END-PERFORM
        ADD 1 TO FLIPS
        MOVE PERM(1) TO K
    END-PERFORM.

NEXT-PERMUTATION.
    MOVE 0 TO NEXT-FLAG
    PERFORM UNTIL NEXT-FOUND OR DONE
        IF R = N
            SET DONE TO TRUE
        ELSE
            *> Rotate the first R + 1 elements left by one.
            MOVE PERM1(1) TO PERM0
            PERFORM VARYING I FROM 1 BY 1 UNTIL I > R
                MOVE PERM1(I + 1) TO PERM1(I)
            END-PERFORM
            MOVE PERM0 TO PERM1(R + 1)
            SUBTRACT 1 FROM CNT(R + 1)
            IF CNT(R + 1) > 0
                SET NEXT-FOUND TO TRUE
            ELSE
                ADD 1 TO R
            END-IF
        END-IF
    END-PERFORM.
