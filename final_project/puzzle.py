from tkinter import *
from logic import *
from random import *
from timer import *
import math
import os
import GUI_chat_client

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
                            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
                            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"


class GameGrid(Frame):
    def __init__(self, name='no name'):
        Frame.__init__(self)
        f3 = open('name_of_user.txt', 'r')
        name1 = f3.readline().strip()
        f3.close()
        if name1 == '':
            self.name = 'no name'
        else:
            self.name = name1
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        #self.gamelogic = gamelogic
        self.commands = {KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right,
                         KEY_UP_ALT: up, KEY_DOWN_ALT: down, KEY_LEFT_ALT: left, KEY_RIGHT_ALT: right}

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):

        bar = Frame(self, height=90, width=SIZE + 68, background="#92877d")
        bar.grid()

        B1 = Button(bar, text="restart", fg='red', command=self.restart, relief=FLAT, width=7, font=("Verdana", 20, "bold")).place(x=50, y=10)
        B2 = Button(bar, text="rank", fg='red', command=self.show_rank, relief=FLAT, width=7, font=("Verdana", 20, "bold")).place(x=50, y=50)
        text1 = Label(bar, text='Your score:', font=("Verdana", 20, "bold"), background="#92877d").place(x=250, y=10)

        self.sw = StopWatch(bar)
        self.sw.place(x=390, y=11)
        self.sw.Start()

        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

        bar2 = Frame(self, height=40, width=SIZE + 68, background="#92877d")
        bar2.grid()
        text2 = Label(bar2, text='When you face difficulty, try to click J', font=("Verdana", 20, "bold"), background="#92877d").place(x=50, y=0)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = new_game(4)

        self.matrix = add_two(self.matrix)
        self.matrix = add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def restart(self):
        self.init_matrix()
        self.update_grid_cells()
        self.sw.Reset()
        self.sw.Start()

    def show_rank(self):
        os.system("python3 game_rank.py")

    def key_down(self, event):
        key = repr(event.char)
        if key == "'j'":
            l_of_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in self.matrix:
                for j in i:
                    if j != 0:
                        n = math.log(j, 2)
                        n = int(n)
                        l_of_numbers[n - 1] += 1
                    else:
                        continue
            for k in range(len(l_of_numbers)):
                if l_of_numbers[k] != 0:
                    min_number = l_of_numbers[k]
                    small_k = k
                    break
                else:
                    continue

            l_smallest_number = []
            for i in range(len(self.matrix)):
                for j in range(4):
                    if self.matrix[i][j] == 2**(small_k + 1):
                        l_smallest_number.append([i, j])
            i_to_delete, j_to_delete = choice(l_smallest_number)
            self.matrix[i_to_delete][j_to_delete] = 0
            # print(self.matrix)
            self.update_grid_cells()

        if key in self.commands:
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = add_two(self.matrix)
                self.update_grid_cells()
                done = False
                if game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    total_time = self.sw.Stop()
                    #name_of_winner = get_name.pop_up_box()
                    # print(name_of_winner)

                    f = open('rank.txt', 'r')
                    s = f.readlines()
                    total_list = []
                    rank_list = []
                    name_list = []
                    for i in s:
                        total_list.append(i.strip())
                    for i in total_list:
                        rank_list.append(i.split('=')[1])
                        name_list.append(i.split('=')[0])

                    print(rank_list, name_list)
                    inserted = False
                    for i in range(len(rank_list)):
                        if int(total_time.split(':')[0]) < int(rank_list[i].split(':')[0]):
                            rank_list.insert(i, total_time)
                            name_list.insert(i, self.name)
                            inserted = True
                            break
                        elif int(total_time.split(':')[0]) == int(rank_list[i].split(':')[0]):
                            if int(total_time.split(':')[1]) < int(rank_list[i].split(':')[1]):
                                rank_list.insert(i, total_time)
                                name_list.insert(i, self.name)
                                inserted = True
                                break
                            elif int(total_time.split(':')[1]) == int(rank_list[i].split(':')[1]):
                                if int(total_time.split(':')[2]) < int(rank_list[i].split(':')[2]):
                                    rank_list.insert(i, total_time)
                                    name_list.insert(i, self.name)
                                    inserted = True
                                    break
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                    if inserted == False:
                        rank_list.append(total_time.strip())
                        name_list.append(self.name)

                    f.close()
                    f2 = open('rank.txt', 'w')
                    total_list = []
                    for i in range(len(name_list)):
                        total_list.append(name_list[i] + '=' + rank_list[i])
                    for line in total_list:
                        f2.write(line + '\n')
                    f2.close()

                if game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="Start", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Again", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    total_time = self.sw.Stop()

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = choice([2, 4])


if __name__ == '__main__':
    gamegrid = GameGrid()
