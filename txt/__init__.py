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

		self.CreateWidgetsFrameTxt()

		self.DivideRoot = self.FrameDivide
		self.DivideDefault()



	def CreateWidgetsFrameTxt(self):

		self.FrameDivide = Frame(self.TxtRoot)
		self.FrameDivide.pack(fill = BOTH)
		self.TxtRoot.add(self.FrameDivide, text='txt Divide')