from binary_operations import *

def encode(s): # ['0000000001101011', '0000010000011011']
    # ''.join(list(map(lambda x: "{0:b}".format(ord(x)).zfill(16), s)))
    return list(map(lambda x: "{0:b}".format(ord(x)).zfill(16), s))


def decode(bins):
    str = ""
    for i in range(0, len(bins), 16):
        binc = bins[i:i + 16]
        if binc != '0000000000000000':
            num = int(binc, 2)
            str += chr(num)
    return str



def round_key(key, i):
    round_key = xor(cyclic_shift(key, -(i*3))[-16::], (inversion(key))[-16::])
    return round_key

def encryption(text, key,f):
    result = ''
    for i in range(len(text)):
        if len(text) > 64:
            block = text[:64]
            text = text[64:len(text)]
            m0 = block[0:16]
            m1 = block[16:32]
            m2 = block[32:48]
            m3 = block[48:64]

            n = 10
            for i in range(n):
                c0 = xor(m3, f(m0, m1, round_key(key, i)))
                c1 = xor(m2, c0)
                c2 = m0
                c3 = xor(m1, m0)
                m0 = c0
                m1 = c1
                m2 = c2
                m3 = c3

            cipher = c0 + c1 + c2 + c3
            result = result+cipher
        else:
            block = text
            if len(block) < 64:
                block = block.zfill(64)

            m0 = block[0:16]
            m1 = block[16:32]
            m2 = block[32:48]
            m3 = block[48:64]

            n = 10
            for i in range(n):
                c0 = xor(m3, f(m0, m1, round_key(key, i)))
                c1 = xor(m2, c0)
                c2 = m0
                c3 = xor(m1, m0)
                m0 = c0
                m1 = c1
                m2 = c2
                m3 = c3

            cipher = c0 + c1 + c2 + c3
            result = result+cipher
            break

    return result


def decryption(text, key, f):
    result = ''
    for i in range(len(text)):
        block = text[:64]
        text = text[64:len(text)]
        c0 = block[0:16]
        c1 = block[16:32]
        c2 = block[32:48]
        c3 = block[48:64]

        n = 10
        for i in range(n):
            m0 = c2
            m1 = xor(c3, m0)
            m2 = xor(c1, c0)
            m3 = xor(c0, f(m0, m1, round_key(key, n-1-i)))
            c0 = m0
            c1 = m1
            c2 = m2
            c3 = m3

        decr = m0 + m1 + m2 + m3
        result = result+decr

    return result