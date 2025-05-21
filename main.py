import numpy as np
from sage.all_cmdline import *   # import sage library


################################################
#################### 1. Sbox ####################
#################################################

a = np.uint16(11109)
b = np.uint16(10403)
a_inv = np.uint16(pow(int(a), -1, 2**16))
b_inv = np.uint16(pow(int(b), -1, 2**16))

inv5 = np.uint16(16 - 5)
inv7 = np.uint16(16 - 7)

def bit_rotate_5_left(x: np.uint16) -> np.uint16: # 10 / 4 = 2.5
    global inv5
    return ((x << 5) | (x >> inv5))

def bit_rotate_7_left(x: np.uint16) -> np.uint16: # 10 / 4 = 2.5
    global inv7
    return ((x << 7) | (x >> inv7))

def bit_rotate_5_right(x: np.uint16) -> np.uint16: # 10 / 4 = 2.5
    global inv5
    return ((x >> 5) | (x << inv5))

def bit_rotate_7_right(x: np.uint16) -> np.uint16: # 10 / 4 = 2.5
    global inv7
    return ((x >> 7) | (x << inv7))

def sbox(x: np.uint16) -> np.uint16: # 32
    x = bit_rotate_5_left(x) # 2.5
    x = ~(x ^ a) # (2 + 2) / 4 = 1
    x *= b # 50 / 4 = 12.5
    x = ~(x ^ b) # 1
    x *= a # 12.5
    x = bit_rotate_7_left(x) # 2.5
    return x

def sbox_inv(x: np.uint16) -> np.uint16: # 32
    x = bit_rotate_7_right(x)
    x *= a_inv
    x ^= b
    x = ~x
    x *= b_inv
    x = ~x
    x ^= a
    x = bit_rotate_5_right(x)
    return x

#################################################
################ 2. Chiffrement #################
#################################################

# We make the choice to store matrices as 64-long-lists of uint64s

def matrix_L_inverse() -> list[np.uint64]:
    # precalculated
    lines = """f8149a47d179d1ad
f029348fa2f3a35b
e052691f45e746b7
c0a4d23e8bce8d6f
8149a47d179d1adf
29348fa2f3a35bf
52691f45e746b7e
a4d23e8bce8d6fc
149a47d179d1adf8
29348fa2f3a35bf0
52691f45e746b7e0
a4d23e8bce8d6fc0
49a47d179d1adf81
9348fa2f3a35bf02
2691f45e746b7e05
4d23e8bce8d6fc0a
9a47d179d1adf814
348fa2f3a35bf029
691f45e746b7e052
d23e8bce8d6fc0a4
a47d179d1adf8149
48fa2f3a35bf0293
91f45e746b7e0526
23e8bce8d6fc0a4d
47d179d1adf8149a
8fa2f3a35bf02934
1f45e746b7e05269
3e8bce8d6fc0a4d2
7d179d1adf8149a4
fa2f3a35bf029348
f45e746b7e052691
e8bce8d6fc0a4d23
d179d1adf8149a47
a2f3a35bf029348f
45e746b7e052691f
8bce8d6fc0a4d23e
179d1adf8149a47d
2f3a35bf029348fa
5e746b7e052691f4
bce8d6fc0a4d23e8
79d1adf8149a47d1
f3a35bf029348fa2
e746b7e052691f45
ce8d6fc0a4d23e8b
9d1adf8149a47d17
3a35bf029348fa2f
746b7e052691f45e
e8d6fc0a4d23e8bc
d1adf8149a47d179
a35bf029348fa2f3
46b7e052691f45e7
8d6fc0a4d23e8bce
1adf8149a47d179d
35bf029348fa2f3a
6b7e052691f45e74
d6fc0a4d23e8bce8
adf8149a47d179d1
5bf029348fa2f3a3
b7e052691f45e746
6fc0a4d23e8bce8d
df8149a47d179d1a
bf029348fa2f3a35
7e052691f45e746b
fc0a4d23e8bce8d6""".split('\n')
    return [np.uint64(int(line, 16)) for line in lines]
    
def bit_rotate_64(x: np.uint64, n: int) -> np.uint64:
    n = np.uint64(n)
    n_inv = np.uint64(64 - n)
    return ((x << n) | (x >> n_inv))

def circulant_matrix_from_vector(vector: np.uint64) -> list[np.uint64]:
    matrix = [np.uint64(0) for _ in range(64)]
    for i in range(64):
        matrix[i] = bit_rotate_64(vector, i)
    return matrix

def matrix_multiply_vector(matrix: list[np.uint64], vector: np.uint64) -> np.uint64:
    # Pour des vecteurs binaires la multiplication revient a xor-er les colonnes
    # correspondant aux linges du vecteur avec un 1
    # ici on le fait avec des lignes cars toutes nos matrices sont symmetriques
    result = np.uint64(0)
    for j in range(64):
        if (vector>>(63-j))&1 == 1:
            result ^= matrix[j]
    return result

matrix_L = circulant_matrix_from_vector(np.uint64(0xc063fe883bca8005))
matrix_L_inv = matrix_L_inverse()

def join_blocks(blocks: list[np.uint16], block_size: int) -> np.uint64:
    return np.uint64(int(''.join([bin(block)[2:].zfill(block_size) for block in blocks]), 2))

def split_blocks(vector: np.uint64, block_size: int) -> list[np.uint16]:
    vector_str = bin(vector)[2:].zfill(64)
    return [np.uint16(int(vector_str[i:i+block_size], 2)) for i in range(0, 64, block_size)]

def join_blocks_64(blocks: list[np.uint64]) -> int:
    return int(''.join([bin(block)[2:].zfill(64) for block in blocks]), 2)

def split_blocks_64(vector: int, num_blocks: int = None) -> list[np.uint64]:
    vector_str = str(bin(vector))[2:]
    length = len(vector_str)
    if num_blocks is None:
        num_blocks = length // 64 + 1
    vector_str = vector_str.zfill(64 * num_blocks)
    return [np.uint64(int(vector_str[i:i+64], 2)) for i in range(0, 64 * num_blocks, 64)]

def linear_layer(blocks: list[np.uint16]) -> np.uint64:
    global matrix_L
    # concatenate the blocks into a single 64-bit vector
    vector = join_blocks(blocks, 16)
    return matrix_multiply_vector(matrix_L, vector)

def linear_layer_inv(vector: np.uint64) -> list[np.uint16]:
    global matrix_L_inv
    output = matrix_multiply_vector(matrix_L_inv, vector)
    # split the output into 16-bit blocks
    return split_blocks(output, 16)

def block_encryption_round(key: np.uint64, message: np.uint64) -> np.uint64:
    message = message ^ key
    blocks = split_blocks(message, 16)
    blocks = [sbox(block) for block in blocks]
    output = linear_layer(blocks)
    return output

def block_decryption_round(key: np.uint64, cipher: np.uint64) -> np.uint64:
    blocks = linear_layer_inv(cipher)
    blocks = [sbox_inv(block) for block in blocks]
    output = join_blocks(blocks, 16)
    output = output ^ key
    return output

def block_encrypt(key: np.uint64, m: int, rounds: int = 16) -> int:
    # separate into 64-bit blocks with padding
    message_blocks = split_blocks_64(m)
    outputs = message_blocks

    for _ in range(rounds):
        for i in range(len(outputs)):
            outputs[i] = block_encryption_round(key, outputs[i])
    
    # concatenate the outputs
    return join_blocks_64(outputs), len(outputs)

def block_decrypt(key: np.uint64, c: int, rounds: int = 16, num_blocks: int = None) -> int:
    # separate into 64-bit blocks with padding
    cipher_blocks = split_blocks_64(c, num_blocks)
    outputs = cipher_blocks


    for _ in range(rounds):
        for i in range(len(outputs)):
            outputs[i] = block_decryption_round(key, outputs[i])
    
    # concatenate the outputs
    return join_blocks_64(outputs)

#################################################
################# 3. Hachage ####################
#################################################

def split_blocks_128(vector: int, num_blocks: int = None) -> list[np.uint64]:
    vector_str = str(bin(vector))[2:]
    length = len(vector_str)
    if num_blocks is None:
        num_blocks = length // 128 + 1
    vector_str = vector_str.zfill(128 * num_blocks)
    return [int(vector_str[i:i+128], 2) for i in range(0, 128 * num_blocks, 128)]

def p_128(value: int) -> int:
    # 128 bits divisés en 8 blocs de 16 bits
    blocs = [(value >> (128 - 16*(i+1))) & 0xFFFF for i in range(8)]
    blocs = [sbox(np.uint16(b)) for b in blocs]
    blocs = [int(blocs[i]) << (128 - 16*(i+1)) for i in range(8)]
    return sum(blocs)


def hash(message: int) -> int:
    """
    Hybride entre éponge et Merkle–Damgård avec f(M, S) = p_128(M ^ S) ^ S
    """

    chunks = split_blocks_128(message)
    state = 0b11110001111110010101001100011001111010101010101011111010110111001101010100011000111010111111010100000111010100111011010111100011

    for chunk in chunks:
        state = p_128(chunk ^ state) ^ state

    return state

#################################################
############## 4. Mode d'Opération ##############
#################################################

def encrypt_and_authenticate(keys: list[np.uint16], m: int, aux=None):
    if len(keys) != 2:
        raise ValueError("Deux clés sont requises")
    
    k1, k2 = keys
    
    c, num_blocks = block_encrypt(k1, m)

    k2 = int(k2)

    tag = hash(m ^ k2)

    aux = num_blocks
    
    return aux, c, tag

def decrypt_and_verify(keys: list[np.uint16], c: int, tag: int, aux=None):
    if len(keys) != 2:
        raise ValueError("Deux clés sont requises")
    
    k1, k2 = keys
    k2 = int(k2)
    
    # Déchiffrement du message seulement si le tag est valide
    m = block_decrypt(k1, c, num_blocks=aux)

    
    # Vérification du tag avant déchiffrement
    computed_tag = hash(m ^ k2)
    
    if computed_tag != tag:
        print(f"Tag invalide: {computed_tag:x} != {tag:x}")
        return False, None
    
    return True, m

#################################################
################## 5.Signature ##################
#################################################

p = Integer(2**128 + 51)
K = GF(p)

a = Integer(2) 
b = Integer(36) 

E = EllipticCurve(K, [a, b])

G = E.gens()[0]
q = G.order()

print(f"Generator of the curve : {G} of order {q}")

def secrandom(length) :
    return ZZ.random_element(1 , p)

def signature_keygen():
    secret_key = secrandom(q)
    public_key = secret_key * G
    return secret_key, public_key

def sign(secret_key, m) :
    e = hash(m) % q
    k = secrandom(q)
    r = ZZ((k * G)[1]) % q
    s = ZZ(e * secret_key * r) * inverse_mod(k, q) % q
    sigma = (r, s)
    return sigma

def verify(public_key, signature, m) :
    r, s = signature
    t = inverse_mod(s, q) % q
    e = hash(m)
    u = r * e * t % q
    r_prime = u * public_key
    success = r == r_prime[1]
    return success

#################################################
############## 6.Echange de clefs ###############
#################################################