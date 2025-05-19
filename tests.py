import tqdm as tqdm

def block_encrypt(key, m) :
    c = 0
    return c

def block_decrypt(key, c) :
    m = 0
    return m

def nbre_branche_diff(L) :
    """ 
    Permet de calculer le nombre de branches différentielles
    N est le nombre de bits que L va prendre en entrée 
    L est la matrice que l'on va tester
    On à maximiser Bd(L)
    """
    N = len(L[0])
    min = 2*N #N bits en sortie et en entrée de L
    for k in range(1, 2**N) : 
        bits_1 = k.bit_count() + L_eval(L, k).bit_count()
        if bits_1 < min :
            min = bits_1
    return min
    
def L_matrice(first_row) :
    """ 
    Permet de définir une matrice circulante, dont la première ligne est first_row
    first row est un str
    """
    N = len(first_row)
    L = [first_row[i:] + first_row[:i] for i in range(N)]
    return L

def L_eval(L, x) :
    """ 
    Calcule Lx 
    """
    X = format(x, "b")
    result = 0
    for k in range(len(X)) :
        if X[k] == "1" :
            entier = int(L[k], 2)
            result = result ^ entier
    return result      

#L = L_matrice("1110" ) 
#print(nbre_branche_diff(L))

# def chiffre(dico) :
#     a = dico[(0, 0)]
#     b = dico[(0, 1)]
#     c = dico[(1, 0)]
#     d = dico[(1, 1)]
#     chiffre = ""
#     while a >= c :
#         chiffre = chiffre + "0"
#         a = a - 1
#     if b > 0 :
#         chiffre = chiffre + "1" 
#         b = b - 1
#     while d >= b :
#         chiffre = chiffre + "1" 
#         d = d - 1
#     if c > 0 :
#         chiffre = chiffre + "0"
#         c = c - 1
#     while b > 0 or c > 0 :
#         if chiffre[-1] == "0" :
#             chiffre += "1"
#             b = b-1
#         if chiffre[-1] == "1" :
#             chiffre += "0"
#             c = c-1
    
#     return chiffre

# def test_dico(N) :
#     big_set = set()
#     petit_dico = {"00" : 0, "01" : 0, "10" : 0, "11" : 0 }
#     a_tester = []
#     petit_dico_k = {}
#     for k in range(2, 2**N) :
#         print(k)
#         bin = format(k, "b")
#         petit_dico_k = petit_dico
#         for i in range(len(bin)-1) :
#             petit_dico_k[bin[i:i+2]] +=1 
#         petit_dico_k[bin[-1] + bin[0]] +=1
#         if petit_dico_k not in big_set :
#             big_set.add(petit_dico_k)
#             a_tester.append(format(k, "b"))
#     return a_tester

# print(test_dico(4)) 

#a_tester = ["1111", "1110", "1100", "1010", "1000", "0000"]
a_tester = [format(k, "b") for k in range(2**16)]
#a_tester = ["000111100", "0"*5 + "1"*4, ""]

#Trouver comment définir a_tester facilement sur N bits et voir si on a une tendance qui se dégage (aller jusqu'à 16 bits par exemple)


max_BdL = 0
row_max = ""
for row in tqdm.tqdm(a_tester) :
    L = L_matrice(row) 
    BdL= nbre_branche_diff(L)
    if BdL > max_BdL : 
        max_BdL = BdL 
        row_max = row
            
print(max_BdL, row_max)    
