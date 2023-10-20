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

def cyclic_shift(m, step):
    m = m[-step:] + m[:-step]
    return m