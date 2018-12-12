"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
@revised by: Sunny Song, Oscar Wan
"""

import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp


class Server:
    def __init__(self):
        self.new_clients = []  # list of new sockets of which the user id is not known
        self.logged_name2sock = {}  # dictionary mapping username to socket
        self.logged_sock2name = {}  # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        # initialize past chat indices
        self.indices = {}
        # sonnet
        self.sonnet = indexer.PIndex("AllSonnets.txt")

        self.mute_list = list()
        self.users_info = {}
        self.read_pwd()

    # password
    def read_pwd(self):
        with open('npwd.pickle', 'rb') as handle:
            pwd_dict = pkl.load(handle)
            self.users_info = pwd_dict
            return pwd_dict

    def store_pwd(self):
        pwd_dict = self.users_info
        with open('npwd.pickle', 'wb') as handle:
            pkl.dump(pwd_dict, handle, protocol=pkl.HIGHEST_PROTOCOL)

    def new_client(self, sock):
        # add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        # read the msg that should have login code plus username
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:

                if msg["action"] == "login":
                    name = msg["name"]
                    if self.group.is_member(name) != True:
                        self.new_clients.remove(sock)
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        if name not in self.indices.keys():
                            try:
                                self.indices[name] = pkl.load(
                                    open(name + '.idx', 'rb'))
                            except IOError:  # chat index does not exist, then create one
                                self.indices[name] = indexer.Index(name)
                        print(name + ' logged in')
                        self.group.join(name)
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "okay"}))
                    else:
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print('wrong code received')
            else:
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        # remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx', 'wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

# ==============================================================================
# main command switchboard
# ==============================================================================
    def handle_msg(self, from_sock):
        # read msg code
        msg = myrecv(from_sock)
        if len(msg) > 0:
            # ==============================================================================
            # handle connect request this is implemented for you
            # ==============================================================================
            msg = json.loads(msg)
            if msg['action'] == 'login':
                from_name = self.logged_sock2name[from_sock]
                to_sock = from_sock
                if from_name == 'logger':
                    nn, np = msg['name-pass'].split(',')
                    if nn in self.users_info.keys():
                        if np == self.users_info[nn]:
                            if self.group.is_member(nn) != True:
                                mysend(to_sock, json.dumps({'action': 'login', 'status': 'okay'}))
                                eliminate_sock = self.logged_name2sock['logger']
                                self.logout(eliminate_sock)
                                print('logger be eliminated')
                                print('self.group after eliminating logger: ', self.group)

                            else:
                                mysend(to_sock, json.dumps({'action': 'login', 'status': 'duplicate'}))
                                print(nn + ' duplicate login attempt')
                        else:
                            mysend(to_sock, json.dumps({'action': 'login', 'status': 'incorrect'}))
                            print(nn + ' is a valid user, but gives wrong password')
                    else:
                        mysend(to_sock, json.dumps({'action': 'login', 'status': 'notFound'}))
                        print(nn + ' is not a valid user name, non exist user!')
                else:
                    print('Login request not from logger, alert!')

            elif msg['action'] == 'register':
                from_name = self.logged_sock2name[from_sock]
                to_sock = from_sock
                if from_name == 'logger':
                    nn, np = msg['name-pass'].split(',')
                    if nn not in self.users_info.keys():
                        self.users_info[nn] = np
                        self.store_pwd()
                        mysend(to_sock, json.dumps({'action': 'register', 'status': 'okay'}))
                    else:
                        mysend(to_sock, json.dumps({'action': 'register', 'status': 'duplicate'}))
                        print(nn + ' duplicate register attempt')
                else:
                    print('Register request not from logger, alert!')

            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action": "connect", "status": "self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps(
                        {"action": "connect", "status": "success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps(
                            {"action": "connect", "status": "request", "from": from_name}))
                else:
                    msg = json.dumps(
                        {"action": "connect", "status": "no-user"})
                mysend(from_sock, msg)
# ==============================================================================
# handle messeage exchange: IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                """
                Finding the list of people to send to and index message
                """
                # IMPLEMENTATION
                # ---- start your code ---- #
                pass

                message = msg["message"]
                name = self.logged_sock2name[from_sock]
                msg_time = text_proc(message, name)
                self.indices[name].add_msg_and_index(msg_time)

                # ---- end of your code --- #

                the_guys = self.group.list_me(from_name)[1:]
                for g in the_guys:
                    to_sock = self.logged_name2sock[g]

                    # IMPLEMENTATION
                    # ---- start your code ---- #
                    pass

                    self.indices[g].add_msg_and_index(msg_time)
                    mysend(
                        to_sock, json.dumps({"action": "exchange", "from": name, "message": message}))  # "...Remember to index the messages before sending, or search won't work"

                    # ---- end of your code --- #

# ==============================================================================
# the "from" guy has had enough (talking to "to")!
# ==============================================================================
            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps(
                        {"action": "disconnect", "msg": "everyone left, you are alone"}))
# ==============================================================================
#                 listing available peers: IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "list":

                # IMPLEMENTATION
                # ---- start your code ---- #
                pass
                from_name = self.logged_sock2name[from_sock]
                msg = self.group.list_all(from_name)  # "...needs to use self.group functions to work"

                # ---- end of your code --- #
                mysend(from_sock, json.dumps(
                    {"action": "list", "results": msg}))
# ==============================================================================
#             retrieve a sonnet : IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "poem":

                # IMPLEMENTATION
                # ---- start your code ---- #
                pass
                index = int(msg["target"])
                from_name = self.logged_sock2name[from_sock]
                print(from_name, "ask for", index)
                lis = self.sonnet.get_poem(index)
                poem = ''
                for i in lis[:-2]:
                    poem += i + '\n'  # "...needs to use self.sonnet functions to work"
                print('here:\n', poem)

                # ---- end of your code --- #

                mysend(from_sock, json.dumps(
                    {"action": "poem", "results": poem}))
# ==============================================================================
#                 time
# ==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps(
                    {"action": "time", "results": ctime}))
# ==============================================================================
#                 search: : IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "search":

                # IMPLEMENTATION
                # ---- start your code ---- #
                pass

                name = self.logged_sock2name[from_sock]
                target = msg["target"]
                print(name, "search for", target)

                search_list = self.indices[name].search(target)
                search_rslt = ''
                for item in search_list:
                    search_rslt += item[1] + '\n'  # "needs to use self.indices search to work"
                print('server side search: ' + search_rslt)

                # ---- end of your code --- #
                mysend(from_sock, json.dumps(
                    {"action": "search", "results": search_rslt}))

# ==============================================================================
#                 the "from" guy really, really has had enough
# ==============================================================================

        else:
            # client died unexpectedly
            self.logout(from_sock)

# ==============================================================================
# main loop, loops *forever*
# ==============================================================================
    def run(self):
        print('starting server...')
        while(1):
            read, write, error = select.select(self.all_sockets, [], [])
            print('checking logged clients..')
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
            print('checking new clients..')
            for newc in self.new_clients[:]:
                if newc in read:
                    self.login(newc)
            print('checking for new connections..')
            if self.server in read:
                # new client request
                sock, address = self.server.accept()
                self.new_client(sock)


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
