# Password Generator

A secure Python script to generate strong, customizable passwords and memorable passphrases. Uses cryptographically secure random generation and provides strength assessment.

## Features

- **Cryptographically Secure** - Uses Python's `secrets` module for true randomness
- **Highly Customizable** - Control length, character types, and format
- **Passphrase Support** - Generate memorable word-based passphrases
- **Strength Assessment** - Real-time entropy calculation and strength rating
- **Clipboard Support** - Copy passwords directly (cross-platform)
- **Ambiguous Character Filter** - Avoid confusing characters like 0/O, 1/l/I
- **Batch Generation** - Create multiple passwords at once
- **Guaranteed Variety** - Ensures at least one character from each enabled type

## Installation

No external dependencies required for basic usage! Uses Python standard library.

**Optional:** For better clipboard support, install:
```bash
pip install pyperclip
```

## Usage

### Basic Password Generation

```bash
# Generate default 16-character password
python password_generator.py

# Output:
#   X7$mK9pL#nR2qW5v
#   Strength: Strong (89.2 bits of entropy)
#   Very secure
```

### Custom Length

```bash
# 20-character password
python password_generator.py -l 20

# 12-character password
python password_generator.py -l 12
```

### Character Type Options

```bash
# No special symbols (alphanumeric only)
python password_generator.py --no-symbols

# No uppercase letters
python password_generator.py --no-uppercase

# No digits
python password_generator.py --no-digits

# Only lowercase and digits
python password_generator.py --no-uppercase --no-symbols
```

### Exclude Ambiguous Characters

Avoid characters that look similar (useful for handwriting or reading aloud):

```bash
# Excludes: i, l, 1, L, o, 0, O
python password_generator.py --no-ambiguous
```

### Multiple Passwords

```bash
# Generate 5 passwords
python password_generator.py -n 5

# Output:
#   Password 1:
#     X7$mK9pL#nR2qW5v
#     Strength: Strong (89.2 bits of entropy)
#     Very secure
#
#   Password 2:
#     aB3$xY9#mN7pQ2wE
#     Strength: Strong (89.2 bits of entropy)
#     Very secure
#   ...
```

### Passphrase Generation

Generate memorable word-based passphrases:

```bash
# Default 4-word passphrase
python password_generator.py --passphrase

# Output:
#   dragon-summer-crystal-falcon-73
#   Strength: Good (97.4 bits of entropy)
#   Reasonably secure

# 6-word passphrase
python password_generator.py --passphrase -w 6

# Custom separator
python password_generator.py --passphrase --separator _

# Capitalize words
python password_generator.py --passphrase --capitalize

# Output:
#   Golden-Phoenix-Mountain-Ocean-42
```

### Clipboard Support

```bash
# Copy to clipboard
python password_generator.py -l 20 --copy

# Output:
#   kN9$pX7mL#2qR5wB8vY3
#   Strength: Excellent (111.5 bits of entropy)
#   Extremely secure
#
#   ✓ Copied to clipboard!
```

### Hide Strength Assessment

```bash
# Just show the password
python password_generator.py --no-strength

# Output:
#   X7$mK9pL#nR2qW5v
```

## Command-Line Options

```
positional arguments:
  None

optional arguments:
  -h, --help            Show help message and exit
  -l LENGTH, --length LENGTH
                        Password length (default: 16)
  -n COUNT, --count COUNT
                        Number of passwords to generate (default: 1)
  --no-uppercase        Exclude uppercase letters
  --no-lowercase        Exclude lowercase letters
  --no-digits           Exclude numbers
  --no-symbols          Exclude special characters
  --no-ambiguous        Exclude ambiguous characters (i, l, 1, L, o, 0, O)
  --passphrase          Generate a passphrase instead of a password
  -w WORDS, --words WORDS
                        Number of words in passphrase (default: 4)
  --separator SEPARATOR
                        Separator for passphrase words (default: -)
  --capitalize          Capitalize words in passphrase
  --copy                Copy first generated password to clipboard
  --no-strength         Do not show strength assessment
```

## Password Strength Guide

The script calculates entropy and assesses password strength:

| Strength | Entropy | Description | Recommendation |
|----------|---------|-------------|----------------|
| **Weak** | < 28 bits | Easy to crack | Not recommended |
| **Fair** | 28-36 bits | Could be stronger | Use with caution |
| **Good** | 36-60 bits | Reasonably secure | Acceptable for most uses |
| **Strong** | 60-80 bits | Very secure | Recommended |
| **Excellent** | > 80 bits | Extremely secure | Best for sensitive accounts |

### Entropy Explanation

Entropy measures password unpredictability in bits. Higher is better:
- **40 bits** = 1 trillion possibilities
- **60 bits** = 1 quintillion possibilities  
- **80 bits** = 1.2 septillion possibilities

## Use Cases

### Random Passwords
- **Online accounts** - Social media, email, shopping sites
- **WiFi passwords** - Secure your home network
- **API keys** - Service authentication tokens
- **Database credentials** - Secure database access
- **Encrypted files** - Archive and document protection

### Passphrases
- **Master passwords** - Password manager master keys
- **Disk encryption** - BitLocker, FileVault, LUKS
- **SSH keys** - Key passphrase protection
- **Memorable but secure** - Easier to type and remember
- **Voice dictation** - Easier to communicate

## Security Best Practices

**Do:**
- Use unique passwords for each account
- Use a password manager to store them
- Generate passwords with at least 16 characters
- Include all character types (upper, lower, digits, symbols)
- Use passphrases for passwords you need to remember
- Change passwords if you suspect compromise

**Don't:**
- Reuse passwords across sites
- Share passwords via insecure channels
- Write passwords on sticky notes (unless secured)
- Use personal information (names, birthdays)
- Use dictionary words alone
- Store passwords in plain text files

## Technical Details

### Random Generation
- Uses Python's `secrets` module (cryptographically secure)
- Not predictable like `random` module
- Suitable for security-sensitive applications

### Character Sets
- **Lowercase**: a-z (26 characters)
- **Uppercase**: A-Z (26 characters)
- **Digits**: 0-9 (10 characters)
- **Symbols**: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ (32 characters)

### Ambiguous Characters
When `--no-ambiguous` is used, these are excluded:
- `i` and `I` (can look like `l`, `1`, or `|`)
- `l` and `L` (can look like `I`, `1`, or `|`)
- `o` and `O` (can look like `0`)
- `0` (can look like `O`)
- `1` (can look like `l`, `I`, or `|`)

## Clipboard Support

The script attempts to copy to clipboard using:
1. **pyperclip** library (if installed) - works on all platforms
2. **pbcopy** (macOS)
3. **xclip** or **xsel** (Linux)
4. **clip** (Windows)

If none are available, the password is still displayed for manual copying.

## Examples

### General Purpose Password
```bash
python password_generator.py -l 16
# Output: X7$mK9pL#nR2qW5v
```

### WiFi Password (no ambiguous characters)
```bash
python password_generator.py -l 20 --no-ambiguous
# Output: aB3xY9mN7pQ2wE5tR8h
```

### Database Password (alphanumeric only)
```bash
python password_generator.py -l 24 --no-symbols
# Output: aB3xY9mN7pQ2wE5tR8hK6vL
```

### Master Password (memorable passphrase)
```bash
python password_generator.py --passphrase -w 5 --capitalize
# Output: Golden-Phoenix-Mountain-Ocean-Thunder-42
```

### API Keys (multiple at once)
```bash
python password_generator.py -l 32 -n 3 --no-symbols
# Generates 3 x 32-character alphanumeric passwords
```

## Requirements

- Python 3.6 or higher
- No external dependencies required (standard library only)
- Optional: `pyperclip` for enhanced clipboard support

## License

This script is part of the Daily Python Scripts collection and is licensed under the MIT License. See the [LICENSE](../LICENSE) file in the root directory for details.
