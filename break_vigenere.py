# break_vigenere.py
from keylength import find_key_length
# THIS FUNCTIONS ARE COPIED FROM PRACTICE 1
# Standard English letter frequencies
ENGLISH_FREQS = {
    'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127,
    'F': 0.022, 'G': 0.020, 'H': 0.061, 'I': 0.070, 'J': 0.002,
    'K': 0.008, 'L': 0.040, 'M': 0.024, 'N': 0.067, 'O': 0.075,
    'P': 0.019, 'Q': 0.001, 'R': 0.060, 'S': 0.063, 'T': 0.091,
    'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001, 'Y': 0.020,
    'Z': 0.001
}

def chi_squared_distance(text: str) -> float:
    """Computes the length-normalized chi-squared distance against English frequencies."""
    n = len(text)
    if n == 0:
        return 0.0
    
    counts = {}
    for char in text.upper():
        if 'A' <= char <= 'Z':
            if char in counts:
                counts[char] = counts[char] + 1
            else:
                counts[char] = 1
                
    chi_sq = 0.0
    for letter in ENGLISH_FREQS:
        observed = counts.get(letter, 0)
        expected = n * ENGLISH_FREQS[letter]
        if expected > 0:
            chi_sq = chi_sq + ((observed - expected) ** 2) / expected
            
    return chi_sq / n


def decrypt_caesar(text: str, shift: int) -> str:
    """Decrypts a text using a given Caesar shift."""
    result = ""
    for char in text.upper():
        if 'A' <= char <= 'Z':
            shifted_code = (ord(char) - ord('A') - shift) % 26 + ord('A')
            result = result + chr(shifted_code)
        else:
            result = result + char
    return result


def break_caesar(coset_text: str) -> str:
    """Breaks a single coset by finding the shift that minimizes chi-squared distance."""
    best_shift = 0
    min_score = float('inf')
    
    for shift in range(26):
        candidate = decrypt_caesar(coset_text, shift)
        score = chi_squared_distance(candidate)
        if score < min_score:
            min_score = score
            best_shift = shift
            
    # Return the key character corresponding to this shift
    return chr(ord('A') + best_shift)


# Make sure to import find_key_length from your keylength module:
# from keylength import find_key_length

def attack(ciphertext: str, language: str = "en") -> tuple[str, str]:
    """
    Returns (key, plaintext) for a Vigenere ciphertext without a given key length.
    Chains key length detection (C1), coset splitting, Caesar breaking, and key assembly.
    """
    text = ciphertext.replace(" ", "").upper()
    
    # 1. Find the key length using C1 function
    m = find_key_length(text, max_m=16, language=language)
    
    # 2. Split the ciphertext into m cosets
    cosets = []
    for i in range(m):
        cosets.append([])
        
    for i in range(len(text)):
        coset_index = i % m
        cosets[coset_index].append(text[i])
        
    # 3. Break each coset using the Caesar breaker to assemble the key characters
    key_chars = []
    for coset_chars in cosets:
        coset_str = "".join(coset_chars)
        key_char = break_caesar(coset_str)
        key_chars.append(key_char)
        
    key = "".join(key_chars)
    
    # 4. Decrypt the full ciphertext using the fully assembled key
    plaintext_chars = []
    for i in range(len(text)):
        key_char = key_chars[i % m]
        shift = ord(key_char) - ord('A')
        
        char = text[i]
        if 'A' <= char <= 'Z':
            plain_code = (ord(char) - ord('A') - shift) % 26 + ord('A')
            plaintext_chars.append(chr(plain_code))
        else:
            plaintext_chars.append(char)
            
    plaintext = "".join(plaintext_chars)
    
    return (key, plaintext)