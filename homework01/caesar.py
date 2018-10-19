def encrypt_caesar(plaintext: str)->str:

    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""

    code_dict = {'x': 'a', 'X': 'A', 'y': 'b', 'Y': 'B', 'z': 'c', 'Z': 'C'}

    for c in plaintext:
        if c == "x" or c == "X" or c == "y" or c == 'Y' or c == "z" or c == "Z":
            ciphertext += code_dict[c]
        else:
            ciphertext += change_symbol(c, 3)

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE  HERE
    return plaintext

def change_symbol(ch: str, shift: int)->bool:

    icode = ord(ch)
    if (icode >= ord('a') and icode <= ord('z')) or \
        (icode >= ord('A') and icode <= ord('Z')):
        return(chr(icode + shift))
    else:
        return ch
