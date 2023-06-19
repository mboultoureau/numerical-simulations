# Chiffrement RSA
## Exponention rapide

import time

# Algorithme naïf
def basic_pow(n, p):
    res = 1
    for i in range(p):
        res *= n
    return res

# Algorithme d'exponentiation rapide
def fast_pow(n, p):
    res = 1
    # On divise consécutivement p par 2 jusqu'à ce que p soit nul
    while p > 0:
        # Si p est impair, on multiplie le résultat par n
        if p % 2 == 1:
            res *= n
        # On divise p par 2 et on multiplie n par lui-même
        n *= n
        p //= 2
    return res

# Fonction qui calcule les performances d'une fonction
def performance(func, nb, n, p):
    start_time = time.perf_counter()
    for i in range(nb):
        func(n, p)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print("Temps d'exécution de l'algorithme : %s secondes" % execution_time)

# Tests des algorithmes
assert basic_pow(3, 9) == 19683
assert fast_pow(3, 9) == 19683

# Comparaison des performances
# performance(basic_pow, 10, 2, 1000000)
# performance(fast_pow, 10, 2, 1000000)





## Calcul des coefficients de Bézout
def bezout_coeff(a, b):
    # Algorithme d'Euclide étendue
    r, u, v, r_prime, u_prime, v_prime = a, 1, 0, b, 0, 1
    while r_prime != 0:
        q = r // r_prime
        r, u, v, r_prime, u_prime, v_prime = r_prime, u_prime, v_prime, r - q * r_prime, u - q * u_prime, v - q * v_prime
    return u, v, r

assert(bezout_coeff(123, 456) == (-63, 17, 3))



## Chiffrement RSA
## Calcul de la clé publique et chiffrement

import math
import random

# Fonction qui vérifie si un nombre est premier
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

assert(is_prime(2) == True)
assert(is_prime(3) == True)
assert(is_prime(4099) == True)
assert(is_prime(4098) == False)

# Fonction qui calcule le PGCD de deux nombres
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

assert(pgcd(123, 456) == 3)

# Génération de nombres premiers
def generate_prime():
    p = random.randint(100, 1000)
    while not is_prime(p):
        p = random.randint(100, 1000)
    return p

assert(is_prime(generate_prime()) == True)
assert(is_prime(generate_prime() + 1) == False)

# Génération des clés
def generate_keys(p, q):
    # Vérification que p et q sont premiers
    assert(is_prime(p))
    assert(is_prime(q))
    assert(p != q)

    n = p * q
    phi = (p - 1) * (q - 1)

    # On choisit un entier e tel pgcd(e, phi) = 1
    e = random.randint(2, phi - 1)
    while pgcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # On calcule d tel que e * d = 1 (mod phi)
    d = bezout_coeff(e, phi)[0]
    if d < 0:
        d += phi

    # On retourne la clé publique et la clé privée
    return (e, n), (d, n)

# Chiffrement
def encrypt(public_key, message):
    e, n = public_key
    return fast_pow(message, e) % n

# Déchiffrement
def decrypt(private_key, message):
    d, n = private_key
    return fast_pow(message, d) % n

# Test de chiffrement et déchiffrement avec des nombres aléatoires
p = generate_prime()
q = generate_prime()

while p == q:
    q = generate_prime()

message = 10
public_key, private_key = generate_keys(p, q)

encrypted_message = encrypt(public_key, message)
decrypted_message = decrypt(private_key, encrypted_message)

print("P : %s" % p)
print("Q : %s" % q)
print("Message : %s" % message)
print("Clé publique : %s" % str(public_key))
print("Clé privée : %s" % str(private_key))
print("Message chiffré : %s" % encrypted_message)
print("Message déchiffré : %s" % decrypted_message)

assert(message == decrypted_message)