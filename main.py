from feistel_net import encryption, decryption,decode, encode
from binary_operations import *
import random
from hash_function import hash_function

# В краце что я поменял в твоем коде. 
# 1) Раскидал функционал по файликам(вся шифрация в один, битовые операции в друго и тд)
# 2) Изменил сигнатуру сети Фейстеля. На вход теперь подается битовая последовательность
#     + функиця для шифрации (f) + булевая константа, которая определяет использовать ли функцию финализации
# 3) Вынес повторяющийся код в отдельные функции (например то, где ты файл читаешь)

# ------------------------Блок твоего кода, просто слегка измененный---------------------------------------
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
# ---------------------------------------------------------------------------------------------------------

# Просто переписанный в функцию код из твоего 1 таска, проверяет работоспособность сети Фейстеля
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

# Функция для теста хеш-функции, сама реализация в файлике я hash_function
# По факту это первое задание из 3 в 3 таске
def test_hash_func():
    file_text = read_data_from_file()
    bin_text = get_binary_data(file_text)
# По логике тут все так же, как в шифровании сетью Фейстеля, просто используем в одном месте другую функцию
# Ну и результат хеш-функции нельзя преобразовать обратно, так что декода нет
    print('Изначальный текст   ', bin_text)
    secret_key = random_key(64)
    en = hash_function(bin_text, f,USE_FINALISATION_FUNCTION)
    print('Зашифрованный текст ', en)

# Второе задание. 
# Функция для поиска коллизий(два различных текста, дающие одинаковый хеш)
def find_collisions():
    # Задаем словарь для храниния пар хеш-открытый текст
    hash_dict = {}
    i = 0
    # Бесконечный цикл
    while True:
        # Используем целое число в качестве открытого текста
        # Нужно для упрощения, потому что по факту любая битовая последовательность 
        # может быть преобразована в число
        text = str(i)  
        # Тут получаем битовое представление числа
        bin_text = get_binary_data(text)
        # Получаем его хеш
        hash_code = hash_function(bin_text,f,USE_FINALISATION_FUNCTION)
        # Если хеш-код уже присутствует в словаре, значит мы нашли пару текстов с одинаковым хеш-кодом
        if hash_code in hash_dict:
            print(bin_text)
            return (text, hash_dict[hash_code])
        
        # Добавляем текущий хеш-код в словарь для дальнейшего сравнения
        hash_dict[hash_code] = text
        # Увеличиваем число
        i += 1


# Третье задание
# Функция для поиска текста, который бы имел отличие не более чем в одном слове
# По факту кстати это задания на поиск коллизий разного рода
# Разница в количестве различающихся знаков, если интересно, спроси, это текстом долго писать)
def searching_for_collisions():
    # Читаем все из файла, переводим в биты и находим оригинальный хеш
    file_text = read_data_from_file()
    bin_text = get_binary_data(file_text)
    origin_hash = hash_function(bin_text,f, USE_FINALISATION_FUNCTION)
    # Делим весь текст на слова
    list_of_words = file_text.split()
    print(origin_hash)
    # Пробуем подставлять все символы на место каждого символа
    # (каждую итерацию меняется один символ) 
    # для конкретно этой функции достаточно перебрать 1 символ, там велик шанс найти коллизию 
    # в целом же нужно перебирать гораздо больше и менять слова на несколько символов
    for i in range(len(file_text)):
        for j in range(257):
            # Получаем новый символ, который подставлять будем
            new_word = chr(j)
            list_of_sim = list(file_text)
            # чтоб не было такого, что мы меняем символ на такой же и получаем тот же хеш
            if not list_of_sim[i] == new_word:
                list_of_sim[i] = new_word
            else: 
                break
            # Собираем строчку обратно после изменения символа
            # И находим ее хеш
            bin_text = get_binary_data(''.join(list_of_sim))
            new_hash = hash_function(bin_text,f, USE_FINALISATION_FUNCTION)
            # Если новая строчка имеет тот же хеш что и оригинальная выводим символ, позицию и новый текст
            if origin_hash == new_hash:
                print(f"{new_word},{i}")
                print(''.join(list_of_sim))

# константа для удобства просто
USE_FINALISATION_FUNCTION = True

if __name__ == '__main__':
    # test_feistel_net()
    
    # test_hash_func()
   
    # collisions = find_collisions()
    # print("Первый текст:", collisions[0],'HASH:',hash_function(get_binary_data(collisions[0]),f,USE_FINALISATION_FUNCTION))
    # print("Второй текст:", collisions[1],'HASH:',hash_function(get_binary_data(collisions[1]),f,USE_FINALISATION_FUNCTION))
   
    searching_for_collisions()
