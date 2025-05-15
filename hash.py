from sbox import sbox

def chunk_binary(string, length):
    return [string[i:length+i].zfill(length) for i in range(0, len(string), length)]

def hash(m : int) -> int :
    part_size = 64
    rounds = 5

    binary_m = bin(m)[2:]
    messages = chunk_binary(binary_m, part_size)

    state = 0x123456789abcdef
    for message in messages :
        int_message = int(message, 2)
        for _ in range(rounds) :
            int_message = sbox(int_message) ^ int_message
        state = int_message
        # final_message += bin(int_message)[2:]

    return state

for i in range(1000, 2000) :
    print(hash(i))