def encrypt_caesar(plaintext: str) -> str:
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


def decrypt_caesar(plaintext: str) -> str:
    """
        >>> decrypt_caesar("SBWKRQ")
        'PYTHON'
        >>> decrypt_caesar("sbwkrq")
        'python'
        >>> decrypt_caesar("Sbwkrq3.6")
        'Python3.6'
        >>> decrypt_caesar("")
        ''
        """
    ciphertext = ""

    code_dict = {'a': 'x', 'A': 'X', 'b': 'y', 'B': 'Y', 'c': 'z', 'C': 'Z'}

    for c in plaintext:
        if c == "a" or c == "A" or c == "b" or c == 'B' or c == "c" or c == "C":
            ciphertext += code_dict[c]
        else:
            ciphertext += change_symbol(c, -3)

    return ciphertext


def change_symbol(ch: str, shift: int) -> bool:
    icode = ord(ch)
    if (icode >= ord('a') and icode <= ord('z')) or \
            (icode >= ord('A') and icode <= ord('Z')):
        return (chr(icode + shift))
    else:
        return ch
