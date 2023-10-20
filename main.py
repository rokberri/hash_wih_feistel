from feistel_net import encryption, decryption,decode, encode
from binary_operations import *
import random
from hash_function import hash_function


def f(m0, m1, round_key):
    result = xor(xor(cyclic_shift(m0, -2), inversion(cyclic_shift(m1, 9))), round_key)
    return result

def random_key(length):
   letters = ['0', '1']
   return ''.join(random.choice(letters) for i in range(length))

def test_feistel_net():
    
    file = open("text.txt", "r", encoding='utf-8')
    file_text = file.read()
    file.close()
    print(file_text)

    bin_text = ''.join(encode(file_text))

    if len(bin_text) < 64:
        bin_text = bin_text.zfill(64 )

    print('Изначальный текст   ', bin_text)
    secret_key = random_key(64)
    en = encryption(bin_text, secret_key,f)
    print('Зашифрованный текст ', en)
    dec = decryption(en, secret_key, f)
    print('Расшифрованный текст', dec)
    print(decode(dec))

def test_hash_func():
    file = open("text.txt", "r", encoding='utf-8')
    file_text = file.read()
    file.close()
    # print(file_text)

    bin_text = ''.join(encode(file_text))

    if len(bin_text) < 64:
        bin_text = bin_text.zfill(64 )

    # print('Изначальный текст   ', bin_text)
    secret_key = random_key(64)
    en = hash_function(bin_text, f)
    print('Зашифрованный текст ', en)



if __name__ == '__main__':
    # test_feistel_net()
    test_hash_func()