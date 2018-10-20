import random


def is_prime(n: int)-> int:
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    div = 1
    for i in range(2, n):
        if n % i == 0:
            div = i
    if div == 1:
        return True
    else:
        return False
    # Проверка, простое ли число
    pass

def gcd(a: int, b: int)-> int:

    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    gcd = a + b
    return gcd
    # наибольший общий делитель
    pass

def multiplicative_inverse(e: int, phi: int)-> int:

    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.
    >>> multiplicative_inverse(7, 40)
    23
    """
    a = []
    b = []
    x = []
    y = []
    result_lst = []


    #Значение из b переносится в следующую строку a. из a mod b перенос в следующую строку b.
    while e % phi != 0:
        a.append(phi)
        b.append(e)
        result_lst.append(phi//e)
        mod = phi % e
        phi = e
        e = mod

    result_lst.append(0)
    x.append(0)
    y.append(1)

    j = len(result_lst) - 1
    i = 0
    while i < len(result_lst):
        x.append(y[i])
        y.append(x[i] - y[i] * result_lst[j])
        i += 1
        j -= 1

    d = y[i] % a[0]
    return d

def generate_keypair(p: int, q: int)-> int:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # n = pq
    n = p * q

    #phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def encrypt(pk:tuple, plaintext:str)-> int:
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher

def decrypt(pk:tuple, ciphertext:list)-> int:
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)

if __name__ == '__main__':
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))