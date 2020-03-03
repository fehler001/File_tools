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
	import zz.Z1
except:
	pass

try:
	class Zz(zz.Z1.CreateFrameZ1
			  ):
	
		def __init__(self):
			super().__init__()
			self.ZzRoot = None
	
		def ZzDefault(self):
			self.CreateWidgetsFrameZz()
			self.Z1Root = self.FrameZ1
			self.Z1Default()
	
		def CreateWidgetsFrameZz(self):
	
			self.FrameZ1 = Frame(self.ZzRoot)
			self.FrameZ1.pack(fill = BOTH)
			self.ZzRoot.add(self.FrameZ1, text='Z1')

except:
	class Zz():
	
		def __init__(self):
			super().__init__()
			self.ZzRoot = None
	
		def ZzDefault(self):	
			pass