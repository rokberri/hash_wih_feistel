import random


file = open(r"C:\Users\Анастасия\PycharmProjects\kript\task1\text.txt", "r", encoding='utf-8')
file_text = file.read()
file.close()
print(file_text)


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


bin_text = ''.join(encode(file_text))
# print(start)

if len(bin_text) < 64:
    bin_text = bin_text.zfill(64 )

print('Изначальный текст   ', bin_text)
# print(len(bin_text))


def inversion(text):
    new_text = ''
    for i in range(len(text)):
        if text[i] == '0':
            new_text = new_text + '1'
        elif text[i] == '1':
            new_text = new_text + '0'
    return new_text


def xor(x1, x2):
    new_str = ''
    for i in range(len(x1)):
        if x1[i] == '0' and x2[i] == '0':
            new_str = new_str + '0'
        elif x1[i] == '0' and x2[i] == '1':
            new_str = new_str + '1'
        elif x1[i] == '1' and x2[i] == '0':
            new_str = new_str + '1'
        elif x1[i] == '1' and x2[i] == '1':
            new_str = new_str + '0'
    return new_str


def f(m0, m1, round_key):
    result = xor(xor(cyclic_shift(m0, -2), inversion(cyclic_shift(m1, 9))), round_key)
    return result


def cyclic_shift(m, step):
    m = m[-step:] + m[:-step]
    return m


def random_key(length):
   letters = ['0', '1']
   return ''.join(random.choice(letters) for i in range(length))


key = random_key(64)
# print(key)
iv = random_key(64)
# print('вектор инициализации:')
# print(iv)


def round_key(key, i):
    round_key = xor(cyclic_shift(key, -(i*3))[-16::], (inversion(key))[-16::])
    return round_key


def encryption(text):
    result = ''
    k = 0
    for i in range(len(text)):
        if len(text) > 64:
            block = text[:64]
            k += 1

            if k == 1:
                block = xor(iv, block)
            else:
                block = xor(block, cipher)

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
            k += 1
            if len(block) < 64:
                block = block.zfill(64)

            if k == 1:
                block = xor(iv, block)
            else:
                block = xor(block, cipher)

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


def decryption(encr_text):
    result = ''
    k = 0
    for i in range(len(encr_text)):
        k+=1
        block = encr_text[:64]
        encr_text = encr_text[64:len(encr_text)]
        if len(block) < 64:
            break
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
        if k == 1:
            decr2 = xor(iv, decr)
            last = block
        else:
            decr2 = xor(decr, last)
            last = block

        result = result+decr2

    return result


print('Зашифрованный текст ', encryption(bin_text))
en = encryption(bin_text)
print('Расшифрованный текст', decryption(en))
dec = decryption(en)
print(decode(dec))
