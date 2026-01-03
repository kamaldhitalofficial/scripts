#!/usr/bin/env python3
"""
Duplicate File Finder - Find and manage duplicate files in directories
Scans directories for duplicate files based on content hash and provides options to manage them.
"""

import os
import hashlib
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def get_file_hash(filepath, hash_algo='md5', chunk_size=8192):
    """
    Calculate hash of a file.
    
    Args:
        filepath: Path to the file
        hash_algo: Hash algorithm to use ('md5' or 'sha256')
        chunk_size: Size of chunks to read (in bytes)
    
    Returns:
        Hash string of the file
    """
    hash_func = hashlib.md5() if hash_algo == 'md5' else hashlib.sha256()
    
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except (IOError, OSError) as e:
        print(f"  ✗ Error reading {filepath}: {e}")
        return None

def format_size(size_bytes):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def get_file_info(filepath):
    """Get file size and modification time."""
    try:
        stat = os.stat(filepath)
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
    except OSError:
        return {'size': 0, 'modified': 'Unknown'}

def find_duplicates(directory, recursive=True, min_size=0, hash_algo='md5'):
    """
    Find duplicate files in a directory.
    
    Args:
        directory: Directory to scan
        recursive: Whether to scan subdirectories
        min_size: Minimum file size in bytes to consider
        hash_algo: Hash algorithm to use
    
    Returns:
        Dictionary mapping hash to list of duplicate file paths
    """
    directory = Path(directory).resolve()
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return {}
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return {}
    
    print(f"\nScanning directory: {directory}")
    print(f"   Recursive: {recursive}, Min size: {format_size(min_size)}, Hash: {hash_algo.upper()}\n")
    
    # First pass: group files by size (faster than hashing everything)
    size_map = defaultdict(list)
    file_count = 0
    
    pattern = '**/*' if recursive else '*'
    for filepath in directory.glob(pattern):
        if filepath.is_file():
            try:
                file_size = filepath.stat().st_size
                if file_size >= min_size:
                    size_map[file_size].append(filepath)
                    file_count += 1
            except OSError:
                continue
    
    print(f"Found {file_count} files to analyze")
    
    # Second pass: hash files with same size
    hash_map = defaultdict(list)
    files_to_hash = sum(len(files) for files in size_map.values() if len(files) > 1)
    
    if files_to_hash == 0:
        print("✓ No potential duplicates found (all files have unique sizes)")
        return {}
    
    print(f"Hashing {files_to_hash} potential duplicates...\n")
    
    hashed = 0
    for size, filepaths in size_map.items():
        if len(filepaths) > 1:  # Only hash files with same size
            for filepath in filepaths:
                file_hash = get_file_hash(filepath, hash_algo)
                if file_hash:
                    hash_map[file_hash].append(filepath)
                    hashed += 1
                    if hashed % 50 == 0:
                        print(f"  Progress: {hashed}/{files_to_hash} files hashed")
    
    # Filter to only keep actual duplicates (hash appears more than once)
    duplicates = {h: files for h, files in hash_map.items() if len(files) > 1}
    
    return duplicates

def display_duplicates(duplicates):
    """Display found duplicates in a formatted way."""
    if not duplicates:
        print("\n✓ No duplicate files found!")
        return
    
    total_sets = len(duplicates)
    total_files = sum(len(files) for files in duplicates.values())
    total_wasted = 0
    
    print(f"\n{'='*80}")
    print(f"Found {total_sets} set(s) of duplicates ({total_files} files total)")
    print(f"{'='*80}\n")
    
    for idx, (file_hash, filepaths) in enumerate(duplicates.items(), 1):
        file_info = get_file_info(filepaths[0])
        file_size = file_info['size']
        wasted_space = file_size * (len(filepaths) - 1)
        total_wasted += wasted_space
        
        print(f"Set {idx}:")
        print(f"  Hash: {file_hash[:16]}...")
        print(f"  Size: {format_size(file_size)} each")
        print(f"  Wasted space: {format_size(wasted_space)}")
        print(f"  Copies: {len(filepaths)}")
        print(f"  Files:")
        
        for filepath in filepaths:
            info = get_file_info(filepath)
            print(f"    • {filepath}")
            print(f"      Modified: {info['modified']}")
        
        print()
    
    print(f"{'='*80}")
    print(f"Total wasted space: {format_size(total_wasted)}")
    print(f"{'='*80}\n")

def interactive_delete(duplicates):
    """Interactively delete duplicate files."""
    if not duplicates:
        return
    
    print("\nInteractive Deletion Mode")
    print("You'll be asked which files to keep from each duplicate set.\n")
    
    for idx, (file_hash, filepaths) in enumerate(duplicates.items(), 1):
        print(f"\nSet {idx}/{len(duplicates)}:")
        print(f"  Size: {format_size(get_file_info(filepaths[0])['size'])}")
        
        for i, filepath in enumerate(filepaths, 1):
            info = get_file_info(filepath)
            print(f"  [{i}] {filepath}")
            print(f"      Modified: {info['modified']}")
        
        while True:
            choice = input(f"\nKeep file [1-{len(filepaths)}] or [s]kip this set or [q]uit: ").strip().lower()
            
            if choice == 'q':
                print("Deletion cancelled.")
                return
            
            if choice == 's':
                print("Skipping this set.")
                break
            
            try:
                keep_idx = int(choice) - 1
                if 0 <= keep_idx < len(filepaths):
                    files_to_delete = [f for i, f in enumerate(filepaths) if i != keep_idx]
                    
                    print(f"\nWill delete {len(files_to_delete)} file(s):")
                    for f in files_to_delete:
                        print(f"  • {f}")
                    
                    confirm = input("Confirm deletion? [y/N]: ").strip().lower()
                    if confirm == 'y':
                        for f in files_to_delete:
                            try:
                                os.remove(f)
                                print(f"  ✓ Deleted: {f}")
                            except OSError as e:
                                print(f"  ✗ Error deleting {f}: {e}")
                    else:
                        print("Deletion cancelled for this set.")
                    break
                else:
                    print(f"Invalid choice. Enter 1-{len(filepaths)}")
            except ValueError:
                print(f"Invalid input. Enter 1-{len(filepaths)}, 's', or 'q'")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Find and manage duplicate files in directories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python duplicate_finder.py ~/Downloads                    # Find duplicates
  python duplicate_finder.py ~/Documents --no-recursive      # Non-recursive scan
  python duplicate_finder.py . --min-size 1048576           # Files >= 1MB only
  python duplicate_finder.py . --delete                      # Interactive deletion
  python duplicate_finder.py . --hash sha256                # Use SHA-256 hash
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to scan (default: current directory)'
    )
    
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Do not scan subdirectories'
    )
    
    parser.add_argument(
        '--min-size',
        type=int,
        default=0,
        help='Minimum file size in bytes to consider (default: 0)'
    )
    
    parser.add_argument(
        '--hash',
        choices=['md5', 'sha256'],
        default='md5',
        help='Hash algorithm to use (default: md5)'
    )
    
    parser.add_argument(
        '--delete',
        action='store_true',
        help='Interactively delete duplicate files'
    )
    
    args = parser.parse_args()
    
    duplicates = find_duplicates(
        args.directory,
        recursive=not args.no_recursive,
        min_size=args.min_size,
        hash_algo=args.hash
    )
    
    display_duplicates(duplicates)
    
    if args.delete and duplicates:
        interactive_delete(duplicates)

if __name__ == '__main__':
    main()
