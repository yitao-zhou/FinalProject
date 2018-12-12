def de_swt(code_str, offset):

    text = str()
    idx = 0
    while True:
        try:
            text += code_str[idx]
            idx += offset
        except:
            break
    return text


def swt(plain_text_msg, offset):
    ''' Switch encription '''
    plain_array = list(plain_text_msg)
    cipher_array = []
    i = 0
    while i < len(plain_text_msg):
        cipher_array.append(plain_array[i])
        for k in range(offset - 1):
            noise = chr(random.randrange(32, 127))
            cipher_array.append(noise)
        i += 1
    cipher_text = ''
    cipher_text = cipher_text.join(cipher_array)
    return cipher_text


if __name__ == '__main__':
    print(de_swt('`[L;)93>zA/:tTXzIe4T+n$kq +YzF]OTR-R', 12))
