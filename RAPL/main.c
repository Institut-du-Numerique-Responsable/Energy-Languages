#define _POSIX_C_SOURCE 200809L
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/wait.h>
#include "rapl.h"

/* Keep language names compatible with C++, CSharp and Java-GraalVM. */
static int valid_language(const char *name)
{
    if (!*name) return 0;
    for (; *name; name++)
        if (!isalnum((unsigned char)*name) && !strchr("_+-", *name)) return 0;
    return 1;
}

int main(int argc, char **argv)
{
    char path[500];
    FILE *output = NULL, *sample = NULL;
    int result = EXIT_FAILURE;
    const int core = 0, repetitions = 10;

    if (argc != 4 || !argv[1][0] || !valid_language(argv[2]) ||
        !argv[3][0] || strpbrk(argv[3], "\r\n;,")) {
        fprintf(stderr, "Usage: %s \"command\" language benchmark\n", argv[0]);
        return EXIT_FAILURE;
    }
    int length = snprintf(path, sizeof path, "../%s.csv", argv[2]);
    if (length < 0 || (size_t)length >= sizeof path) {
        fprintf(stderr, "Language name is too long.\n");
        return EXIT_FAILURE;
    }
    output = fopen(path, "a");
    if (!output) {
        perror(path);
        return EXIT_FAILURE;
    }
    if (rapl_init(core) != 0) {
        fprintf(stderr, "RAPL initialization failed.\n");
        goto cleanup;
    }

    for (int i = 0; i < repetitions; i++) {
        struct timespec before, after;
        /* Stage the row so a command or sensor failure cannot append it. */
        sample = tmpfile();
        if (!sample) { perror("tmpfile"); goto cleanup; }
        if (clock_gettime(CLOCK_MONOTONIC, &before) != 0) {
            perror("clock_gettime"); goto cleanup;
        }
        rapl_before(sample, core);
        int status = system(argv[1]);
        if (status == -1) {
            perror("system"); goto cleanup;
        }
        if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
            result = WIFEXITED(status) ? WEXITSTATUS(status) : EXIT_FAILURE;
            fprintf(stderr, "Benchmark failed at repetition %d (status %d); sample discarded.\n",
                    i + 1, status);
            goto cleanup;
        }
        rapl_after(sample, core);
        if (clock_gettime(CLOCK_MONOTONIC, &after) != 0) {
            perror("clock_gettime"); goto cleanup;
        }
        double milliseconds = (after.tv_sec - before.tv_sec) * 1000.0 +
                              (after.tv_nsec - before.tv_nsec) / 1000000.0;
        if (fprintf(sample, " %G \n", milliseconds) < 0 ||
            fflush(sample) != 0 || fseek(sample, 0, SEEK_SET) != 0) {
            perror("sample output"); goto cleanup;
        }
        if (fprintf(output, "%s ; ", argv[3]) < 0) {
            perror("CSV output"); goto cleanup;
        }
        char buffer[1024];
        size_t count;
        while ((count = fread(buffer, 1, sizeof buffer, sample)) > 0) {
            if (fwrite(buffer, 1, count, output) != count) {
                perror("CSV output"); goto cleanup;
            }
        }
        if (ferror(sample) || fflush(output) != 0) {
            perror("CSV output"); goto cleanup;
        }
        fclose(sample);
        sample = NULL;
    }
    result = EXIT_SUCCESS;

cleanup:
    if (sample) fclose(sample);
    if (fclose(output) != 0) {
        perror("CSV close");
        result = EXIT_FAILURE;
    }
    return result;
}
