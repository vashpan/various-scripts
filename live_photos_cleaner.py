#!/usr/bin/env python3
"""
script to remove live-photo .mov files exported from Photos app

this script recursively walks through a given folder and deletes any .mov file
that has a corresponding picture file (same base name but different extension).
it lists the files along with their human-readable size (e.g. 2k instead of 2048 bytes)
and shows the total space saved by removing these files.
use the --dry flag to only list the files without deleting them.
"""

import os
import argparse

def human_readable_size(num):
    # convert size in bytes to human readable format using 1024 as factor
    if num < 1024:
        return f"{num}B"
    elif num < 1024**2:
        return f"{num // 1024}k"
    elif num < 1024**3:
        return f"{num // 1024**2}M"
    else:
        return f"{num // 1024**3}G"

def main():
    parser = argparse.ArgumentParser(
        description='remove live-photo .mov files exported from Photos app'
    )
    parser.add_argument('folder', help='folder to scan')
    parser.add_argument('--dry', action='store_true', help='dry run (only list files to delete)')
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"folder '{args.folder}' does not exist")
        exit(1)

    total_size_saved = 0

    for root, dirs, files in os.walk(args.folder):
        for f in files:
            if f.lower().endswith('.mov'):
                base, ext = os.path.splitext(f)
                # check for a corresponding picture file with the same base name and different extension
                found_picture = any(
                    (other != f and os.path.splitext(other)[0] == base)
                    for other in files
                )
                if found_picture:
                    file_path = os.path.join(root, f)
                    try:
                        size = os.path.getsize(file_path)
                    except Exception as e:
                        print(f"error getting size for {file_path}: {e}")
                        continue
                    total_size_saved += size
                    print(f"deleting {file_path} ({human_readable_size(size)})")
                    if not args.dry:
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"error deleting {file_path}: {e}")

    print(f"\nTotal space saved: {human_readable_size(total_size_saved)}")

if __name__ == '__main__':
    main()