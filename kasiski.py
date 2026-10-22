# kasiski.py

def repeats(ciphertext: str, min_len: int = 3) -> dict[str, list[int]]:
    text = ciphertext.replace(" ", "")
    n = len(text)
    
    substring_positions = {}
    
    # We extract all substrings of length >= min_len
    for length in range(min_len, n + 1):
        for i in range(n - length + 1):
            sub = text[i : i + length]
            if sub not in substring_positions:
                substring_positions[sub] = []
            substring_positions[sub].append(i)
            
    # We filter to keep only substrings that appear more than once
    repeated_subs = {}
    for sub in substring_positions:
        if len(substring_positions[sub]) > 1:
            repeated_subs[sub] = substring_positions[sub]
            
    return repeated_subs


def distances(ciphertext: str, min_len: int = 3) -> list[int]:
    rep_dict = repeats(ciphertext, min_len)
    dist_list = []
    
    for sub in rep_dict:
        positions = rep_dict[sub]
        # We calculate distance between consecutive occurrences
        for i in range(len(positions) - 1):
            d = positions[i + 1] - positions[i]
            dist_list.append(d)
            
    return dist_list


def factor_tally(ciphertext: str, max_factor: int = 20) -> dict[int, int]:
    dist_list = distances(ciphertext, min_len=3)
    tally = {}
    
    for factor in range(2, max_factor + 1):
        count = 0
        for d in dist_list:
            if d % factor == 0:
                count = count + 1
        tally[factor] = count
        
    return tally

sample_cipher = (
    "ELQYR JVQDR LXEGB ELQQV ALQFE PTQOG DEZRG SIDSC PEFGO PXDOL "
    "ELQYR JXAOA LPKGV D"
)

# Run and print repeats
rep = repeats(sample_cipher, min_len=3)
print("REPEATS FOUND")
for sub, pos in rep.items():
    print(f"'{sub}': positions {pos}")

# Run and print distances
dists = distances(sample_cipher, min_len=3)
print("\nDISTANCES")
print(dists)

# Run and print factor tally
tally = factor_tally(sample_cipher, max_factor=20)
print("\nFACTOR TALLY")
print(tally)