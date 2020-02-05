import sys
import os
from tkinter import messagebox
import random
import shutil
import stat
	
import lib.baselib

from natsort import natsort_keygen, ns


class TxtLib():

	def __init__(self):
		super().__init__()


	def create_txt(self, txt_name):
		f = open(txt_name, 'w', encoding='utf-8')
		f.close()


	def append_one_line(self, txt_name, line):
		f = open(txt_name, 'a', encoding='utf-8')
		f.write(line)
		f.close()


	def divide_txt(self, txt_src, txt_save_path, lines_limit = 500, digit = 6):
		src = txt_src
		path = txt_save_path
		limit = lines_limit
		try:
			f = open(src, 'r', encoding='utf-8')
		except:
			messagebox.showerror ("ERROR", 'Can not open src\n\nUTF-8 txt file needed')
			return -1
		n = 1
		nline = 0

		txt_name = path + '/' + (digit -len(str(n)))*'0' + str(n) + '.txt'
		self.create_txt(txt_name)

		for line in f:
			self.append_one_line(txt_name, line)
			nline = nline + 1

			if nline % limit == 0:
				n = n + 1
				txt_name = path + '/' + (digit - len(str(n)))*'0' + str(n) + '.txt'
				try:
					self.create_txt(txt_name)
				except:
					messagebox.showerror ("ERROR", '"' + e + '"' + "went wrong")
					return -1






