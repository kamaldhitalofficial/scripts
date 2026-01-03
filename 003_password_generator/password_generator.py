"""
Password Generator - Generate secure, customizable passwords
Creates strong passwords with various options and security features.
"""

import secrets
import string
import math
import argparse
import sys

class PasswordGenerator:
    """Generate secure passwords with customizable options."""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = string.punctuation
        self.ambiguous = 'il1Lo0O'
        
    def generate(self, length=16, use_uppercase=True, use_lowercase=True, 
                 use_digits=True, use_symbols=True, no_ambiguous=False):
        """
        Generate a random password.
        
        Args:
            length: Password length
            use_uppercase: Include uppercase letters
            use_lowercase: Include lowercase letters
            use_digits: Include numbers
            use_symbols: Include special characters
            no_ambiguous: Exclude ambiguous characters (i, l, 1, L, o, 0, O)
        
        Returns:
            Generated password string
        """
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        # Build character set
        charset = ''
        required_chars = []
        
        if use_lowercase:
            chars = self.lowercase
            if no_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_uppercase:
            chars = self.uppercase
            if no_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_digits:
            chars = self.digits
            if no_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_symbols:
            charset += self.symbols
            required_chars.append(secrets.choice(self.symbols))
        
        if not charset:
            raise ValueError("At least one character type must be enabled")
        
        # Generate password ensuring at least one character from each enabled type
        remaining_length = length - len(required_chars)
        if remaining_length < 0:
            raise ValueError(f"Password length {length} is too short for the required character types")
        
        password_chars = required_chars + [secrets.choice(charset) for _ in range(remaining_length)]
        
        # Shuffle to avoid predictable patterns
        password_list = list(password_chars)
        for i in range(len(password_list) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_list[i], password_list[j] = password_list[j], password_list[i]
        
        return ''.join(password_list)
    
    def generate_passphrase(self, num_words=4, separator='-', capitalize=False):
        """
        Generate a passphrase using random words.
        
        Args:
            num_words: Number of words in passphrase
            separator: Character to separate words
            capitalize: Capitalize first letter of each word
        
        Returns:
            Generated passphrase string
        """
        # Common word list for passphrases
        words = [
            'correct', 'horse', 'battery', 'staple', 'monkey', 'dragon', 'happy',
            'garden', 'summer', 'winter', 'spring', 'forest', 'mountain', 'ocean',
            'river', 'cloud', 'thunder', 'rainbow', 'sunset', 'sunrise', 'planet',
            'galaxy', 'cosmic', 'magic', 'wizard', 'castle', 'knight', 'queen',
            'king', 'prince', 'royal', 'golden', 'silver', 'crystal', 'diamond',
            'ruby', 'emerald', 'sapphire', 'pearl', 'tiger', 'lion', 'eagle',
            'falcon', 'hawk', 'wolf', 'bear', 'panda', 'koala', 'dolphin',
            'whale', 'shark', 'phoenix', 'unicorn', 'pegasus', 'griffin', 'mermaid',
            'ninja', 'samurai', 'warrior', 'archer', 'ranger', 'rogue', 'paladin',
            'shield', 'sword', 'arrow', 'lance', 'armor', 'helmet', 'crown',
            'throne', 'temple', 'tower', 'bridge', 'gates', 'valley', 'meadow',
            'field', 'prairie', 'desert', 'tundra', 'jungle', 'swamp', 'marsh',
            'island', 'coast', 'harbor', 'port', 'bay', 'lagoon', 'reef',
            'flame', 'blaze', 'frost', 'storm', 'breeze', 'gale', 'tempest',
            'lightning', 'thunder', 'comet', 'meteor', 'asteroid', 'nebula', 'quasar'
        ]
        
        if num_words < 2:
            raise ValueError("Passphrase must have at least 2 words")
        
        selected_words = [secrets.choice(words) for _ in range(num_words)]
        
        if capitalize:
            selected_words = [word.capitalize() for word in selected_words]
        
        # Add a random number at the end for extra security
        passphrase = separator.join(selected_words) + separator + str(secrets.randbelow(100))
        
        return passphrase
    
    def calculate_entropy(self, password):
        """Calculate password entropy (bits)."""
        charset_size = 0
        
        if any(c in self.lowercase for c in password):
            charset_size += len(self.lowercase)
        if any(c in self.uppercase for c in password):
            charset_size += len(self.uppercase)
        if any(c in self.digits for c in password):
            charset_size += len(self.digits)
        if any(c in self.symbols for c in password):
            charset_size += len(self.symbols)
        
        if charset_size == 0:
            return 0
        
        entropy = len(password) * math.log2(charset_size)
        return entropy
    
    def assess_strength(self, password):
        """
        Assess password strength.
        
        Returns:
            Tuple of (strength_label, color_code, description)
        """
        entropy = self.calculate_entropy(password)
        length = len(password)
        
        has_lower = any(c in self.lowercase for c in password)
        has_upper = any(c in self.uppercase for c in password)
        has_digit = any(c in self.digits for c in password)
        has_symbol = any(c in self.symbols for c in password)
        
        variety = sum([has_lower, has_upper, has_digit, has_symbol])
        
        # Strength assessment
        if entropy < 28 or length < 8 or variety < 2:
            return ('Weak', 'Easy to crack, not recommended')
        elif entropy < 36 or length < 10 or variety < 3:
            return ('Fair', 'Could be stronger')
        elif entropy < 60 or length < 12:
            return ('Good', 'Reasonably secure')
        elif entropy < 80 or length < 16:
            return ('Strong', 'Very secure')
        else:
            return ('Excellent', 'Extremely secure')

def copy_to_clipboard(text):
    """Attempt to copy text to clipboard (cross-platform)."""
    try:
        # Try using pyperclip if available
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        # Fallback methods for different platforms
        import subprocess
        import platform
        
        system = platform.system()
        try:
            if system == 'Darwin':  # macOS
                process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
                return True
            elif system == 'Linux':
                # Try xclip first, then xsel
                try:
                    process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                    process.communicate(text.encode('utf-8'))
                    return True
                except FileNotFoundError:
                    process = subprocess.Popen(['xsel', '--clipboard', '--input'], stdin=subprocess.PIPE)
                    process.communicate(text.encode('utf-8'))
                    return True
            elif system == 'Windows':
                process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
                process.communicate(text.encode('utf-16'))
                return True
        except Exception:
            return False
    
    return False

def main():
    parser = argparse.ArgumentParser(
        description='Generate secure passwords with customizable options',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python password_generator.py                              # Default 16-char password
  python password_generator.py -l 20                        # 20-character password
  python password_generator.py -l 12 --no-symbols          # No special characters
  python password_generator.py -l 16 --no-ambiguous        # Exclude ambiguous chars
  python password_generator.py -n 5                         # Generate 5 passwords
  python password_generator.py --passphrase                 # Generate passphrase
  python password_generator.py --passphrase -w 5            # 5-word passphrase
  python password_generator.py -l 20 --copy                 # Copy to clipboard
        """
    )
    
    parser.add_argument(
        '-l', '--length',
        type=int,
        default=16,
        help='Password length (default: 16)'
    )
    
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=1,
        help='Number of passwords to generate (default: 1)'
    )
    
    parser.add_argument(
        '--no-uppercase',
        action='store_true',
        help='Exclude uppercase letters'
    )
    
    parser.add_argument(
        '--no-lowercase',
        action='store_true',
        help='Exclude lowercase letters'
    )
    
    parser.add_argument(
        '--no-digits',
        action='store_true',
        help='Exclude numbers'
    )
    
    parser.add_argument(
        '--no-symbols',
        action='store_true',
        help='Exclude special characters'
    )
    
    parser.add_argument(
        '--no-ambiguous',
        action='store_true',
        help='Exclude ambiguous characters (i, l, 1, L, o, 0, O)'
    )
    
    parser.add_argument(
        '--passphrase',
        action='store_true',
        help='Generate a passphrase instead of a password'
    )
    
    parser.add_argument(
        '-w', '--words',
        type=int,
        default=4,
        help='Number of words in passphrase (default: 4)'
    )
    
    parser.add_argument(
        '--separator',
        type=str,
        default='-',
        help='Separator for passphrase words (default: -)'
    )
    
    parser.add_argument(
        '--capitalize',
        action='store_true',
        help='Capitalize words in passphrase'
    )
    
    parser.add_argument(
        '--copy',
        action='store_true',
        help='Copy first generated password to clipboard'
    )
    
    parser.add_argument(
        '--no-strength',
        action='store_true',
        help='Do not show strength assessment'
    )
    
    args = parser.parse_args()
    
    generator = PasswordGenerator()
    
    print()
    
    try:
        passwords = []
        
        for i in range(args.count):
            if args.passphrase:
                password = generator.generate_passphrase(
                    num_words=args.words,
                    separator=args.separator,
                    capitalize=args.capitalize
                )
            else:
                password = generator.generate(
                    length=args.length,
                    use_uppercase=not args.no_uppercase,
                    use_lowercase=not args.no_lowercase,
                    use_digits=not args.no_digits,
                    use_symbols=not args.no_symbols,
                    no_ambiguous=args.no_ambiguous
                )
            
            passwords.append(password)
            
            # Display password
            if args.count > 1:
                print(f"Password {i+1}:")
            
            print(f"  {password}")
            
            # Show strength assessment
            if not args.no_strength:
                strength, description = generator.assess_strength(password)
                entropy = generator.calculate_entropy(password)
                print(f"  Strength: {strength} ({entropy:.1f} bits of entropy)")
                print(f"  {description}")
            
            if i < args.count - 1:
                print()
        
        # Copy to clipboard
        if args.copy and passwords:
            if copy_to_clipboard(passwords[0]):
                print(f"\n✓ Copied to clipboard!")
            else:
                print(f"\n⚠ Could not copy to clipboard (install pyperclip for better support)")
        
        print()
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)

if __name__ == '__main__':
    main()
