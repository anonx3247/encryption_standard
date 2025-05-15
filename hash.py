from sbox import sbox

def chunk_binary(string, length):
    return [string[i:length+i].zfill(length) for i in range(0, len(string), length)]

def hash(m : int) -> int :
    """
    Calcule le hash d'un message de taille quelconque, selon la construction de Merkle–Damgård.
    Pour la fonction, nous utilisons une construction du type Davies–Meyer, avec la 
    fonction f(M, S) = sbox(M ^ S) ^ S
    Le S initial est un entier de 64 bits généré aléatoirement.
    La taille des morceaux et le nombre de rounds sont paramétrables.
    """
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

for i in range(100, 110) :
    print(f"Valeur de la sbox pour {i} : {sbox(i)}")