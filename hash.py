from sbox import sbox

def chunk_binary(string, length):
    return [int(string[i:length+i].zfill(length), 2) for i in range(0, len(string), length)]

def hash(message : int) -> int :
    """
    Calcule le hash d'un message de taille quelconque, selon la construction de Merkle–Damgård.
    Pour la fonction, nous utilisons une construction du type Davies–Meyer, avec la 
    fonction f(M, S) = sbox(M ^ S) ^ S
    Le S initial est un entier de 64 bits généré aléatoirement.
    La taille des morceaux et le nombre de rounds sont paramétrables.
    """
    chunk_size = 64
    rounds = 5

    binary_message = bin(message)[2:]
    message_chunks = chunk_binary(binary_message, chunk_size)

    state = 0b0111000110010001001111000000111011100001010010100101100001100010
    
    for chunk in message_chunks :
        for _ in range(rounds) :
            # print(state)
            state = sbox(chunk ^ state) ^ state
        # final_message += bin(int_message)[2:]

    return state

for i in range(100, 110) :
    print(f"Valeur de la sbox pour {i} : {sbox(i)}")