from collections import deque

def flipper(nibble):
    out = ""
    for i in nibble:
        if i == "1":
            out += "0"
        elif i == "0":
            out += "1"
    return out

def encrypt(hash, key):
    bin_from_key = []
    bin_from_hash = []

    # Substitute hexadecimal digits with binary equivalent {
    for digit in hash:
        bin_from_hash.append(format(int(digit, 16), "04b"))

    for digit in key:
        bin_from_key.append(format(int(digit, 16), "04b"))
    # }

    # Turn binary list into matrix {
    matrix_key = [[bin_from_key[i] for i in range(x, x+8)] for x in range(0, len(bin_from_key), 8)]
    
    matrix_hash = [[bin_from_hash[i] for i in range(x, x+8)] for x in range(0, len(bin_from_hash), 8)]
    # }

    # Turn to deque (for row shifting) {
    for i in range(len(matrix_hash)):
        matrix_hash[i] = deque(matrix_hash[i])
    
    for i in range(len(matrix_key)):
        matrix_key[i] = deque(matrix_key[i])
    # }

    # Combine key {
    for i in range(8):
        for j in range(8):
            matrix_hash[i][j] = format(int(matrix_key[i][j], 2) ^ int(matrix_hash[i][j], 2), "04b")
    # }

    # Round function {
    for i in range(20):
        # Modify hash {
        # Flip nibble
        for j in range(8):
            for e in range(8):
                matrix_hash[j][e] = matrix_hash[j][e][::-1]
        
        # Flip bits in nibble
        for j in range(8):
            for e in range(8):
                matrix_hash[j][e] = flipper(matrix_hash[j][e])
        
        # Mix columns
        for j in range(8):
            for e in range(8):
                if j == 7:
                    matrix_hash[j][e] = format(int(matrix_hash[0][e], 2) ^ int(matrix_hash[j][e], 2), "04b")
                else:
                    matrix_hash[j][e] = format(int(matrix_hash[j+1][e], 2) ^ int(matrix_hash[j][e], 2), "04b")
        
        # Shift left
        for j in range(8):
            matrix_hash[j].rotate(-(j))
        # }
        
        # Generate round key {
        # Shift right
        for j in range(8):
            matrix_key[j].rotate(j)
        
        # Combine columns 
        first_column = [j[0] for j in matrix_key]
        for j in range(1, 8):
            for e in range(8):
                matrix_key[e][j] = format(int(first_column[e], 2) ^ int(matrix_key[e][j], 2), "04b")
        
        
        # }

        # Combine key + hash
        for j in range(8):
            for e in range(8):
                matrix_hash[j][e] = format(int(matrix_key[j][e], 2) ^ int(matrix_hash[j][e], 2), "04b")
        
        # Reverse hash
        matrix_hash = matrix_hash[::-1]

    end = [" ".join(i) for i in matrix_hash]
    end2 = " ".join(end)
    return end2.replace(" ", "")
    

if __name__ == "__main__":
    print(encrypt("3CDD147A9C274898FB6E23310A19A3B6523685DFA96F4F87912E17709421262D", format(65637, "064x")))
    flipper(None)
    
