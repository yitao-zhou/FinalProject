import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine_student as csm

import threading


class Client:
    def __init__(self, args):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''    # All the messages that are printed in the user interface
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        # svr = ('10.209.5.117', 1118)
        self.socket.connect(svr)

        print(svr)

        self.sm = csm.ClientSM(self.socket)

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        # peer_code = M_UNDEF    for json data, peer_code is redundant
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    def output(self):
        self.msg = self.system_msg
        self.system_msg = ''
        return self.msg

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if len(my_msg) > 0:
            self.name = my_msg
            msg = json.dumps({"action": "login", "name": self.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'okay':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)

                self.system_msg += 'Welcome, ' + self.name + '!\n'

                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:
            return(False)

    def input_instruction(self, text):
        self.console_input.append(text)

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self, username):
        self.init_chat()
        self.system_msg += 'Welcome to SOS Chat ' + username + '\n'


#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)
