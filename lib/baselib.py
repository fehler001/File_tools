#coding=utf-8
#File_tools/lib/baselib.py

import os
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font, nametofont
import random
import shutil
import stat
import codecs
import base64
import html
import chardet
from encodings.aliases import aliases
import pprint




class BaseLib():

	def __init__(self):
		super().__init__()


	def check_legit_int(self, cont):
		try:
			int(cont)
		except:
			messagebox.showerror ("NUMERIC ERROR", 'Please fill a number. (like "1", "3")')
			return -1


	def check_legit_string(self, cont):
		illegal = ['/', '\\', ':', '*', '"', '<', '>', '|', '?']
		for c in cont:
			if c in illegal:
				messagebox.showerror ("STRING ERROR", "['/', '\\', ':', '*', '\"', '<', '>', '|', '?'] are not allowed")
				return -1


	def check_has_repeat(self, list):
		l2 = []
		for item in list:
			if item in l2:
				messagebox.showerror ("REPEAT ERROR", "Got same name file !\n\n" + '"' + item + '"')
				return -1
			l2.append(item)



	def clean_list(self, list, is_repeat = 0, is_sort = 0):
		all = []
		if is_repeat == 1:
			list = set(list)
		if is_sort == 1:
			list = sorted(list, key = self.natsort_key2)
		for item in list:
			if item == '' or item == '\n':
				continue
			all.append(item)
		return all



	def str_encode(self, string, enc = 'utf-8'):
		if enc == 'html':
			rst = html.escape(string)
			return rst
		if enc == 'base64':
			rst_b = base64.b64encode(string.encode("utf-8"))
			rst = str(rst_b, "utf-8")
			#rst_b = base64.urlsafe_b64encode(string.encode("utf-8"))   # safe encode in base64
			#rst = str(rst_b, "utf-8")
			return rst
		rst = codecs.encode(string, encoding = enc, errors = 'backslashreplace')
		return rst


	def bytes_decode(self, binary, enc = 'utf-8'):
		rst = codecs.decode(binary, encoding = enc, errors = 'backslashreplace')
		return rst


	def str_decode(self, string, enc = 'utf-8'):
		if string[0:2] == "b'" and string[-1] == "'":
			str = string[2:-1]
		else:
			str = string
		if enc == 'html':
			rst = html.unescape(str)
			return rst
		if enc == 'base64':
			b = base64.b64decode(str)
			rst = codecs.decode(b, encoding = 'utf-8', errors = 'backslashreplace')
			return rst
		else:
			b = eval('b' + "'" + str + "'")		
		rst = codecs.decode(b, encoding = enc, errors = 'backslashreplace')
		return rst


	def str_transcode(self, string, enc_from = 'utf-8', enc_to = 'utf-8'):
		b = self.str_encode(string, enc = enc_from)
		rst = self.bytes_decode(b, enc = enc_to)
		return rst



	def guess_encoding_binary(self, binary):
		return chardet.detect(binary)




if __name__ == '__main__':
	import txtlib
	p = r'd:\a.txt'
	tl = txtlib.TxtLib()
	bl = BaseLib()
	b = b"example"
	print(b)
	s = "ああ有難う士兵出?"

