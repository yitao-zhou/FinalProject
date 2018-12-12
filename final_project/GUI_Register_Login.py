import tkinter
import tkinter.messagebox
from GUI_chat_client import *
from chat_client_class import *

from tkinter import *
from tkinter import messagebox


class LogInterface:
    def __init__(self):
        # Main Window #
        self.main_window = tkinter.Tk()
        self.main_window.title('Welcome to SOS Chat!')
        self.main_window.geometry('400x300')

        # Logo #
        self.main_canvas = tkinter.Canvas(self.main_window, height=200, width=400)
        main_image_file = tkinter.PhotoImage(file='SOS-1.gif')
        main_image = self.main_canvas.create_image(-5, 10, anchor='nw', image=main_image_file)
        self.main_canvas.pack(side='top')

        # User Info #
        # self.userlabel = tkinter.Label(self.main_window, text='Username:')
        self.usercanvas = self.main_canvas.create_text(110, 115, text='Username:', font=("Verdana", 15, "bold"))
        # self.password_label = tkinter.Label(self.main_window, text='Password:')
        self.passwordcanvas = self.main_canvas.create_text(110, 165, text='Password:', font=("Verdana", 15, "bold"))
        # self.userlabel.place(x=50, y=100)
        # self.password_label.place(x=50, y=150)

        # User Entry #
        self.username_var = tkinter.StringVar()
        self.userpass_var = tkinter.StringVar()

        self.username_entry = tkinter.Entry(self.main_window, bd=3, textvariable=self.username_var)
        self.user_pass = tkinter.Entry(self.main_window, bd=3, textvariable=self.userpass_var, show='*')

        self.username_entry.place(x=160, y=100)
        self.user_pass.place(x=160, y=150)

        # Buttons #
        self.login_b = tkinter.Button(self.main_window, height=2, width=5, text='Login', font=("Verdana", 13, 'bold'), fg='blue', command=self.user_login)
        self.login_b.place(x=220, y=190)

        self.sign_up_b = tkinter.Button(self.main_window, height=2, width=7, text='Sign up', font=("Verdana", 13), command=self.user_sign_up)
        self.sign_up_b.place(x=280, y=190)

        # Response Info #
        self.response_msg = tkinter.StringVar()

        import argparse
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()

        self.client = Client(args)
        self.logged_in = False
        self.client.input_instruction('logger')
        self.client.run_chat('logger')
        self.logged_in = self.client.login()
        print('logger born', self.logged_in)
        tkinter.mainloop()

    def user_login(self):
        self.user_name = self.username_var.get()
        self.user_pass = self.userpass_var.get()
        msg = json.dumps({"action": "login", "name-pass": self.user_name + ',' + self.user_pass})
        self.client.send(msg)
        response = json.loads(self.client.recv())
        if response["status"] == 'okay':
            print('User Exists')
            self.main_window.destroy()
            self.new_window = GUI_Logged_in(self.user_name)
        elif response["status"] == 'notFound':
            self.response_msg.set('Sorry! User name does not exist.')
            self.response_label = tkinter.Label(self.main_window, textvariable=self.response_msg, fg='Red')
            self.response_label.place(x=55, y=230)
            self.response_label = tkinter.Label(self.main_window, text='Please try again.', fg='Red')
            self.response_label.place(x=55, y=255)

        elif response["status"] == 'duplicate':
            self.response_msg.set('Sorry! This user has already logged in.')
            self.response_label = tkinter.Label(self.main_window, textvariable=self.response_msg, fg='Red')
            self.response_label.place(x=55, y=230)
            self.response_label = tkinter.Label(self.main_window, text='Please try again.', fg='Red')
            self.response_label.place(x=55, y=255)

        elif response["status"] == 'incorrect':
            self.response_msg.set('Sorry! Username or passowrd is incorrect.')
            self.response_label = tkinter.Label(self.main_window, textvariable=self.response_msg, fg='Red')
            self.response_label.place(x=55, y=230)
            self.response_label = tkinter.Label(self.main_window, text='Please try again.', fg='Red')
            self.response_label.place(x=55, y=255)

    def user_sign_up(self):

        def new_user_sign_up():
            nn = new_name.get()
            np = new_pwd.get()
            npc = new_pwd_confirm.get()
            if nn.strip() and np.strip() and npc.strip():
                if np != npc:
                    self.response_msg.set('Sorry! Password does not match.')
                    response_label = tkinter.Label(self.sign_up_window, textvariable=self.response_msg, fg='Red')
                    response_label.place(x=10, y=25)
                    response_label = tkinter.Label(self.sign_up_window, text='Please try again.', fg='Red')
                    response_label.place(x=10, y=45)
                else:
                    msg = json.dumps({"action": "register", "name-pass": nn + ',' + np})
                    self.client.send(msg)
                    print('sending registration information')
                    response = json.loads(self.client.recv())
                    print('response to registration comes back from server: ', response)
                    if response["status"] == 'okay':
                        self.response_msg.set('You have successfully signed up!')
                        self.response_label = tkinter.Label(self.main_window, textvariable=self.response_msg, fg='Blue')
                        self.response_label.place(x=55, y=230)
                        self.sign_up_window.destroy()

                    elif response["status"] == 'duplicate':
                        self.response_msg.set('Sorry! Username already exist.')
                        response_label = tkinter.Label(self.sign_up_window, textvariable=self.response_msg, fg='Red')
                        response_label.place(x=10, y=25)
                        response_label = tkinter.Label(self.sign_up_window, text='Please try again.', fg='Red')
                        response_label.place(x=10, y=45)
            else:
                self.response_msg.set('Sorry! Name or password should not be blank.')
                response_label = tkinter.Label(self.sign_up_window, textvariable=self.response_msg, fg='Red')
                response_label.place(x=10, y=25)
                response_label = tkinter.Label(self.sign_up_window, text='Please try again.', fg='Red')
                response_label.place(x=10, y=45)

        self.sign_up_window = tkinter.Toplevel(self.main_window)
        self.sign_up_window.geometry('350x300')
        self.sign_up_window.title('Sign up')

        # Logo #
        # self.sign_up_canvas = tkinter.Canvas(self.sign_up_window, height=200, width=300)
        # sign_up_image_file = tkinter.PhotoImage(file='SOS-2.gif')
        # sign_up_image = self.sign_up_canvas.create_image(0, 10, anchor='nw', image=sign_up_image_file)
        # self.sign_up_canvas.pack(side='top')

        # Username #
        new_name = tkinter.StringVar()
        tkinter.Label(self.sign_up_window, text='Username:').place(x=10, y=70)
        entry_new_name = tkinter.Entry(self.sign_up_window, textvariable=new_name)
        entry_new_name.place(x=150, y=70)

        # Password #
        new_pwd = tkinter.StringVar()
        tkinter.Label(self.sign_up_window, text='Password:').place(x=10, y=110)
        entry_new_pwd = tkinter.Entry(self.sign_up_window, textvariable=new_pwd, show='*')
        entry_new_pwd.place(x=150, y=110)

        # Confirm Password #
        new_pwd_confirm = tkinter.StringVar()
        tkinter.Label(self.sign_up_window, text='Confirm password:').place(x=10, y=150)
        entry_new_pwd_confirm = tkinter.Entry(self.sign_up_window, textvariable=new_pwd_confirm, show='*')
        entry_new_pwd_confirm.place(x=150, y=150)

        # Sign up Button #
        sign_up = tkinter.Button(self.sign_up_window, height=2, width=7, text='Sign up', command=new_user_sign_up)
        sign_up.place(x=270, y=190)


if __name__ == '__main__':
    login = LogInterface()
