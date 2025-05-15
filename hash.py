from sbox import sbox

def chunk_binary(string, length):
    return [string[i:length+i].zfill(length) for i in range(0, len(string), length)]

def hash(m : int) -> int :
    part_size = 64
    rounds = 5

    binary_m = bin(m)[2:]
    messages = chunk_binary(binary_m, part_size)

    state = 0b0111000110010001001111000000111011100001010010100101100001100010
    for message in messages :
        int_message = int(message, 2)
        for _ in range(rounds) :
            # print(state)
            state = sbox(int_message ^ state) ^ state
        # final_message += bin(int_message)[2:]

    return state

print(hash(100000000))
print(hash(100000001))