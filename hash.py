import numpy as np
from sbox import sbox
from encryption import split_blocks_128

def permute128(x: int) -> int:
    return ((x << 1) & ((1 << 128) - 1)) | (x >> 127)

ROLL_CONSTS = [
    0x0123456789ABCDEF0123456789ABC7EF,
    0x89ABCDEF012345A789ABCBEF01234567,
    0xFEDCBA9896548210FEDCBA9876543210,
    0x76543210FEDCBA98765432101EDCB898,
    0xE80CA19FB33EF56A729C3599FCAB01CA
]

def round_f(state: int, block: int, rc: int) -> int:
    x = state ^ block ^ rc

    y = 0
    for i in range(8):
        nb = (x >> (128 - 16*(i+1))) & 0xFFFF
        s = sbox(np.uint16(nb))
        y |= (int(s) << (128 - 16*(i+1)))

    for j in range (43):
        y = permute128(y)

    return y ^ state

def hash(m_bytes: bytes) -> int:
    m_bitstr = ''.join(f"{byte:08b}" for byte in m_bytes)
    padded = m_bitstr + '1'
    total_with_len = len(padded) + 64
    pad_len = (128 - (total_with_len % 128)) % 128
    padded += '0' * pad_len
    padded += f"{len(m_bitstr):064b}"

    blocs = []
    for i in range(0, len(padded), 128):
        blocs.append(int(padded[i:i+128], 2))

    state = 0b11110001111110010101001100011001111010101010101011111010110111001101010100011000111010111111010100000111010100111011010111100011

    for block in blocs:
        for r in range(len(ROLL_CONSTS)):
            state = round_f(state, block, ROLL_CONSTS[r])

    return state


def hamming_distance(x: int, y: int) -> int:
    return bin(x ^ y).count("1")

def average_hamming(num_values: int) -> float:
    if num_values < 2:
        raise ValueError("Il faut au moins 2 valeurs pour calculer une distance moyenne.")

    hashes = [hash(i.to_bytes((i.bit_length() + 7) // 8 or 1, 'big')) for i in range(num_values)]
    
    total_hd = 0
    for i in range(num_values - 1):
        total_hd += hamming_distance(hashes[i], hashes[i + 1])

    return total_hd / (num_values - 1)


if __name__ == "__main__":
    N = 1000
    avg = average_hamming(N)
    print(f"Distance de Hamming moyenne pour {N} nombres : {avg:.2f} bits")
