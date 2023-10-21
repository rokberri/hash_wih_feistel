from feistel_net import encode,decode,encryption,decryption
from binary_operations import *


def split_into_blocks(bins:str, size=64)->list[str]:
    list_of_blocks = list()
    tmp = ''
    for el in bins:
        tmp += el
        if len(tmp) == size: 
            list_of_blocks.append(tmp)
            tmp = ''
    return list_of_blocks 

def hash_function(bins:str,f, use_fin_func=False)->str:
    IV = '1101110110111010110001001101001000000010110110101000111010100010'
    hash_code = ''
    blocks_of_bins = split_into_blocks(bins)
    for block in blocks_of_bins:
        if len(hash_code) == 0:
            hash_code = xor(block,IV)
            hash_code = encryption(hash_code, IV, f)
            hash_code = xor(hash_code, block)
        else:
            prev_hash = hash_code
            hash_code = xor(block,prev_hash)
            hash_code = encryption(hash_code, prev_hash, f)
            hash_code = xor(hash_code, block)
    if use_fin_func:
        return finalization_func(hash_code)
    else:
        return hash_code


def finalization_func(hash_code:str)->str:
    return hash_code[56:64]