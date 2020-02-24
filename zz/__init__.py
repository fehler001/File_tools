#coding=utf-8
#File_tools/zz/__init__.py


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

try:
	import zz.z1
	z = 1
except:
	z = 0


class Zz(
		  ):

	def __init__(self):
		super().__init__()
		
		if z == 0:
			return

		self.ZzRoot = None


	def ZzDefault(self):

		self.CreateWidgetsFrameZz()

		self.Z1Root = self.FrameDivide
		self.Z1Default()



	def CreateWidgetsFrameTxt(self):

		self.FrameZ1 = Frame(self.ZzRoot)
		self.FrameZ1.pack(fill = BOTH)
		self.ZzRoot.add(self.FrameZ1, text='Z1')
