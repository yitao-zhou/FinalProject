def enc(plain_text_msg, offset):
    ''' Caesar encription '''
    cipher_text = ""
    i = 0
    while i < len(plain_text_msg):
        chrctr = plain_text_msg[i]
        code_of_replacement = (ord(chrctr) + offset) % 128
        replacement = chr(code_of_replacement)
        cipher_text = cipher_text + replacement
        i += 1

    return cipher_text


def swt(plain_text_msg, offset):
    ''' Switch encription '''
    plain_array = list(plain_text_msg)
    cipher_array = []
    i = 0
    while i < len(plain_text_msg):
        here_chr = plain_text_msg[i]
        later_chr = plain_text_msg[i + offset]

        i += 1


def dec(cipher_text_msg, offset):
    plain_text = enc(cipher_text_msg, -offset)
    return plain_text


def break_enc_improved(cipher_text, threshold):
    ''' Semi-automatic Caesar decryption when we DON'T know the offset
       (when we don't know the shared secret)
       '''
    common = ["def", "while", "for", "print(", "return"]
 #   common = ["The","you","is","are"]
    # notice that the space wrapped in the quotation marks are taken into consideration when searching
    possible_offset = 0
    while possible_offset < 128:
        possible_plain_text = dec(cipher_text, possible_offset)
        cnt = 0
        j = 0
        while j < len(common):
            cnt = cnt + possible_plain_text.count(common[j])
            j += 1
        if cnt > threshold:
            print(possible_offset, possible_plain_text, "\n")
        possible_offset += 1
    print("___________________decryption finished___________________")
    print("The 'common' list I used:")
    print(common)


if __name__ == '__main__':
    break_enc_improved("_`a\x1bn`g`^onjmo#gno$5\x05\x1b\x1b\x1b\x1bjpo\x1b8\x1bVX\x05\x1b\x1b\x1b\x1bi\x1b8\x1bg`i#gno$\x05\x1b\x1b\x1b\x1bajm\x1bd\x1bdi\x1bm\\ib`#i$5\x05\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1bh\x1b8\x1bhdi#gno$\x05\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1bgno)m`hjq`#h$\x05\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1bjpo\x1b8\x1bjpo\x1b&\x1bVhX\x1b\x1ejpo\x1b&8\x1bVhX\x05\x1b\x1b\x1b\x1bm`opmi\x1bjpo", 1)

    print(enc('This is a temple', 16))
