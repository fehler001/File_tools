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

import txt.Clean_txt
import txt.Divide_txt
import txt.String_encoding_decoding
import txt.String_match


class Txt(txt.Clean_txt.CreateFrameClean,
				txt.Divide_txt.CreateFrameDivide,
				txt.String_encoding_decoding.CreateFrameStr,
				txt.String_match.CreateFrameMatch,
		  ):

	def __init__(self):
		super().__init__()
		
		self.TxtRoot = None


	def TxtDefault(self):

		self.CreateWidgetsFrameTxt()

		self.CleanRoot = self.FrameClean
		self.CleanDefault()
		self.DivideRoot = self.FrameDivide
		self.DivideDefault()
		self.StrRoot = self.FrameStr
		self.StrDefault()
		self.MatchRoot = self.FrameMatch
		self.MatchDefault()



	def CreateWidgetsFrameTxt(self):

		self.FrameClean = Frame(self.TxtRoot)
		self.FrameClean.pack(fill = BOTH)
		self.TxtRoot.add(self.FrameClean, text='txt Clean')
		self.FrameDivide = Frame(self.TxtRoot)
		self.FrameDivide.pack(fill = BOTH)
		self.TxtRoot.add(self.FrameDivide, text='Divide')
		self.FrameStr = Frame(self.TxtRoot)
		self.FrameStr.pack(fill = BOTH)
		self.TxtRoot.add(self.FrameStr, text='Transcode')
		self.FrameMatch = Frame(self.TxtRoot)
		self.FrameMatch.pack(fill = BOTH)
		self.TxtRoot.add(self.FrameMatch, text='Match')