import numpy as np

a = np.uint16(11109)
b = np.uint16(10403)
a_inv = np.uint16(pow(int(a), -1, 2**16))
b_inv = np.uint16(pow(int(b), -1, 2**16))


operations = [
    (lambda x: x + a, 3),
    (lambda x: x + x + x, 6),
    (lambda x: x ^ b, 2),
    (lambda x: x + b, 3),
    (lambda x: x + x + x + x + x, 9),
    (lambda x: x ^ a, 2),
    (lambda x: bit_rotate_16(x, 19), 10),
    (lambda x: bit_rotate_16(x, 13), 10),
]

def sbox(x: np.uint16) -> np.uint16: # 32
    x = bit_rotate_16_left(x, 5)
    x ^= a
    x = ~x
    x *= b
    x = ~x
    x ^= b
    x *= a
    x = bit_rotate_16_left(x, 7)
    return x

def sbox_inv(x: np.uint16) -> np.uint16: # 32
    x = bit_rotate_16_right(x, 7)
    x *= a_inv
    x ^= b
    x = ~x
    x *= b_inv
    x = ~x
    x ^= a
    x = bit_rotate_16_right(x, 5)
    return x

def build_sbox():
    total_cost = 0
    ops = []
    while total_cost < 32:
        op, cost = operations[np.random.randint(0, len(operations))]
        total_cost += cost
        ops.append(op)
    if total_cost > 32:
        ops.pop() 

    def sbox(x: np.uint64) -> np.uint64:
        for op in ops:
            x = op(x)
        return x
    return sbox

def sequential_evaluator(sbox):
    "sees how much outputs differ from inputs"
    inputs = [np.uint64(i) for i in range(1000)]
    outputs = [sbox(x) for x in inputs]
    diff = 0
    for i in range(len(inputs)-1):
        diff += np.sum(outputs[i] ^ outputs[i+1])
    return diff / len(inputs)


def find_good_sbox():
    for _ in range(10000):
        sbox = build_sbox()
        score = sequential_evaluator(sbox)
        if score < 20:
            return sbox
    raise Exception("Failed to find a good sbox")


def bit_rotate_64(x: np.uint64, n: int) -> np.uint64: # 10
    n = np.uint64(n)
    n_inv = np.uint64(64 - n)
    return ((x << n) | (x >> n_inv))

def bit_rotate_64_inv(x: np.uint64, n: int) -> np.uint64: # 10
    n = np.uint64(n)
    n_inv = np.uint64(64 - n)
    return ((x >> n) | (x << n_inv))

def bit_rotate_16(x: np.uint16, n: int) -> np.uint16: # 10
    n = np.uint16(n)
    n_inv = np.uint16(16 - n)
    return ((x << n) | (x >> n_inv))

def bit_rotate_16_left(x: np.uint16, n: int) -> np.uint16:
    n = np.uint16(n)
    n_inv = np.uint16(16 - n)
    return ((x << n) | (x >> n_inv))

def bit_rotate_16_right(x: np.uint16, n: int) -> np.uint16:
    n = np.uint16(n)
    n_inv = np.uint16(16 - n)
    return ((x >> n) | (x << n_inv))


def test_2n(f):
    for i in range(32):
        inp = 2**i
        j = f(np.uint16(inp))
        print(f"{inp:#06x} -> {j:#06x}")


def test_n(f):
    for i in range(32):
        j = f(np.uint16(i))
        print(f"{i:#06x} -> {j:#06x}")

def test_collisions(f, n):
    prev = set()
    for i in range(n):
        j = f(np.uint16(i))
        if j in prev:
            print(f"Collision found at {i:#06x}")
        prev.add(j)
    return prev
