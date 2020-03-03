#coding=utf-8
#File_tools/rar/__init__.py


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

import rar.Brute_force_crack


class Rar(rar.Brute_force_crack.CreateFrameBrute,
				
		  ):

	def __init__(self):
		super().__init__()
		
		self.RarRoot = None


	def RarDefault(self):

		self.CreateWidgetsFrameRar()

		self.BruteRoot = self.FrameBrute
		self.BruteDefault()



	def CreateWidgetsFrameRar(self):

		self.FrameBrute = Frame(self.RarRoot)
		self.FrameBrute.pack(fill = BOTH)
		self.RarRoot.add(self.FrameBrute, text='rar Crack')
