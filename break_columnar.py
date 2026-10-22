# break_columnar.py
import itertools
import math

def decrypt_with_order(ciphertext: str, order: tuple[int, ...]) -> str:
    n_cols = len(order)
    num_rows = len(ciphertext) // n_cols
    
    # We create an empty grid
    grid = [['' for _ in range(n_cols)] for _ in range(num_rows)]
    
    # We fill the grid columns according to the given permutation order
    char_index = 0
    for col_idx in order:
        for r in range(num_rows):
            grid[r][col_idx] = ciphertext[char_index]
            char_index = char_index + 1
            
    # We read the grid row by row to reconstruct the plaintext
    plaintext = ""
    for r in range(num_rows):
        for c in range(n_cols):
            plaintext = plaintext + grid[r][c]
            
    return plaintext



def score_text(text: str) -> float:
    score = 0.0
    text = text.upper()
    
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if 'A' <= bigram[0] <= 'Z' and 'A' <= bigram[1] <= 'Z':
            score = score + 1.0 
            
    return score


def attack(ciphertext: str, n_cols: int, language: str = "en") -> tuple[tuple[int, ...], str]:
    text = ciphertext.replace(" ", "").upper()
    
    best_order = None
    best_plaintext = ""
    max_score = -float('inf')
    
    # We generate all n! permutations of column indices
    all_permutations = itertools.permutations(range(n_cols))
    
    for order in all_permutations:
        candidate_plain = decrypt_with_order(text, order)
        score = score_text(candidate_plain)
        
        if score > max_score:
            max_score = score
            best_order = order
            best_plaintext = candidate_plain
            
    return (best_order, best_plaintext)