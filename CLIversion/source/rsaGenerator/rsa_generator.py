import random
import sympy
from source.rsaGenerator.trng_generator import *
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


# Greatest common divisor function
def gcd(a, b):
    if b > 0:
        return gcd(b, a % b)
    return a


# Inverse modulo m of a
def find_mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


# Calculate the variable that has key_len (bits) using the list of random data generated by the trng generator
def pq_generator(key_len, audio_trng_data):
    x = 0
    for i in range(int(key_len / 8)):
        number = audio_trng_data[random.randint(0, len(audio_trng_data)) - 1]
        if i == 0:
            while number < 128:
                number = audio_trng_data[random.randint(0, len(audio_trng_data)) - 1]
            x = number
        else:
            x = (x << 8) | number

    x = sympy.prevprime(x)

    if x.bit_length() == key_len:
        return x
    else:
        pq_generator(key_len, audio_trng_data)


# Generate public and private RSA key that has key_len (bits) using the list of random data generated by the trng generator
def rsa_generator(key_len, audio_trng_data):
    p = pq_generator(key_len, audio_trng_data)
    q = pq_generator(key_len, audio_trng_data)
    n = p * q
    phiN = (p - 1) * (q - 1)

    while True:
        e = random.randrange(1, phiN)
        g = gcd(e, phiN)
        if g == 1:
            break

    d = find_mod_inverse(e, phiN)

    # publicKey = (n, e)
    # privateKey = (n, d)

    publicKey = rsa.RSAPublicNumbers(
        e=e,
        n=n,
    ).public_key()

    privateKey = rsa.RSAPrivateNumbers(
        p=p,
        q=q,
        d=d,
        dmp1=d % (p - 1),
        dmq1=d % (q - 1),
        iqmp=pow(q, -1, p),
        public_numbers=rsa.RSAPublicNumbers(e=e, n=n),
    ).private_key()

    return publicKey, privateKey


# Convert the raw private key to PEM form
def pem_rsa_private_key(privateKey):
    pem_private_key = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return pem_private_key


# Convert the raw public key to PEM form
def pem_rsa_public_key(publicKey):
    pem_public_key = publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return pem_public_key