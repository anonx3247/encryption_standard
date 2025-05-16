import numpy as np

a = np.uint64(11109033717525269061)
b = np.uint64(10403331604385742251)

operations = [
    (lambda x: x + a, 3),
    (lambda x: x + x + x, 6),
    (lambda x: x ^ b, 2),
    (lambda x: x + b, 3),
    (lambda x: x + x + x + x + x, 9),
    (lambda x: x ^ a, 2),
    (lambda x: bit_rotate(x, 19), 10),
    (lambda x: bit_rotate(x, 13s), 10),
]

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


def sbox(x: np.uint64) -> np.uint64:
    """
    Evals for this s-box are:
    alpha: 4605518919111820264, beta: 2209636954507691192, P: 0.0002
    alpha: 2640855108307626154, beta: 7342575683542231546, P: 0.0002
    alpha: 13221700181408208335, beta: 6322185673877839173, P: 0.0002
    Top Linear Pairs:
    a: 7423956078665021271, b: 409410123895023919, B: 0.0079 ± 0.0078
    a: 8533490844825014657, b: 7271756754228565278, B: 0.0079 ± 0.0078
    a: 384992579778828649, b: 10049135689920458331, B: 0.0079 ± 0.0078
    """

    

    def round(x, a, b): # 11
        x += a # 3
        x = x + x + x  # 6
        return x ^ b # 2

    
    y = round(x, a, b) # 11
    y = round(y, a, b) # 11
    y = round(y, a, b) # 11
    return y



def bit_rotate(x: np.uint64, n: int) -> np.uint64: # 10
    n = np.uint64(n)
    n_inv = np.uint64(64 - n)
    return ((x << n) | (x >> n_inv))

def test_2n(f):
    for i in range(32):
        inp = 2**i
        j = f(np.uint64(inp))
        print(f"{inp:#018x} -> {j:#018x}")


def test_n(f):
    for i in range(32):
        j = f(np.uint64(i))
        print(f"{i:#018x} -> {j:#018x}")