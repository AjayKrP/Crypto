FIXED_IP = (2, 6, 3, 1, 4, 8, 5, 7)
FIXED_EP = (4, 1, 2, 3, 2, 3, 4, 1)
FIXED_IP_INVERSE = (4, 1, 3, 5, 7, 2, 8, 6)
FIXED_P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
FIXED_P8 = (6, 3, 7, 4, 8, 5, 10, 9)
FIXED_P4 = (2, 4, 3, 1)
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

KEY = [0, 0, 1, 0, 0, 1, 0, 1, 1, 1]

def permute(original, table):
    result = list()
    for i in table: result.append(original[i - 1])
    return result

def get_left(bits): return bits[:len(bits) // 2]

def get_right(bits): return bits[len(bits) // 2:]

def circular_left_shift(l, n): return l[n:] + l[:n]

def key1(): return permute(circular_left_shift(permute(KEY, FIXED_P10), 1), FIXED_P8)

def key2(): return permute(circular_left_shift(permute(KEY, FIXED_P10), 3), FIXED_P8)

def xor(l1, l2): return [i ^ j for i, j in zip(l1, l2)]

def to_binary(i): return [int(j) for j in bin(i).replace('b', '').zfill(4)]

def look_sbox(bits, sbox):
    row = bits[0] * 2 + bits[3]
    col = bits[1] * 2 + bits[2]
    return to_binary(sbox[row][col])

def f(bits, key):
    L, R = get_left(bits), get_right(bits)
    bits = permute(R, FIXED_EP)
    bits = xor(bits, key)
    bits = look_sbox(get_left(bits), S0) + look_sbox(get_right(bits), S1)
    bits = permute(bits, FIXED_P4)
    return xor(bits, L)

def encrypt(pt):
    bits = permute(pt, FIXED_IP)
    f_k = f(bits, key1())
    bits = get_right(bits) + f_k
    bits = f(bits, key2())
    return permute(bits + f_k , FIXED_IP_INVERSE)



def decrypt(pt):
    bits = permute(pt, FIXED_IP)
    f_k = f(bits, key2())
    bits = get_right(bits) + f_k
    bits = f(bits, key1())
    return permute(bits + f_k, FIXED_IP_INVERSE)

plaintext = [1, 0, 0, 1, 0, 1, 0, 1]

print(encrypt(plaintext))
print(decrypt(encrypt(plaintext)))
