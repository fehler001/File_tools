#coding=utf-8
#File_tools/txt/__init__.py


import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog 
import os
import sys
import shutil
import random
import json


import txt.Divide_txt


class Txt(txt.Divide_txt.CreateFrameDivide):

	def __init__(self):
		super().__init__()
		
		self.TxtRoot = None


	def TxtDefault(self):

		self.TxtDefaultLog()
		self.CreateWidgetsFrameTxt()

		self.DivideRoot = self.FrameDivide
		self.DivideDefault()


	def TxtDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		if not 'txt' in j['file_tools']:
			j['file_tools']['txt'] = {}
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def CreateWidgetsFrameTxt(self):

		self.FrameDivide = Frame(self.TxtRoot)
		self.FrameDivide.pack(fill = BOTH)
		self.TxtRoot.add(self.FrameDivide, text='Divide txt')