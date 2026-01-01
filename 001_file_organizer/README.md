# File Organizer

A Python script that automatically organizes files in a directory by categorizing them based on their file extensions.

## Features

- Organizes files into 8 categories: Images, Documents, Videos, Audio, Archives, Code, Executables, and Others
- Safe dry-run mode by default (preview changes before executing)
- Automatically handles filename conflicts
- Skips hidden files and existing directories
- Provides detailed summary of operations

## Categories

| Category | File Extensions |
|----------|----------------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico, .tiff |
| **Documents** | .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx, .csv |
| **Videos** | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v |
| **Audio** | .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a |
| **Archives** | .zip, .rar, .7z, .tar, .gz, .bz2, .xz |
| **Code** | .py, .js, .java, .cpp, .c, .html, .css, .php, .rb, .go, .rs, .ts |
| **Executables** | .exe, .msi, .dmg, .pkg, .deb, .rpm, .app |
| **Others** | Any unrecognized file type |

## Usage

### Dry Run (Preview Mode)

See what would happen without actually moving files:

```bash
# Preview organization of Downloads folder
python file_organizer.py ~/Downloads

# Preview organization of current directory
python file_organizer.py .

# Preview organization of specific folder
python file_organizer.py /path/to/messy/folder
```

### Execute Mode

Actually organize the files:

```bash
# Organize Downloads folder
python file_organizer.py ~/Downloads --execute

# Organize current directory
python file_organizer.py . --execute

# Organize specific folder
python file_organizer.py /path/to/messy/folder --execute
```

## Example Output

```
DRY RUN - Scanning directory: /Users/username/Downloads

Found 15 file(s) to organize:

  [Images     ] vacation.jpg
  [Images     ] screenshot.png
  [Documents  ] report.pdf
  [Documents  ] notes.txt
  [Videos     ] tutorial.mp4
  [Code       ] script.py
  [Archives   ] backup.zip
  ...

Summary:
  Archives: 2 file(s)
  Code: 3 file(s)
  Documents: 4 file(s)
  Images: 3 file(s)
  Videos: 3 file(s)

(This was a dry run. Use --execute to actually move files)
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Customization

You can easily customize the categories by editing the `FILE_CATEGORIES` dictionary in the script:

```python
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', ...],
    'Documents': ['.pdf', '.doc', '.docx', ...],
    # Add categories here
    'MyCustomCategory': ['.custom', '.ext'],
}
```

## Safety Features

- **Dry run by default**: Always shows preview before making changes
- **Conflict resolution**: Automatically renames files if destination already exists
- **Skips system files**: Ignores hidden files and existing directories
- **Error handling**: Continues execution even if individual files fail to move

## Notes

- The script creates category folders only if there are files to move into them
- Original files remain untouched in dry-run mode
- Always review the dry-run output before using `--execute`

## License

This script is part of the Daily Python Scripts collection and is licensed under the MIT License. See the [LICENSE](../LICENSE) file in the root directory for details.
