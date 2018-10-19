def encrypt_vigenere(plaintext: str, keyword: str)->str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = code_vigenere(plaintext, keyword, 1)

    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str)-> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = code_vigenere(ciphertext, keyword, -1)
    # PUT YOUR CODE HERE
    return plaintext

def code_vigenere(plaintext: str, keyword: str, is_cipher: int) -> str:
    """
    Запуск кода шифр Виженера
    :param plaintext: входная строка
    :param keyword: ключ
    :param is_cipher: знак. 1 - если шифруем, -1 если дешифруем
    :return: зашифрованная строка
    """
    ciphertext = ""
    i = 0
    for idx, ch in enumerate(plaintext):
        # найти новый код лля текущего символа
        if i >= len(keyword):
            i = 0
        code_key = find_shift(keyword[i], ch, is_cipher)
        ciphertext += change_symbol(ch, code_key)
        i = i + 1

    return ciphertext

def find_pos(input_ch: str)->int:
    """
    Найти позицию символа в алфавите
    :param input_ch: символ
    :return: позиция символа
    """
    lst = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",\
           "w", "x", "y", "z"]
    for idx, ch in enumerate(lst):
        if ch.lower() == input_ch.lower():
            return idx
    return -1

def find_shift(key_ch: str, ch: str, is_cipher: int)->int:
    """
    Найти сдвиг в зависимости от позиции входного символа и символа ключа
    :param key_ch: символ ключа
    :param ch: символ строки, которую шифруем
    :param is_cipher: признак, что это шифр
    :return: сдвиг для шифра
    """
    m = find_pos(ch)
    k = find_pos(key_ch)
    if k == -1 or m == -1:
        print("Ошибка в ключе. Должны быть символы")
        return 0
    # по формуле: (позиция вх.символа+ позиция символа ключа) mod 26 - шифроаание
    # (m-k)%26 - дешифрование
    return((m + k*is_cipher)%26)


def change_symbol(ch: str, shift: int)->str:
    """
    Найти сдвиг в зависимости от позиции входного символа и символа ключа
    :param ch: символ строки, которую шифруем
    :param shift: сдвиг для шифра
    :return: символ после ширфа
    """

    i_code = ord(ch)
    i_first = 0;
    if (i_code >= ord('a') and i_code <= ord('z')) or \
        (i_code >= ord('A') and i_code <= ord('Z')):
        # проверка на верхний регистр
        if ch.isupper():
            i_first = ord("A")
        else:
            i_first = ord("a")
        # считаем от первой буквы плюс сдвиг
        return chr(i_first + shift)
    else:
        return ch
