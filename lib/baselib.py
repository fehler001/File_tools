#coding=utf-8
#File_tools/lib/baselib.py
import os
from tkinter import messagebox
import random
import shutil
import stat



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


