import numpy as np
import galois
from sbox import bit_rotate_64

GF = galois.GF(2)

def matrix_multiply_vector(matrix: list[np.uint64], vector: np.uint64) -> np.uint64:
    result = np.uint64(0)
    for j in range(64):
        if (vector>>(63-j))&1 == 1:
            result ^= matrix[j]
    return result

def test_matrix_multiply_vector():
    A = rand_matrix()
    x = np.random.randint(0, 2**64, dtype=np.uint64)
    y = matrix_multiply_vector(A, x)
    A_in_F2 = matrix_to_F2(A)
    x_in_F2 = vector_to_F2(x)
    y_in_F2 = A_in_F2 @ x_in_F2
    y_from_F2 = vector_from_F2(y_in_F2)
    print("y_from_F2", bin(y_from_F2)[2:].zfill(64))
    print("y", bin(y)[2:].zfill(64))
    print("y_from_F2 == y", y_from_F2 == y)

def transpose_matrix(matrix_as_list_rows: list[np.uint64]) -> list[np.uint64]:
    """
    Transpose a matrix represented as a list of rows.

    Note: basically useless as we are using only symmetric matrices
    """
    mat = np.array(list_repr_to_matrix(matrix_as_list_rows))
    return matrix_to_list_repr(np.array(mat.T).tolist())


def rand_matrix() -> list[np.uint64]:
    rand_init = np.random.randint(0, 2**64, dtype=np.uint64)
    return circular_matrix_from_vector(rand_init)

def circular_matrix_from_vector(vector: np.uint64) -> list[np.uint64]:
    matrix = [np.uint64(0) for _ in range(64)]
    for i in range(64):
        matrix[i] = bit_rotate_64(vector, i)
    return matrix

def display_matrix(matrix: list[np.uint64]) -> None:
    for i in range(64):
        print(bin(matrix[i])[2:].zfill(64))

def matrix_inverse(input: list[np.uint64]) -> list[np.uint64]:
    matrix = matrix_to_F2(input)
    matrix_inv = np.linalg.inv(matrix)
    return matrix_from_F2(matrix_inv)

def test_inverse():
    x = np.random.randint(0, 2**64, dtype=np.uint64)
    A = rand_matrix()
    print("x", x)
    y = matrix_multiply_vector(A, x)
    print("y", y)
    A_inv = matrix_inverse(A)
    z = matrix_multiply_vector(A_inv, y)
    print("z", z)
    print("x == z", x == z)



def list_repr_to_matrix(list_repr: list[np.uint64]) -> list[list[np.uint64]]:
    matrix = [[0 for _ in range(64)] for _ in range(64)]
    for i in range(64):
        repr = bin(list_repr[i])[2:].zfill(64)
        for j in range(64):
            matrix[i][j] = int(repr[j])
    return matrix

def matrix_to_list_repr(matrix: list[list[np.uint64]]) -> list[np.uint64]:
    return [np.uint64(int(''.join([str(matrix[i][j]) for j in range(64)]), 2)) for i in range(64)]

def matrix_to_F2(matrix: list[np.uint64]) -> np.ndarray:
    matrix = list_repr_to_matrix(matrix)
    matrix_in_F2 = GF(matrix)
    return matrix_in_F2

def matrix_from_F2(matrix: np.ndarray) -> list[np.uint64]:
    return matrix_to_list_repr(matrix.tolist())

def vector_to_F2(vector: np.uint64) -> np.ndarray:
    vector = np.array([int(bin(vector)[2:].zfill(64)[i]) for i in range(64)])
    vector_in_F2 = GF(vector)
    return vector_in_F2

def vector_from_F2(vector: np.ndarray) -> np.uint64:
    return np.uint64(int(''.join([str(vector[i]) for i in range(64)]), 2))
