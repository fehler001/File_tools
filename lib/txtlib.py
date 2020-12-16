import sys
import os
from tkinter import messagebox
import random
import shutil
import stat
	
try:
	import lib.baselib
except:
	import baselib

from natsort import natsort_keygen, ns


class TxtLib():

	def __init__(self):
		super().__init__()

		try:
			self.bl = lib.baselib.BaseLib()
		except:
			self.bl = baselib.BaseLib()




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



	# return list with lines after ".strip()",      split means split line, not lines
	def get_txt_content(self, file, split = None, mode = 'r', encoding = 'utf-8'):
		try:
			content = []
			f = open(file, mode, encoding = encoding)

			if split == 'wholetext':
				content = f.read()
				f.close()
				return content

			lines = f.readlines()
			f.close()
			for line in lines:
				if split != None:
					lines_1 = line.split(split)
				else:
					lines_1 = [line]
				for line_1 in lines_1:
					content.append( line_1.strip() )
			return content
		except:
			messagebox.showerror ("ERROR", 'Can not open txt\n\nUTF-8 txt file needed')
			return -1




	def clean_txt(self, source, mode = 'mode 1', is_repeat = 0, is_sort = 0, is_enter = 0):
		all = []

		s = 0
		if len(source) < 1000:
			if os.path.exists(source):
				src = self.get_txt_content(source)
				if src == -1:
					return -1
			else: s = 1
		else: s = 1

		if s ==1:
			src = source
			#src = src.replace('\n', '\n \n')
			src = src.split('\n')

		for i in range(len(src)):
			line = ''
			if mode == 'mode 1':
				line = src[i]
			elif mode == 'mode 2':
				if src[i] == '':
					continue
				tmp = src[i].split()
				for t in tmp:
					line = line + t + ' '
			all.append(line)

		if is_repeat == 1:
			all2 = []
			for line in all:
				if line == '':
					all2.append(line)
					continue
				elif line in all2:
					continue
				else:
					all2.append(line)
			all = all2

		if is_sort == 1:
			all = sorted(all, key=self.natsort_key2)
			all = self.bl.clean_list(all)

		if is_enter == 1:
			all2 = []
			s = 0
			for line in all:
				if line != '':
					if s == 1:
						all2.append('')
						s = 0
					all2.append(line)
					s = 1
					continue
				else:
					s = 0
					all2.append(line)
			all = all2

		return all



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




	def check_string_in(self, source, dict, mode, is_reverse = 0, is_strip_space = 0):
		all = []

		if len(source) < 1000:
			if os.path.exists(source):
				try:
					src = self.get_txt_content(source)
				except:
					messagebox.showerror ("ERROR", 'Can not open src\n\nUTF-8 txt file needed')
					return -1
			else: src = source
		else: src = source

		if is_strip_space == 1:
			n = 0
			for line in src:
				src[n] = src[n].replace(' ', '')
				n = n + 1
			

		if os.path.exists(dict):
			try:
				d = self.get_txt_content(dict)   # get a dict with multiple lines, not a whole single string
			except:
				messagebox.showerror ("ERROR", 'Can not open src\n\nUTF-8 txt file needed')
				return -1
		else:
			d = dict
		
		s = []
		if mode == 'mode 1':
			if is_strip_space == 0:
				s = d
			else:
				for line in d:
					s.append(line.replace(' ', ''))
		elif mode == 'mode 2':
			for i in range(len(d)):
				l = len(d[i])
				if l < 3:
					s.append(d[i])
				else:
					for i2 in range( l - 1 ):
						s.append( d[i][ i2 : i2+2 ] )
		elif mode == 'mode 3':
			for i in range(len(d)):
				for c in d[i]:
					s.append(c)
		s = set(s)
		s = sorted(s, key=self.natsort_key2)
		s = self.bl.clean_list(s)

		for i in range(len(s)):
			if is_reverse == 0:
				if s[i] in src:
					all .append(s[i])
			else:
				if s[i] not in src:
					all .append(s[i])

		return all




if __name__ == '__main__':

	tl = TxtLib()
	p=r'F:\newfolder2\system\linux\ubuntu.txt'
	c=tl.clean_txt(p)
	print(c)
