#!/usr/bin/env python3
"""
File Organizer - Automatically organize files by type
Sorts files in a directory into categorized subdirectories based on file extensions.
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

# Define file categories and their extensions
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
    'Code': ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css', '.php', '.rb', '.go', '.rs', '.ts'],
    'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.app'],
    'Others': []  # Catch-all for unrecognized extensions
}

def get_category(file_extension):
    """Determine the category of a file based on its extension."""
    file_extension = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category
    return 'Others'

def organize_files(directory, dry_run=True):
    """
    Organize files in the specified directory by type.
    
    Args:
        directory (str): Path to the directory to organize
        dry_run (bool): If True, only show what would be done without moving files
    """
    directory = Path(directory).resolve()
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return
    
    # Statistics
    stats = defaultdict(int)
    files_to_move = []
    
    # Scan directory for files
    print(f"\n{'DRY RUN - ' if dry_run else ''}Scanning directory: {directory}\n")
    
    for item in directory.iterdir():
        # Skip directories and hidden files
        if item.is_dir() or item.name.startswith('.'):
            continue
        
        # Get file extension and category
        file_extension = item.suffix
        category = get_category(file_extension)
        
        # Prepare destination
        dest_folder = directory / category
        dest_path = dest_folder / item.name
        
        # Handle filename conflicts
        counter = 1
        original_dest = dest_path
        while dest_path.exists():
            stem = original_dest.stem
            suffix = original_dest.suffix
            dest_path = dest_folder / f"{stem}_{counter}{suffix}"
            counter += 1
        
        files_to_move.append((item, dest_path, category))
        stats[category] += 1
    
    if not files_to_move:
        print("No files to organize.")
        return
    
    # Display what will be done
    print(f"Found {len(files_to_move)} file(s) to organize:\n")
    for source, dest, category in files_to_move:
        print(f"  [{category:12}] {source.name}")
    
    print(f"\nSummary:")
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} file(s)")
    
    # Move files if not dry run
    if not dry_run:
        print(f"\nOrganizing files...")
        for source, dest, category in files_to_move:
            # Create category folder if it doesn't exist
            dest.parent.mkdir(exist_ok=True)
            
            try:
                shutil.move(str(source), str(dest))
                print(f"  ✓ Moved: {source.name} → {category}/")
            except Exception as e:
                print(f"  ✗ Error moving {source.name}: {e}")
        
        print(f"\n✓ Organization complete!")
    else:
        print(f"\n(This was a dry run. Use --execute to actually move files)")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Organize files in a directory by type',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            python file_organizer.py ~/Downloads
            python file_organizer.py ~/Downloads --execute
            python file_organizer.py /path/to/folder --execute
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to organize (default: current directory)'
    )
    
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually move files (default is dry run)'
    )
    
    args = parser.parse_args()
    
    organize_files(args.directory, dry_run=not args.execute)

if __name__ == '__main__':
    main()
