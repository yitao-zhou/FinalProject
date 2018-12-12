# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
@revised by: Sunny Song, Oscar Wan
"""
from util import *
import string
import pprint
import pickle


class WordFreq:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __str__(self):
        return self.word + ":" + str(self.freq)


class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = []
        self.index = {}
        self.sect_index = {}
        self.wd_freq_list = []
        self.total_words = 0
        self.num_sections = 0

    def add_msg(self, m):
        self.msgs.append(m.strip())
        self.total_msgs += 1
        word_l = m.split(' ')
        self.total_words += len(word_l)

    def get_msg_size(self):
        return len(self.msgs)

    def set_sect_begin_end(self, i, start, end):
        self.sect_index[i] = (start, end)

    def get_sect(self, i):
        rt = ''
        if i <= len(self.sect_index):
            start = self.sect_index[i][0]
            end = self.sect_index[i][1]
            for i in range(start, end):
                rt += self.msgs[i] + '\n'
        return rt

    def add_msg_and_index(self, m):
        self.msgs.append(m)
        self.indexing(m, len(self.msgs) - 1)

    def get_msg(self, n):
        return self.msgs[n]

    def indexing(self, m, l):
        words = m.split()
        # remove the following two lines when run real
        if len(words) == 1:
            self.num_sections += 1
        else:
            self.total_words += len(words)
            for wd in words:
                if wd not in self.index:
                    self.index[wd] = [l, ]
                else:
                    self.index[wd].append(l)

    def build_wf_list(self):
        wf_list = []
        for wd in self.index.keys():
            wf = WordFreq(wd, len(self.index[wd]))
            wf_list.append(wf)
            self.wd_freq_list = sorted(wf_list,
                                       key=lambda wf: wf.freq,
                                       reverse=True)

    def print_msg_with_key(self, key):
        if key not in self.index.keys():
            print(key, ': not found!')
            return
        print('KEY: [', key, ']')
        # add logic to change fonts
        for msg_num in self.index[key]:
            msg2 = proc_message(key, self.get_msg(msg_num))
            print(msg_num, ': ', msg2)
        print('+++++++++++++++++++++++++++++++++++\n')

    def print_top_freq_word(self, num_tops, msg_too):
        print('+++ top', num_tops, 'words+++++++++++++++')
        for i in range(num_tops):
            wf = self.wd_freq_list[i]
            print(i, '->\t', wf)
            if msg_too == True:
                self.print_msg_with_key(wf.word)

    def print_stats(self):
        print('\n+++++++++ stats ++++++++++++')
        print('there are', self.num_sections, 'sections')
        print('a total of', self.total_words, 'unique words')
        print('out of a total of', len(self.index), 'words')
        print('\n')

    def search(self, term):
        msgs = []
        if (term in self.index.keys()):
            indices = self.index[term]
            msgs = [(i, self.msgs[i]) for i in indices]
        return msgs

    def sub_search(self, word):
        indices = []
        if word in self.index:
            indices += self.index[word]
        return indices


class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()

        # load poems
    def load_poems(self):
        lines = open(self.name, 'r')
        for line in lines:
            self.add_msg_and_index(line)
        lines.close()

    def get_poem(self, p):
        rom_p = self.int2roman[p] + '.'
        line_num = self.index[rom_p][0]

        end_rom_p = self.int2roman[p + 1] + '.'
        end_line_num = self.index[end_rom_p][0]
        poem = []
        for line_ind in range(line_num, end_line_num):
            poem.append(self.get_msg(line_ind))

        pprint.pprint(poem)

        return poem


if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    p3 = sonnets.get_poem(3)
    print(p3)
    s_love = sonnets.search("love")
    print(s_love)
