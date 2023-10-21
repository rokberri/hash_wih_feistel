from feistel_net import encode,decode,encryption,decryption
from binary_operations import *

# Функция деления всей битовой строки на блоки заданного размера, просто для удобства итераций
def split_into_blocks(bins:str, size=64)->list[str]:
    list_of_blocks = list()
    tmp = ''
    for el in bins:
        tmp += el
        if len(tmp) == size: 
            list_of_blocks.append(tmp)
            tmp = ''
    return list_of_blocks 

# Хеш-функция
def hash_function(bins:str,f, use_fin_func=False)->str:
    # Начальный вектор инициализации(считай секретный ключ)
    IV = '1101110110111010110001001101001000000010110110101000111010100010'
    hash_code = ''
    blocks_of_bins = split_into_blocks(bins)
    # Для каждого блока по 64 бита
    for block in blocks_of_bins:
        # если это первый блок, ксорим его с вектором инициализации по схеме
        if len(hash_code) == 0:
            hash_code = xor(block,IV)
            hash_code = encryption(hash_code, IV, f)
            hash_code = xor(hash_code, block)
        else:
            # если не первый - то ксорим с предыдущим результатом, опять же по схеме
            prev_hash = hash_code
            hash_code = xor(block,prev_hash)
            hash_code = encryption(hash_code, prev_hash, f)
            hash_code = xor(hash_code, block)
    # Ну и если нам нужно усечь значение хеш-функции усекаем или выводим как есть
    if use_fin_func:
        return finalization_func(hash_code)
    else:
        return hash_code

# Функция финализации(по факту просто берет какое-то количество бит хеша вместо полгого хеша)
def finalization_func(hash_code:str)->str:
    return hash_code[56:64]