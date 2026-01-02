# Duplicate File Finder

A Python script that scans directories to find and manage duplicate files based on their content hash. Helps you reclaim disk space by identifying and optionally removing duplicate files.

## Features

- **Smart Detection** - Two-pass approach (size comparison first, then hash) for efficiency
- **Multiple Hash Algorithms** - Choose between MD5 (fast) or SHA-256 (secure)
- **Size Filtering** - Only scan files above a certain size threshold
- **Recursive Scanning** - Optional subdirectory traversal
- **Detailed Reports** - Shows file sizes, dates, and wasted disk space
- **Safe Deletion** - Interactive mode to choose which duplicates to keep
- **Progress Tracking** - Real-time progress updates during scanning

## How It Works

1. **First Pass**: Groups files by size (fast operation)
2. **Second Pass**: Only hashes files with matching sizes (efficient)
3. **Detection**: Identifies files with identical content hashes as duplicates
4. **Reporting**: Displays duplicate sets with detailed information
5. **Optional Cleanup**: Interactively delete duplicates while keeping originals

## Usage

### Basic Scanning

Find duplicates in a directory:

```bash
# Scan Downloads folder
python duplicate_finder.py ~/Downloads

# Scan current directory
python duplicate_finder.py .

# Scan specific folder
python duplicate_finder.py /path/to/folder
```

### Advanced Options

**Non-recursive scan** (only current directory, no subdirectories):
```bash
python duplicate_finder.py ~/Documents --no-recursive
```

**Filter by minimum file size** (useful for ignoring small files):
```bash
# Only scan files 1MB or larger
python duplicate_finder.py . --min-size 1048576

# Only scan files 10KB or larger
python duplicate_finder.py . --min-size 10240
```

**Choose hash algorithm**:
```bash
# Use MD5 (faster, default)
python duplicate_finder.py . --hash md5

# Use SHA-256 (more secure, slower)
python duplicate_finder.py . --hash sha256
```

**Interactive deletion mode**:
```bash
python duplicate_finder.py ~/Downloads --delete
```

**Combine multiple options**:
```bash
# Scan recursively, files >= 100KB, SHA-256, with deletion
python duplicate_finder.py ~/Documents --min-size 102400 --hash sha256 --delete
```

## Example Output

```
Scanning directory: /Users/username/Downloads
Recursive: True, Min size: 0.00 B, Hash: MD5

Found 247 files to analyze
Hashing 45 potential duplicates...

Progress: 45/45 files hashed

================================================================================
Found 3 set(s) of duplicates (8 files total)
================================================================================

Set 1:
  Hash: a3d5c8f91b2e7d4...
  Size: 2.45 MB each
  Wasted space: 4.90 MB
  Copies: 3
  Files:
    • /Users/username/Downloads/vacation.jpg
      Modified: 2025-12-15 14:23:10
    • /Users/username/Downloads/backup/vacation.jpg
      Modified: 2025-12-15 14:23:10
    • /Users/username/Downloads/old/vacation_copy.jpg
      Modified: 2025-12-20 09:15:42

Set 2:
  Hash: 7f3a9e2c4b8d1f6...
  Size: 156.00 KB each
  Wasted space: 156.00 KB
  Copies: 2
  Files:
    • /Users/username/Downloads/report.pdf
      Modified: 2025-11-30 16:45:22
    • /Users/username/Downloads/documents/report.pdf
      Modified: 2025-11-30 16:45:22

Set 3:
  Hash: 2c9f7e1a5d8b3c4...
  Size: 45.12 KB each
  Wasted space: 135.36 KB
  Copies: 4
  Files:
    • /Users/username/Downloads/icon.png
      Modified: 2025-10-05 11:20:33
    • /Users/username/Downloads/assets/icon.png
      Modified: 2025-10-05 11:20:33
    • /Users/username/Downloads/backup/icon.png
      Modified: 2025-10-05 11:20:33
    • /Users/username/Downloads/temp/icon_copy.png
      Modified: 2025-10-12 14:08:15

================================================================================
Total wasted space: 5.19 MB
================================================================================
```

## Interactive Deletion Mode

When using `--delete`, the script will guide you through each duplicate set:

```
Interactive Deletion Mode
You'll be asked which files to keep from each duplicate set.

Set 1/3:
  Size: 2.45 MB
  [1] /Users/username/Downloads/vacation.jpg
      Modified: 2025-12-15 14:23:10
  [2] /Users/username/Downloads/backup/vacation.jpg
      Modified: 2025-12-15 14:23:10
  [3] /Users/username/Downloads/old/vacation_copy.jpg
      Modified: 2025-12-20 09:15:42

Keep file [1-3] or [s]kip this set or [q]uit: 1

Will delete 2 file(s):
  • /Users/username/Downloads/backup/vacation.jpg
  • /Users/username/Downloads/old/vacation_copy.jpg

Confirm deletion? [y/N]: y
  ✓ Deleted: /Users/username/Downloads/backup/vacation.jpg
  ✓ Deleted: /Users/username/Downloads/old/vacation_copy.jpg
```

## Command-Line Options

```
positional arguments:
  directory             Directory to scan (default: current directory)

optional arguments:
  -h, --help            Show help message and exit
  --no-recursive        Do not scan subdirectories
  --min-size BYTES      Minimum file size in bytes to consider (default: 0)
  --hash {md5,sha256}   Hash algorithm to use (default: md5)
  --delete              Interactively delete duplicate files
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Use Cases

- **Clean up Downloads folder** - Remove duplicate downloads
- **Photo library cleanup** - Find duplicate images across folders
- **Backup verification** - Identify redundant backup files
- **Disk space recovery** - Free up space by removing duplicates
- **File organization** - Find scattered copies of the same file

## Performance Tips

1. **Use `--min-size`** to skip small files (config files, etc.)
2. **Use MD5** for faster scanning of large directories
3. **Use `--no-recursive`** if you only need to check one folder
4. **Start with dry run** (without `--delete`) to see what you have

## Safety Notes

- The script only deletes files when you use `--delete` flag
- You must confirm each deletion interactively
- You choose which file to keep from each duplicate set
- The script shows modification dates to help you decide
- You can skip sets or quit anytime during deletion

## Common File Size Values

For the `--min-size` option:

- 1 KB = 1024 bytes
- 10 KB = 10240 bytes
- 100 KB = 102400 bytes
- 1 MB = 1048576 bytes
- 10 MB = 10485760 bytes
- 100 MB = 104857600 bytes

## License

This script is part of the Daily Python Scripts collection and is licensed under the MIT License. See the [LICENSE](../LICENSE) file in the root directory for details.
