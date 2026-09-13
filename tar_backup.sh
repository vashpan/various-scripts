#!/usr/bin/env fish

# Creates an uncompressed tar archive from an input directory
# and writes it to the specified output path.
#
# Shows transfer progress, speed, percentage, and ETA using pv.
#
# Usage:
#   ./tar_backup.sh <input-folder> <output.tar>
#
# Example:
#   ./tar_backup.sh ~/Documents ~/Desktop/documents.tar
#
# Requirements:
#   fish
#   pv

if test (count $argv) -ne 2
    echo "Usage: "(status filename)" <input-folder> <output.tar>"
    exit 1
end

if not test -d "$argv[1]"
    echo "Error: Input folder does not exist: $argv[1]" >&2
    exit 1
end

if not type -q pv
    echo "Error: pv is required. Install it with: brew install pv" >&2
    exit 1
end

set input_dir (realpath "$argv[1]")

set output_dir (dirname "$argv[2]")
set output_name (basename "$argv[2]")

if not test -d "$output_dir"
    echo "Error: Output directory does not exist: $output_dir" >&2
    exit 1
end

set output_dir (realpath "$output_dir")
set output_file "$output_dir/$output_name"

set parent_dir (dirname "$input_dir")
set folder_name (basename "$input_dir")

set size (du -sk "$input_dir" | awk '{print $1 * 1024}')

tar -C "$parent_dir" -cf - "$folder_name" \
    | pv -s $size \
    > "$output_file"