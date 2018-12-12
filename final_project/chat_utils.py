import socket
import time
import encryption


CHAT_IP = socket.gethostbyname(socket.gethostname())
CHAT_PORT = 1113
SERVER = (CHAT_IP, CHAT_PORT)

menu = "++++ Choose one of the following commands\n \
        c _peer_: to connect to the _peer_ and chat\n \
        ? _term_: to search your chat logs where _term_ appears\n \
        Explore more tools in the menu! \n\n"

'''q: to leave the chat system\n'''

S_OFFLINE = 0
S_CONNECTED = 1
S_LOGGEDIN = 2
S_CHATTING = 3

SIZE_SPEC = 5

CHAT_WAIT = 0.2


def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_CONNECTED:
        print('Connected')
    elif state == S_LOGGEDIN:
        print('Logged in')
    elif state == S_CHATTING:
        print('Chatting')
    else:
        print('Error: wrong state')


def mysend(s, msg):
    msg = encryption.serial_encrypt(msg, 191)
    # print(msg)

    # append size to message and send it
    msg = ('0' * SIZE_SPEC + str(len(msg)))[-SIZE_SPEC:] + str(msg)
    msg = msg.encode()
    total_sent = 0
    while total_sent < len(msg):
        sent = s.send(msg[total_sent:])
        if sent == 0:
            print('server disconnected')
            break
        total_sent += sent


def myrecv(s):
    # receive size first
    size = ''
    while len(size) < SIZE_SPEC:
        text = s.recv(SIZE_SPEC - len(size)).decode()
        if not text:
            print('disconnected')
            return('')
        size += text
    size = int(size)
    # now receive message
    msg = ''
    while len(msg) < size:
        text = s.recv(size - len(msg)).decode()
        if text == b'':
            print('disconnected')
            break
        msg += text
    #print ('received '+message)
    # print(msg)
    msg = encryption.serial_decrypt(msg, 191)
    return (msg)


def text_proc(text, user):
    ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    return('(' + ctime + ') ' + user + ' : ' + text)  # message goes directly to screen
