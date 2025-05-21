import numpy as np
import galois

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
    return ((x << 5) | (x >> inv5))

def bit_rotate_7_left(x: np.uint16) -> np.uint16: # 10 / 4 = 2.5
    return ((x << 7) | (x >> inv7))

def bit_rotate_5_right(x: np.uint16) -> np.uint16: # 10 / 4 = 2.5
    return ((x >> 5) | (x << inv5))

def bit_rotate_7_right(x: np.uint16) -> np.uint16: # 10 / 4 = 2.5
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

F_2 = galois.GF(2)
# We make the choice to store matrices as 64-long-lists of uint64s

def matrix_L() -> list[np.uint64]:
    lines = """c063fe883bca8005
80c7fd107795000b
18ffa20ef2a0017
31ff441de54002e
63fe883bca8005c
c7fd107795000b8
18ffa20ef2a00170
31ff441de54002e0
63fe883bca8005c0
c7fd107795000b80
8ffa20ef2a001701
1ff441de54002e03
3fe883bca8005c06
7fd107795000b80c
ffa20ef2a0017018
ff441de54002e031
fe883bca8005c063
fd107795000b80c7
fa20ef2a0017018f
f441de54002e031f
e883bca8005c063f
d107795000b80c7f
a20ef2a0017018ff
441de54002e031ff
883bca8005c063fe
107795000b80c7fd
20ef2a0017018ffa
41de54002e031ff4
83bca8005c063fe8
7795000b80c7fd1
ef2a0017018ffa2
1de54002e031ff44
3bca8005c063fe88
7795000b80c7fd10
ef2a0017018ffa20
de54002e031ff441
bca8005c063fe883
795000b80c7fd107
f2a0017018ffa20e
e54002e031ff441d
ca8005c063fe883b
95000b80c7fd1077
2a0017018ffa20ef
54002e031ff441de
a8005c063fe883bc
5000b80c7fd10779
a0017018ffa20ef2
4002e031ff441de5
8005c063fe883bca
b80c7fd107795
17018ffa20ef2a
2e031ff441de54
5c063fe883bca8
b80c7fd1077950
17018ffa20ef2a0
2e031ff441de540
5c063fe883bca80
b80c7fd10779500
17018ffa20ef2a00
2e031ff441de5400
5c063fe883bca800
b80c7fd107795000
7018ffa20ef2a001
e031ff441de54002""".split('\n')
    
    mat = [np.uint64(int())
    

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
    result = np.uint64(0)
    for j in range(64):
        if (vector>>(63-j))&1 == 1:
            result ^= matrix[j]
    return result




#################################################
################# 3. Hachage ####################
#################################################


#################################################
############## 4. Mode d'Opération ##############
#################################################


#################################################
################## 5.Signature ##################
#################################################


#################################################
############## 6.Echange de clefs ###############
#################################################