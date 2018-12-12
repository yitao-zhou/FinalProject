import random

''' Caesar encription '''

def enc(plain_text_msg, offset):
    cipher_text = ""
    i = 0
    while i < len(plain_text_msg):
        chrctr = plain_text_msg[i]
        code_of_replacement = (ord(chrctr) + offset)%128
        replacement = chr(code_of_replacement)
        cipher_text = cipher_text + replacement
        i += 1

    return cipher_text

def dec(cipher_text_msg, offset):
    plain_text = enc(cipher_text_msg, -offset)
    return plain_text

    ''' Switch encription '''

def swt(plain_text_msg, offset):
    plain_array = list(plain_text_msg)
    cipher_array = []
    i = 0
    while i < len(plain_text_msg):
        cipher_array.append(plain_array[i])
        for k in range(offset-1): 
            noise = chr(random.randrange(32,127))
            cipher_array.append(noise)
        i += 1
    cipher_text = ''
    cipher_text =  cipher_text.join(cipher_array)
    return cipher_text

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

    ''' Serial encription [C,S,C,S,_,_,_,_] '''

def serial_encrypt(plain_msg,keyNum):
    keyString = bin(keyNum)[2:10]#note keyNum has to be greater equal than 128 to generate 
    #print('keyString',keyString)
    formerPart = list(keyString[:4])
    
    laterPart = keyString[4:]

    offset_addon = int(laterPart, 2)
    #print('offset_addon',offset_addon)
    offset = 3 + offset_addon
    i = 0
    msg = plain_msg
    for status in formerPart:
        if status == '1':
            if i%2 == 0:
                msg = enc(msg,offset)
                #print(i,'enc',msg)
            else:
                msg = swt(msg,offset)
                #print(i,'swt',msg)
        elif status == '0':
            #print('zero')
            pass
        i += 1    
    return msg


def serial_decrypt(code, decy_code):
    bin_command = bin(decy_code)[2:10]
    offset_str = bin_command[4:]
    offset = 3 + int(offset_str, 2)
    cmd = bin_command[3::-1]

    for i in range(4):
        if cmd[i] == '1':
            if int(i) % 2 == 0:
                code = de_swt(code, offset)
            else:
                code = dec(code, offset)
    return code

''' Possible hacker attach method '''
def break_enc_brute(cipher_text, threshold):
    ''' Semi-automatic Caesar decryption when we DON'T know the offset
       (when we don't know the shared secret)
       '''
    #common = ["def", "while", "for", "print(", "return"]
    common = ["There ","You "," you "," I "," is "," are ","The "," the "," a ","This "," this ","What ","When ","How ","Where "]
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
'''
break_enc_brute("_`a\x1bn`g`^onjmo#gno$5\x05\x1b\x1b\x1b\x1bjpo\x1b8\x1bVX\x05\x1b\x1b\x1b\x1bi\x1b8\x1bg`i#gno$\x05\x1b\x1b\x1b\x1bajm\x1bd\x1bdi\x1bm\\ib`#i$5\x05\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1bh\x1b8\x1bhdi#gno$\x05\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1bgno)m`hjq`#h$\x05\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1bjpo\x1b8\x1bjpo\x1b&\x1bVhX\x1b\x1ejpo\x1b&8\x1bVhX\x05\x1b\x1b\x1b\x1bm`opmi\x1bjpo", 1)
'''