import numpy as np
from sbox import sbox, sbox_inv
from matrix_ops import matrix_multiply_vector, circular_matrix_from_vector, matrix_inverse

matrix = circular_matrix_from_vector(np.uint64(0xc063fe883bca8005))
matrix_inv = matrix_inverse(matrix)

def block_encrypt(key: np.uint64, message: int, rounds: int = 16) -> int:
    # separate into 64-bit blocks with padding
    message_blocks = split_blocks(message, 64)
    outputs = message_blocks

    for _ in range(rounds):
        for i in range(len(outputs)):
            outputs[i] = block_encryption_round(key, outputs[i])
    
    # concatenate the outputs
    return join_blocks(outputs, 64)

def block_decrypt(key: np.uint64, cipher: int, rounds: int = 16) -> int:
    # separate into 64-bit blocks with padding
    cipher_blocks = split_blocks(cipher, 64)
    outputs = cipher_blocks

    for _ in range(rounds):
        for i in range(len(outputs)):
            outputs[i] = block_decryption_round(key, outputs[i])
    
    # concatenate the outputs
    return join_blocks(outputs, 64)


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

def linear_layer(blocks: list[np.uint16]) -> np.uint64:
    global matrix
    # concatenate the blocks into a single 64-bit vector
    vector = join_blocks(blocks, 16)
    return matrix_multiply_vector(matrix, vector)

def linear_layer_inv(vector: np.uint64) -> list[np.uint16]:
    global matrix_inv
    output = matrix_multiply_vector(matrix_inv, vector)
    # split the output into 16-bit blocks
    return split_blocks(output, 16)


def join_blocks(blocks: list[np.uint16], block_size: int) -> np.uint64:
    return np.uint64(int(''.join([bin(block)[2:].zfill(block_size) for block in blocks]), 2))

def split_blocks(vector: np.uint64, block_size: int) -> list[np.uint16]:
    vector_str = bin(vector)[2:].zfill(64)
    if block_size == 16:
        blocks = [np.uint16(int(vector_str[i:i+block_size], 2)) for i in range(0, 64, block_size)]
    elif block_size == 64:
        blocks = [np.uint64(int(vector_str[i:i+block_size], 2)) for i in range(0, 64, block_size)]
    return blocks