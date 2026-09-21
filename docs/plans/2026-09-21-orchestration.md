# Remaining orchestration priorities

Scope: medium-priority audit findings; do not invent unavailable benchmark implementations or alter existing measurement recipes.

1. Add integration tests for failure propagation for all actions, Python 3 language entry points, directories containing spaces/metacharacters, missing targets, and no-execution inventory.
2. Implement one root Python 3 runner; delegate the four legacy entry points to it. Use subprocess argument lists and cwd, stream command output, prune build/dependency/internal directories, and report aggregate failures. Add --root, --check and measurement delay control.
3. Test and fix input generation from the actual FASTA source, independent of current directory. Generate into a temporary directory before replacing outputs; reuse the identical nucleotide dataset. Preserve default sizes and allow small sizes for tests.
4. Update README/changelog/limitations and CI labels. Run integration tests, inventory actual Makefiles, and request independent review before committing and pushing the continued fixes.

Acceptance: failed or unsupported operations return nonzero; available operations continue and are summarized; checks never execute benchmark recipes; input-generation failures preserve existing datasets; all prior runner tests continue passing. No real RAPL validation claimed.
