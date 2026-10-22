# measure.py
def index_of_coincidence(text: str) -> float:
    n = len(text)
    if n <= 1:
        return 0.0
        
    # We count the frequency of each character in the text
    counts = {}
    for char in text:
        if char in counts:
            counts[char] = counts[char] + 1
        else:
            counts[char] = 1
            
    # We calculate the numerator: sum of f * (f - 1) for each character
    numerator = 0
    for char in counts:
        f = counts[char]
        numerator = numerator + (f * (f - 1))
        
    # We calculate the denominator: n * (n - 1)
    denominator = n * (n - 1)
    
    # We return the final Index of Coincidence float value
    return numerator / denominator

print(index_of_coincidence("CRYPTANALYSIS"))
print(index_of_coincidence("THEINDEXOFCOINCIDENCE"))

ENGLISH_FREQS = {
    'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127,
    'F': 0.022, 'G': 0.020, 'H': 0.061, 'I': 0.070, 'J': 0.002,
    'K': 0.008, 'L': 0.040, 'M': 0.024, 'N': 0.067, 'O': 0.075,
    'P': 0.019, 'Q': 0.001, 'R': 0.060, 'S': 0.063, 'T': 0.091,
    'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001, 'Y': 0.020,
    'Z': 0.001
}

def chi_squared_distance(text: str) -> float:
    n = len(text)
    if n == 0:
        return 0.0
        
    # We count occurrences of each letter in the text (convert to uppercase)
    counts = {}
    for char in text.upper():
        if 'A' <= char <= 'Z':
            if char in counts:
                counts[char] = counts[char] + 1
            else:
                counts[char] = 1
                
    # We calculate the chi-squared statistic: sum(((O - E)^2) / E) / n
    chi_sq = 0.0
    for letter in ENGLISH_FREQS:
        observed = counts.get(letter, 0)
        expected = n * ENGLISH_FREQS[letter]
        if expected > 0:
            chi_sq = chi_sq + ((observed - expected) ** 2) / expected
            
    # We return length-normalized chi-squared distance
    return chi_sq / n


def classify(ciphertext: str, language: str = "en") -> str:
    score = chi_squared_distance(ciphertext)
    
    # Threshold chosen from experimental data (typically around 0.05 to 0.08 
    # depending on text length; transposition keeps natural English frequencies 
    # resulting in a low score, while substitution flattens or alters them).
    threshold = 0.06
    
    if score < threshold:
        return "transposition"
    else:
        return "substitution"