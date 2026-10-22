# PRACTICE_2_Transposition_Ciphers_and_Classical_Cryptoanalysis_Javier_Caro

## 1. How to run everything with verbatim commands 
This project is built using only standard libraries (`math`, `itertools`, `collections`, `unittest`).

### Running the Unit Test Suite
To execute the complete unit test suite covering round-trips, published check values, and edge cases:

```bash
python -m unittest discover -s tests
```
### Running Individual Cryptanalysis & Cipher Modules
#### Part A: Rail Fence Encryption & Decryption
```bash
python -c "import railfence; print(railfence.encrypt('MYSECRETMESSAGE', 3))"
python -c "import railfence; print(railfence.decrypt('MEMSYRTSGEACESE', 3))"
```
#### Part A: Columnar & Double Transposition
```bash
python -c "import columnar; print(columnar.encrypt('MYSECRETMESSAGE', 'CIPHER', pad='X'))"
python -c "import columnar; print(columnar.encrypt_double('THISISAOFTENUNEVENPLAINTEXTFORTESTING', 'ROTOR', 'ENIGMA', pad='X'))"
```
#### Part B1: Index of Coincidence (IC)
```bash
python -c "import measure; print(measure.index_of_coincidence('CRYPTANALYSIS'))"
```
#### Part B2: Single-Letter Frequency Classifier
```bash
python -c "import measure; print(measure.classify('YOUR_CIPHERTEXT_HERE', language='en'))"
```
#### Part B3: Kasiski Examination
```bash
python -c "import kasiski; print(kasiski.repeats('ELQYRJVQDRLXEGBELQQVALQFEPTQOGDEZRGSIDSCPEFGOPXDOLELQYRJXAOALPKGVD', min_len=3))"
python -c "import kasiski; print(kasiski.factor_tally('ELQYRJVQDRLXEGBELQQVALQFEPTQOGDEZRGSIDSCPEFGOPXDOLELQYRJXAOALPKGVD'))"
```
#### Part C1: Coset IC & Key Length Detection
```bash
python -c "import keylength; print(keylength.find_key_length('YOUR_CIPHERTEXT_HERE', max_m=16))"
```
#### Part C2: Vigenère Cipher Breaker
```bash
python -c "import break_vigenere; key, plain = break_vigenere.attack('YOUR_CIPHERTEXT_HERE'); print(f'Key: {key}\nPlain: {plain[:50]}...')"
```
#### Part C3: Columnar Transposition Breaker
```bash
python -c "import break_columnar; order, plain = break_columnar.attack('YOUR_CIPHERTEXT_HERE', n_cols=5); print(f'Order: {order}\nPlain: {plain[:50]}...')"
```
## 2. Part A3: Padding and Double Transposition 
#### Question:
In your report: that plaintext is 30 letters, and 30 is a multiple of both key lengths, so no padding is needed at either
pass. Explain what your decrypt_double has to do differently when the plaintext length is not a multiple of both,
and why a naive implementation returns garbage in that case.

#### Answer:
When the plaintext length N is not a multiple of both key lengths (k_1 and k_2), the first encryption pass appends padding characters to fill the matrix grid. Double transposition decryption requires reversing the process by first tracking the padded lengths (N_pad1 and N_pad2) because extra dummy characters are added during encryption. You must **reverse Pass 2 first** using Key 2 and N_pad2 to recover the intermediate text, and then **reverse Pass 1 second** using Key 1 and N_pad1 to reconstruct the original padded plaintext. A naive implementation fails because if it uses the original unpadded length (N) instead of N_pad1 for Pass 2, the grid dimensions become mismatched; this offsets the column boundaries, causing a domino effect where every subsequent character falls into the wrong position and turns the final message into unreadable garbage.

## 3. Part B1: Minimum trustworthy length
#### Question:
CRYPTANALYSIS is an English word whose index equals that of uniformly random letters. State the
shortest text length at which you would trust this measurement, and how you decided.

#### Answer: 
The Index of Coincidence ($\text{IC}$) is defined as:$$\text{IC} = \frac{\sum_{i=A}^{Z} f_i (f_i - 1)}/{N (N - 1)}$$
For the word CRYPTANALYSIS (N = 13). IC = $6/156$

