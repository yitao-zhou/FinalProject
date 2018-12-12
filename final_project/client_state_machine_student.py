"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json


class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action": "connect", "target": peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        # print(response)
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action": "disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                # if my_msg == 'q':
                #     self.out_msg += 'See you next time!\n'
                #     self.state = S_OFFLINE

                if my_msg == 'time':
                    mysend(self.s, json.dumps({"action": "time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action": "list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg == 'menu':
                    self.out_msg += menu

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if peer == self.get_myname():
                        self.out_msg += 'You can\'t connect to yourself!\n'
                    else:
                        if self.connect_to(peer) == True:
                            self.state = S_CHATTING
                            self.out_msg += 'You are connected to ' + peer + '. Chat away!\n\n'
                            self.out_msg += '-----------------------------------\n'

                        else:
                            self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "search", "target": term}))
                    search_rslt = json.loads(myrecv(self.s))["results"][1:].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p':
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "poem", "target": poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"][1:].strip()
                    if (len(poem) > 0):
                        self.out_msg += poem
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                elif my_msg[:5] == 'admin':
                    mysend(self.s, json.dumps({"action": "admin", "password": my_msg[5:].strip()}))
                elif my_msg[:5] == 'reset':
                    mysend(self.s, json.dumps({"action": "reset", "password": my_msg[5:].strip()}))
                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                # print('peer_msg in S_LOGGEDIN', peer_msg)
                if peer_msg["action"] == "connect":
                    #----------------Self Implemented--------------#
                    peer = peer_msg['from'].strip()
                    self.out_msg += 'Request from ' + peer + '\n'
                    self.out_msg += 'You are connected with ' + peer.rstrip() + '. Chat away!\n\n'
                    self.out_msg += '-----------------------------------\n'
                    self.state = S_CHATTING

                if peer_msg["action"] == "admin":
                    attempt_person = peer_msg['person'].strip()
                    admin_result = peer_msg['results']
                    if admin_result:
                        self.out_msg += attempt_person + ' has joined the administor team!\n\n'
                    else:
                        self.out_msg += attempt_person + ' has tried to join the administor team but failed!\n\n'

                if peer_msg["action"] == "reset":
                    attempt_person = peer_msg['person'].strip()
                    reset_result = peer_msg['results']
                    if reset_result:
                        self.out_msg += attempt_person + ' has changed his or her password!\n\n'
                    else:
                        self.out_msg += attempt_person + ' has tried to change his or her password but failed!\n\n'

                    #==============================================================================
                    # Start chatting, 'bye' for quit
                    # This is event handling instate "S_CHATTING"
                    #==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                # print('my msg after connection:', text_proc(my_msg, self.me))
                mysend(self.s, json.dumps({"action": "exchange", "from": "[" + self.me + "]", "message": my_msg}))

                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''

            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)

                if peer_msg['action'] == 'connect' and peer_msg['status'] == 'request':
                    peer = peer_msg['from'].strip()
                    self.out_msg += '( ' + peer + ' joined )\n'

                elif peer_msg['action'] == 'exchange':
                    self.out_msg += peer_msg['message']
                    if peer_msg['message'][:5] != 'Admin':
                        self.out_msg = peer_msg['from'] + ' ' + self.out_msg

                elif peer_msg['action'] == 'disconnect':
                    self.out_msg += 'You are disconnected from ' + self.peer + '\n'
                    self.state = S_LOGGEDIN
                    self.peer = ''

                elif peer_msg["action"] == "admin":
                    attempt_person = peer_msg['person'].strip()
                    admin_result = peer_msg['results']
                    if admin_result:
                        self.out_msg += attempt_person + ' has joined the administor team!\n\n'
                    else:
                        self.out_msg += attempt_person + ' has tried to join the administor team but failed!\n\n'

            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            # self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
