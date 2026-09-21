#!/bin/bash
set -euo pipefail

if [[ $# -gt 2 ]]; then
    echo "Usage: bash gen-input.sh [nucleotide-size [regex-size]]" >&2
    exit 1
fi
nucleotide_size=${1:-25000000}
regex_size=${2:-5000000}
if [[ ! $nucleotide_size =~ ^[1-9][0-9]*$ || ! $regex_size =~ ^[1-9][0-9]*$ ]]; then
    echo "Input sizes must be positive integers." >&2
    exit 1
fi

project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
python_command=${PYTHON:-python3}
source_file="$project_dir/Python/fasta/fasta.python3-3.python3"
# Stage all data first; a failed generator must not truncate existing inputs.
staging_dir=$(mktemp -d "$project_dir/.inputs.XXXXXX")
trap 'rm -rf -- "$staging_dir"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

nucleotide_file="knucleotide-input${nucleotide_size}.txt"
reverse_file="revcomp-input${nucleotide_size}.txt"
regex_file="regexredux-input${regex_size}.txt"
echo "Generating k-nucleotide and reverse-complement inputs (n=$nucleotide_size)"
"$python_command" "$source_file" "$nucleotide_size" > "$staging_dir/$nucleotide_file"
cp -- "$staging_dir/$nucleotide_file" "$staging_dir/$reverse_file"
echo "Generating regex-redux input (n=$regex_size)"
"$python_command" "$source_file" "$regex_size" > "$staging_dir/$regex_file"

for filename in "$nucleotide_file" "$reverse_file" "$regex_file"; do
    mv -f -- "$staging_dir/$filename" "$project_dir/$filename"
done
echo "Input files ready in $project_dir"
