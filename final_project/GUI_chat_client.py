from tkinter import *
import tkinter.messagebox
import pprint
from chat_utils import *
from chat_client_class import *
import os


class GUI_Logged_in:

    def __init__(self, username):

        #-------------------------------------#
        #---------- Chat Initiating ----------#
        #-------------------------------------#

        import argparse
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()

        self.client = Client(args)
        self.logged_in = False
        self.client.input_instruction(username)
        self.client.run_chat(username)
        self.logged_in = self.client.login()
        self.username = username

        #-------------------------------------#
        #---------- Chat Initiating ----------#
        #-------------------------------------#

        self.main_window = Tk()
        self.main_window.geometry('750x580')
        self.main_window.title('SOS Chat')

        self.full_info = ''
        self.reading_position = 0

        self.top_frame = Frame(self.main_window)
        self.mid_frame = Frame(self.main_window)
        self.bot_frame = Frame(self.main_window)

        #----- Drop Down Munu -----#
        self.menu = Menu(self.main_window)
        self.main_window.config(menu=self.menu)

        self.subMenu = Menu(self.menu)
        self.menu.add_cascade(label='Tool', menu=self.subMenu)

        # To access the time function
        self.subMenu.add_command(label='Time', command=self.time)
        self.subMenu.add_command(label='poem', command=self.message)

        # To access how many people are online
        self.subMenu.add_command(label='Online people', command=self.online)
        self.subMenu.add_separator()

        # Quit the app
        self.subMenu.add_command(label='Quit', command=self.quit)

        self.editMenu = Menu(self.menu)
        self.menu.add_cascade(label='Game', menu=self.editMenu)

        # To access the game
        self.editMenu.add_command(label='2048', command=self.game)

        #----- Top Frame Hello User -----#
        self.hello_label = Label(self.top_frame, text='Welcome to SOS Chat', font='Arial -30 bold')
        self.hello_label.pack(side='right')
        #----- Top Frame Hello User -----#

        #----- Mid Frame Info Box -----#
        self.output_msg = StringVar()
        self.full_info = self.client.output()
        self.output_msg.set(self.full_info)
        self.info_label = Label(self.mid_frame, textvariable=self.output_msg, height=25, width=60, bg='#B0C4DE')
        self.info_label.pack(side='top')

        #----- Mid Frame Info Box -----#

        #----- Bot Frame Text Input -----#
        self.my_msg_entry = Entry(self.bot_frame, width=40)
        self.my_msg_entry.pack(side='left')
        self.send_button = Button(self.bot_frame, text='Send', height=2, width=6, command=self.update_output)
        self.send_button.pack(side='left')
        self.my_msg_entry.bind("<KeyPress-Return>", self.update_output)
        self.main_window.bind('<Up>', self.move_up)
        self.main_window.bind('<Down>', self.move_down)

        #----- Bot Frame Text Input -----#

        # self.top_frame.pack()
        self.top_frame.place(x=230, y=20)
        self.mid_frame.place(x=100, y=80)
        self.bot_frame.place(x=150, y=520)

        self.clock()

        self.main_window.mainloop()

        #-----------------------------------#
        #---------- Timely Update ----------#
        #-----------------------------------#

    def clock(self):                           # $$$ USER READING IN
        self.client.proc()
        sys_msg = self.client.output()
        if len(sys_msg) > 0:
            self.full_info += '\n' + sys_msg + '\n'
            # UPDATE LABEL
            offset = 0
            self.update_label(sys_msg, offset, 2)

        self.main_window.after(1000, self.clock)

        #-----------------------------------#
        #---------- Timely Update ----------#
        #-----------------------------------#
    # Auto downward moving, not to the bottom, easy to get out of sync
    def update_label(self, msg, offset=0, pad=0):  # msg handles self.client.output() and self.my_msg_entry.get()
        all_lines = self.full_info.split('\n')
        msg_list = msg.split('\n')
        if len(all_lines) == 18:
            if pad < 0 and self.reading_position == 0:
                pass
            else:
                self.reading_position += pad
        if len(all_lines) > 18:
            self.reading_position += len(msg_list) + 1
        # temporary adjustment, say for sonnet, offset = -10 to show the who poem from beginning, for admin notification, offset = -1 to allow another line saying Admin has done something
        self.reading_position += offset

        lines_displaying = all_lines[self.reading_position:self.reading_position + 17]
        lines_displaying = '\n'.join(lines_displaying) + '\n'

        self.output_msg.set(lines_displaying)

    '''
    # Auto move to the bottom when new message created
    def update_label(self, msg):
        all_lines = self.full_info.split('\n')
        msg_list = msg.split('\n')

        self.reading_position = (len(all_lines) - 9) * 2
        lines_displaying = all_lines[self.reading_position:self.reading_position + 9]
        lines_displaying = '\n\n'.join(lines_displaying)
    '''

    def move_label(self, k):  # msg handles self.client.output() and self.my_msg_entry.get()
        all_lines = self.full_info.split('\n')

        if len(all_lines) > 18:
            if k > 0:
                print('all_lines', len(all_lines))
                if self.reading_position < len(all_lines) - 22:
                    self.reading_position += k
            if k < 0:
                if self.reading_position > 1:
                    self.reading_position += k

        lines_displaying = all_lines[self.reading_position:self.reading_position + 24]
        lines_displaying = '\n'.join(lines_displaying)
        lines_displaying = '\n' + lines_displaying + '\n'
        self.output_msg.set(lines_displaying)
        print(self.reading_position)

    def update_output(self, event=None):  # $$$ USER WRITING OUT
        # Pass input to client
        if len(self.my_msg_entry.get()) > 0:
            # checking
            self.input = self.my_msg_entry.get()
            self.full_info += '\n' + self.input + '\n'
            self.client.input_instruction(self.input)
            # UPDATE LABEL
            offset = 0
            self.update_label(self.input, offset, -2)

            if not self.logged_in:
                self.logged_in = self.client.login()

            if self.logged_in and self.client.sm.get_state() != S_OFFLINE:
                print(True)
                self.client.proc()
                time.sleep(CHAT_WAIT)
                self.clock()

            else:
                self.client.shutdown_chat()
                self.client.quit()
                self.quit()

        while self.my_msg_entry.get() != '':
            self.my_msg_entry.delete(0)

    def time(self):
        self.client.input_instruction('time')
        self.client.proc()

    def getname(self):
        f = open('name_of_user.txt', 'w')
        f.write(self.username)
        f.close()

    def game(self):
        self.getname()

        os.system('python3 puzzle.py')

    #----- Poem Window -----#
    def message(self):
        self.poem_window = Toplevel(self.main_window)
        self.poem_window.geometry('350x200')
        self.poem_window.title('Poem Number')
        self.poem_top_frame = Frame(self.poem_window)
        self.poem_top_frame.place(x=90, y=40)
        self.poem_mid_frame = Frame(self.poem_window)
        self.poem_mid_frame.place(x=80, y=70)
        self.poem_but_frame = Frame(self.poem_window)
        self.poem_but_frame.place(x=150, y=130)

        self.poem_number = StringVar()
        entry = Label(self.poem_top_frame, text='type \"p + number\" (ex.p1):')
        entry.place(x=10, y=10)
        entry.pack()
        self.entry_poem_name = Entry(self.poem_mid_frame, textvariable=self.poem_number)
        self.entry_poem_name.place(x=150, y=10)
        self.entry_poem_name.pack()

        self.confirm_button = Button(self.poem_but_frame, text='Confirm', height=2, width=6, command=self.poem)
        self.confirm_button.pack()
        self.entry_poem_name.bind("<KeyPress-Return>", self.poem)

    def poem(self, event=None):
        self.pn = self.poem_number.get()
        self.client.input_instruction(self.pn)
        self.client.proc()
        self.poem_window.destroy()

    def online(self):
        self.client.input_instruction('who')
        self.client.proc()

    def move_up(self, event=None):
        self.move_label(-2)

    def move_down(self, event=None):
        self.move_label(2)

    def quit(self):
        if self.client.sm.get_state() == S_CHATTING:
            self.client.input_instruction('bye')
            self.client.proc()
        self.client.quit()
        self.main_window.destroy()


if __name__ == '__main__':
    myGUI = GUI_Logged_in('SOS')
    # pprint.pprint(dir(myGUI.my_msg_entry))
