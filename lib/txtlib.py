import sys
import os
from tkinter import messagebox
import random
import shutil
import stat
	
#import lib.baselib

from natsort import natsort_keygen, ns


class TxtLib():

	def __init__(self):
		super().__init__()


	def create_txt(self, txt_name, mode = 'w', encoding = 'utf-8'):
		f = open(txt_name, mode, encoding = encoding)
		f.close()


	def append_one_line(self, txt_name, line, encoding = 'utf-8'):
		f = open(txt_name, 'a', encoding =  encoding)
		f.write(line)
		f.close()



	def write_txt(self, txt_name, content, mode = 'w', encoding = 'utf-8'):
		self.create_txt(txt_name, mode = mode, encoding = encoding)
		self.append_one_line(txt_name = txt_name, line = content, encoding = encoding)



	# return list with lines after ".strip()"
	def get_txt_content(self, file, split = None, mode = 'r', encoding = 'utf-8'):
		try:
			content = []
			f = open(file, mode, encoding = encoding)
			lines = f.readlines()
			f.close()
			for line in lines:
				lines_1 = lines
				if split != None:
					lines_1 = line.split(split)
				for line_1 in lines_1:
					content.append( line_1.strip() )
			return content
		except:
			messagebox.showerror ("ERROR", 'Can not open txt\n\nUTF-8 txt file needed')
			return -1



	def divide_txt(self, txt_src, txt_save_path, lines_limit = 500, digit = 6, mode = 'r', encoding = 'utf-8'):
		src = txt_src
		path = txt_save_path
		limit = lines_limit
		try:
			f = open(src, mode, encoding = encoding)
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





if __name__ == '__main__':

	tl = TxtLib()
	t = tl.get_txt_content(r'E:\python\File_tools\firewall_add_rules_savefile.txt')#, split = '#')
	for l in t:
		print(l)
