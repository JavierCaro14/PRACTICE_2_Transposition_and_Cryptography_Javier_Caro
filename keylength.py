# keylength.py

def index_of_coincidence(text: str) -> float: # same as in measure.py
    n = len(text)
    if n <= 1:
        return 0.0
        
    counts = {}
    for char in text:
        if char in counts:
            counts[char] = counts[char] + 1
        else:
            counts[char] = 1
            
    numerator = 0
    for char in counts:
        f = counts[char]
        numerator = numerator + (f * (f - 1))
        
    denominator = n * (n - 1)
    return numerator / denominator



def coset_ic(ciphertext: str, m: int) -> float:
    text = ciphertext.replace(" ", "")
    
    # We create m empty lists to hold the cosets
    cosets = []
    for i in range(m):
        cosets.append([])
        
    # We distribute characters into cosets based on their index modulo m
    for i in range(len(text)):
        coset_index = i % m
        cosets[coset_index].append(text[i])
        
    # We calculate the IC(Index of Coincidence) for each coset and find the average
    total_ic = 0.0
    for coset_chars in cosets:
        coset_str = "".join(coset_chars)
        total_ic = total_ic + index_of_coincidence(coset_str)
        
    return total_ic / m


def find_key_length(ciphertext: str, max_m: int = 16, language: str = "en") -> int:
    # Random text IC is around 0.038, English text IC is around 0.067.
    # We set a threshold well above random text to identify proper alignment.
    threshold = 0.055
    
    # We loop from 1 upwards to find the smallest valid key length
    for m in range(1, max_m + 1):
        avg_ic = coset_ic(ciphertext, m)
        
        # If the average IC stands above the baseline then we return this m
        if avg_ic > threshold:
            return m
            
    return 1