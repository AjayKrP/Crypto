def circular_left_shift(l, n):
	return l[n:] + l[:n]


def generate_keys(key):
	round_constant_1 = [1, 0, 0, 0, 0, 0, 0, 0]
	round_constant_2 = [0, 0, 1, 1, 0, 0, 0, 0]

	w0, w1 = key[:len(key)//2], key[len(key)//2:]
	
	w1_rotated = circular_left_shift(w1, len(w1) // 2)
	w1_subbed = substitute_nibbles(w1_rotated)
	w1_xored = add_round_key(w1_subbed, round_constant_1)
	w2 = add_round_key(w0, w1_xored)

	w3 = add_round_key(w1, w2)

	w3_rotated = circular_left_shift(w3, len(w3) // 2)
	w3_subbed = substitute_nibbles(w3_rotated)
	w3_xored = add_round_key(w3_subbed, round_constant_2)
	w4 = add_round_key(w2, w3_xored)

	w5 = add_round_key(w3, w4)

	first_key = w0 + w1
	second_key = w2 + w3
	third_key = w4 + w5

	return first_key, second_key, third_key


def add_round_key(state_box, round_key):
	xored_box = [state_box_value ^ round_key_value for state_box_value, round_key_value in zip(state_box, round_key)]

	return xored_box


def substitute_nibbles(state_box, inverse=False):
	SBox = [[9, 4, 10, 11], [13, 1, 8, 5], [6, 2, 0, 3], [12, 14, 15, 7]]
	SBox_INV = [[10, 5, 9, 11], [1, 7, 8, 15], [6, 0, 2, 3], [12, 4, 13, 14]]

	if inverse:
		box = SBox_INV
	else: box = SBox		

	subbed_box = []		
	for i in range(0, len(state_box), 4):	
		row = state_box[i] * 2 + state_box[i+1]
		col = state_box[i+2] * 2 + state_box[i+3]
		value = box[row][col]

		# Converting hex (mod 16) value into 4 binary digits
		subbed_box += [value // 8, (value % 8) // 4, (value % 4) // 2, value % 2]

	return subbed_box
		

def shift_rows(state_box):
	n0 = state_box[:len(state_box) // 4]
	n1 = state_box[len(state_box) // 4:len(state_box) // 2]
	n2 = state_box[len(state_box) // 2:len(state_box) // 2 + 4]
	n3 = state_box[len(state_box) // 2 + 4:]
	
	state_box = n0 + n3 + n2 + n1	
	
	return state_box


def mix_columns(state_box, inverse=False):
	mixed_box = [None for _ in range(len(state_box))]
	
	if inverse:
		for i, j in zip(range(0, len(state_box), 8), range(4, len(state_box), 8)):
			b0, b1, b2, b3 = state_box[i], state_box[i+1], state_box[i+2], state_box[i+3]
			b4, b5, b6, b7 = state_box[j], state_box[j+1], state_box[j+2], state_box[j+3]

			mixed_box[i:i+4] = [b3 ^ b5, b0 ^ b6, b1 ^ b4 ^ b7, b2 ^ b3 ^ b4]
			mixed_box[j:j+4] = [b1 ^ b7, b2 ^ b4, b0 ^ b3 ^ b5, b0 ^ b6 ^ b7]

	else:
		for i, j in zip(range(0, len(state_box), 8), range(4, len(state_box), 8)):
			b0, b1, b2, b3 = state_box[i], state_box[i+1], state_box[i+2], state_box[i+3]
			b4, b5, b6, b7 = state_box[j], state_box[j+1], state_box[j+2], state_box[j+3]
	
			mixed_box[i:i+4] = [b0 ^ b6, b1 ^ b4 ^ b7, b2 ^ b4 ^ b5, b3 ^ b5]
			mixed_box[j:j+4] = [b2 ^ b4, b0 ^ b3 ^ b5, b0 ^ b1 ^ b6, b1 ^ b7]

	return mixed_box


def encrypt(plaintext, key):
	first_key, second_key, third_key = generate_keys(key)
	ciphertext = ''

	# Initial XOR with first_key
	state_box = add_round_key(plaintext, first_key)
	
	# Round 1
	state_box = substitute_nibbles(state_box)
	state_box = shift_rows(state_box)
	state_box = mix_columns(state_box)
	state_box = add_round_key(state_box, second_key)

	# Round 2
	state_box = substitute_nibbles(state_box)
	state_box = shift_rows(state_box)
	ciphertext = add_round_key(state_box, third_key)

	return ciphertext


def decrypt(ciphertext, key):
	first_key, second_key, third_key = generate_keys(key)
	plaintext = ''
	
	state_box = add_round_key(ciphertext, third_key)
	state_box = shift_rows(state_box)
	state_box = substitute_nibbles(state_box, inverse=True)
	
	state_box = add_round_key(state_box, second_key)
	state_box = mix_columns(state_box, inverse=True)
	state_box = shift_rows(state_box)
	state_box = substitute_nibbles(state_box, inverse=True)
	
	plaintext = add_round_key(state_box, first_key)

	return plaintext


def main():
#	plaintext = [0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1]
	key = [1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1]

#	print(plaintext)

#	ciphertext = encrypt(plaintext, key)
#	print(ciphertext)

#	plaintext = decrypt(ciphertext, key)
#	print(plaintext)

	plaintext = input('Enter plaintext : ')

	ciphertext = ''	
	for i in range(0, len(plaintext), 2):
		first_half = ord(plaintext[i])
		
		if i + 1 == len(plaintext):
			second_half = 0
		else:
			second_half = ord(plaintext[i+1])
		
		first_half = bin(first_half).lstrip('0b').zfill(8)
		first_half = [int(char) for char in first_half]
		second_half = bin(second_half).lstrip('0b').zfill(8)
		second_half = [int(char) for char in second_half]

		plain = first_half + second_half
		cipher = encrypt(plain, key)
		
		first_half, second_half = cipher[:len(cipher)//2], cipher[len(cipher)//2:]
		first_half, second_half = ''.join([str(num) for num in first_half]), ''.join([str(num) for num in second_half])
		first_half, second_half = int(first_half, 2), int(second_half, 2)
		first_half, second_half = chr(first_half), chr(second_half)
		
		ciphertext += first_half + second_half

	print('Ciphertext is :', ciphertext)
		
	plaintext = ''
	for i in range(0, len(ciphertext), 2):
		first_half = ord(ciphertext[i])
		second_half = ord(ciphertext[i+1])

		first_half = bin(first_half).lstrip('0b').zfill(8)
		first_half = [int(char) for char in first_half]
		second_half = bin(second_half).lstrip('0b').zfill(8)
		second_half = [int(char) for char in second_half]
		
		cipher = first_half + second_half
		plain = decrypt(cipher, key)

		first_half, second_half = plain[:len(plain)//2], plain[len(plain)//2:]
		first_half, second_half = ''.join([str(num) for num in first_half]), ''.join([str(num) for num in second_half])
		first_half, second_half = int(first_half, 2), int(second_half, 2)
		first_half, second_half = chr(first_half), chr(second_half)
	
		plaintext += first_half + second_half

	print('Decrypted plaintext is :', plaintext)	
		

if __name__ == '__main__':
	main()
