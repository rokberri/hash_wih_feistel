from feistel_net import encryption, decryption,decode, encode
from binary_operations import *
import random
from hash_function import hash_function


def read_data_from_file(filepath='text.txt')->str:
    file = open("text.txt", "r", encoding='utf-8')
    file_text = file.read()
    file.close()
    return file_text

def get_binary_data(data:str):
    bin_text = ''.join(encode(data))
    if len(bin_text) < 64:
        bin_text = bin_text.zfill(64 )
    return bin_text
    
def f(m0, m1, round_key):
    result = xor(xor(cyclic_shift(m0, -2), inversion(cyclic_shift(m1, 9))), round_key)
    return result

def random_key(length):
   letters = ['0', '1']
   return ''.join(random.choice(letters) for i in range(length))

def test_feistel_net():
    file_text = read_data_from_file()
    print(file_text)

    bin_text = get_binary_data(file_text)

    print('Изначальный текст   ', bin_text)
    secret_key = random_key(64)
    en = encryption(bin_text, secret_key,f)
    print('Зашифрованный текст ', en)
    dec = decryption(en, secret_key, f)
    print('Расшифрованный текст', dec)
    print(decode(dec))

def test_hash_func():
    file_text = read_data_from_file()
    # print(file_text)
    bin_text = get_binary_data(file_text)

    print('Изначальный текст   ', bin_text)
    secret_key = random_key(64)
    en = hash_function(bin_text, f,USE_FINALISATION_FUNCTION)
    print('Зашифрованный текст ', en)

def generate_text(length:int)->str:
    ALPH =list("""0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя""")
    text = ''
    for i in range(length):
        text += random.choice(ALPH)
    return text

def searching():
    pass


def searching_for_collisions():
    file_text = read_data_from_file()
    bin_text = get_binary_data(file_text)
    origin_hash = hash_function(bin_text,f, USE_FINALISATION_FUNCTION)
    list_of_words = file_text.split()
    print(origin_hash)
    for i in range(len(list_of_words)):
        for j in range(257):
            new_word = chr(j)
            # list_of_words[i] = new_word
            list_of_sim = list(file_text)
            if not list_of_sim[i] == new_word:
                list_of_sim[i] = new_word
            else: 
                break
            bin_text = get_binary_data(''.join(list_of_sim))
            new_hash = hash_function(bin_text,f, USE_FINALISATION_FUNCTION)
            if origin_hash == new_hash:
                print(f"{new_word},{i}")
                print(''.join(list_of_sim))


USE_FINALISATION_FUNCTION = True

def find_collisions():
    hash_dict = {}
    i = 0
    while True:
        text = str(i)  # Используем целое число в качестве открытого текста
        bin_text = get_binary_data(text)
        hash_code = hash_function(bin_text,f,USE_FINALISATION_FUNCTION)
        
        if hash_code in hash_dict:
            # Если хеш-код уже присутствует в словаре, значит мы нашли пару текстов с одинаковым хеш-кодом
            print(bin_text)
            return (text, hash_dict[hash_code])
        
        # Добавляем текущий хеш-код в словарь для дальнейшего сравнения
        hash_dict[hash_code] = text
        
        i += 1

if __name__ == '__main__':
    # test_feistel_net()
    
    test_hash_func()
   
    # collisions = find_collisions()
    # print("Первый текст:", collisions[0],'HASH:',hash_function(get_binary_data(collisions[0]),f,USE_FINALISATION_FUNCTION))
    # print("Второй текст:", collisions[1],'HASH:',hash_function(get_binary_data(collisions[1]),f,USE_FINALISATION_FUNCTION))
   
    # searching_for_collisions()
