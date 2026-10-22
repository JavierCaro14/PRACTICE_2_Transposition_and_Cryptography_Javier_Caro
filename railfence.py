# railfence.py
def encrypt(plaintext:str, rails: int) -> str:
    if rails == 1: # if there is only one rail it is obvios that it is the same text
        return plaintext
    # We create the rails using a normal loop
    fence = []
    for r in range(rails):
        fence.append([])
        
    current_rail = 0
    step = 1 # 1 means going up and -1 going down
    
    # We distribute each character in a zigzag pattern across the rails
    for char in plaintext:
        fence[current_rail].append(char)
        current_rail = current_rail + step

        # We change the direction in case we hit the top or bottom rail 
        if current_rail == 0 or current_rail == rails - 1:
            step = step * -1
            
    # We combine all the rails from top to bottom into a single string 
    resultado = ""
    for row in fence:
        for char in row:
            resultado = resultado + char
            
    return resultado

def decrypt(ciphertext:str, rails:int) -> str:
    if rails == 1:
        return ciphertext
        
    # Create an empty grid step-by-step with loops
    fence = []
    for r in range(rails):
        row = []
        for c in range(len(ciphertext)):
            row.append(None)
        fence.append(row)
        
    # Mark the zigzag path with asterisks '*'
    current_rail = 0
    step = 1
    for i in range(len(ciphertext)):
        fence[current_rail][i] = "*"
        current_rail = current_rail + step
        if current_rail == 0 or current_rail == rails - 1:
            step = step * -1
            
    # Fill the asterisks in order with the characters from the ciphertext
    index = 0
    for r in range(rails):
        for c in range(len(ciphertext)):
            if fence[r][c] == "*" and index < len(ciphertext):
                fence[r][c] = ciphertext[index]
                index = index + 1
                
    # Read the grid following the zigzag path to reconstruct the original text
    resultado = ""
    current_rail = 0
    step = 1
    for i in range(len(ciphertext)):
        resultado = resultado + fence[current_rail][i]
        current_rail = current_rail + step
        if current_rail == 0 or current_rail == rails - 1:
            step = step * -1
            
    return resultado

print(encrypt("MYSECRETMESSAGE", 2))
print(encrypt("MYSECRETMESSAGE", 3))
print(encrypt("MYSECRETMESSAGE", 4))
