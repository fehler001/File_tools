#coding=utf-8
#File_tools/zz/Match_txt.py

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
import copy

import tkinterdnd2 
from tkinterdnd2 import *



class CreateFrameMatch():

	def __init__(self):
		super().__init__()

		self.MatchRoot = None

		self.MatchSourcePath = ''
		self.MatchDictPath = ''



	def MatchDefault(self):

		self.MatchDefaultLog()
		self.CreateWidgetsFrameMatch()
		self.MatchRestoreState()
		

	def MatchDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'match' in j['file_tools']['txt']:
			j['file_tools']['txt']['match'] = {}
		if not 'path_source' in j['file_tools']['txt']['match']:
			j['file_tools']['txt']['match']['path_source'] = ''
		if not 'path_dict' in j['file_tools']['txt']['match']:
			j['file_tools']['txt']['match']['path_dict'] = ''
		if not 'combo_mode' in j['file_tools']['txt']['match']:
			j['file_tools']['txt']['match']['combo_mode'] = 'mode 1'
		if not 'text_up' in j['file_tools']['txt']['match']:
			j['file_tools']['txt']['match']['text_up'] = ''
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()




	def MatchRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.MatchSourcePath = j['file_tools']['txt']['match']['path_source']
		self.MatchDictPath = j['file_tools']['txt']['match']['path_dict']
		self.MatchEntryTxtSource.insert(0, self.MatchSourcePath)
		self.MatchEntryTxtDict.insert(0, self.MatchDictPath )
		self.MatchComboMode.set(j['file_tools']['txt']['match']['combo_mode'])
		self.MatchTextUp.insert(INSERT, j['file_tools']['txt']['match']['text_up'] )
		f.close()


	

	def ReadMatchPath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.MatchSourcePath = j['file_tools']['txt']['match']['path_source']
		self.MatchDictPath = j['file_tools']['txt']['match']['path_dict']
		f.close()



	def MatchSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['txt']['match']['path_source'] = self.MatchEntryTxtSource.get()
			j['file_tools']['txt']['match']['path_dict'] = self.MatchEntryTxtDict.get()
			j['file_tools']['txt']['match']['combo_mode'] = self.MatchComboMode.get()
			tu = self.MatchTextUp.get('1.0', 'end')
			if tu[-1] == '\n':
				j['file_tools']['txt']['match']['text_up'] = tu[0:-1]
			else:
				j['file_tools']['txt']['match']['text_up'] = tu
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def MatchReset(self):
		self.MatchEntryTxtSource.delete(0, "end")
		self.MatchEntryTxtDict.delete(0, "end")
		self.MatchTextUp.delete("1.0", "end")
		self.MatchTextDown.delete("1.0", "end")
		self.MatchSaveEntry()
	


	def MatchAddSource(self):
		self.ReadMatchPath()
		p = self.MatchSourcePath
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(initialdir = p) 
		else:
			dir = filedialog.askopenfilename(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.MatchEntryTxtSource.delete(0, "end")
			self.MatchEntryTxtSource.insert(0, dir)
			self.MatchSourcePath = dir
			self.MatchSaveEntry()
		except:pass
	

	def MatchAddDirection(self):
		self.ReadMatchPath()
		p = self.MatchDictPath
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(initialdir = p) 
		else:
			dir = filedialog.askopenfilename(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.MatchEntryTxtDict.delete(0, "end")
			self.MatchEntryTxtDict.insert(0, dir)
			self.MatchDictPath = dir
			self.MatchSaveEntry()
		except:pass




	def MatchCheckText(self):
		self.MatchSaveEntry()
		self.ReadMatchPath()
		self.MatchTextDown.delete("1.0", "end")
		mode = self.MatchComboMode.get()
		textup = self.MatchTextUp.get("1.0", "end")
		textdown = self.tl.check_string_in(source = textup, dict = self.MatchDictPath, mode = mode)
		for line in textdown:
			self.MatchTextDown.insert(INSERT, line)
			self.MatchTextDown.insert(INSERT, '\n')



	def MatchCheckTxt(self, preview = False):
		self.MatchSaveEntry()
		self.ReadMatchPath()
		self.MatchTextDown.delete("1.0", "end")
		mode = self.MatchComboMode.get()
		textdown = self.tl.check_string_in(source = self.MatchSourcePath, dict = self.MatchDictPath, mode = mode)
		for line in textdown:
			self.MatchTextDown.insert(INSERT, line)
			self.MatchTextDown.insert(INSERT, '\n')
		
		


	def CreateWidgetsFrameMatch(self):

		# start up left Frame
		self.MatchFrameUpLeft = ttk.LabelFrame(self.MatchRoot, text = "")
		self.MatchFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.28)

		# start Frame1
		self.MatchFrame1 = ttk.Frame(self.MatchFrameUpLeft)
		self.MatchFrame1.pack(side = TOP, fill = X)

		self.MatchScrollbarXTxtSource = ttk.Scrollbar(self.MatchFrame1, orient = HORIZONTAL)
		self.MatchScrollbarXTxtSource.pack( side = BOTTOM, fill = X )

		self.MatchLableTxtSource = ttk.Label(self.MatchFrame1, text = "Txt Source Path ( use dict to match content in source )", anchor = W)
		self.MatchLableTxtSource.pack(side = TOP, fill = X)
		
		self.MatchEntryTxtSource = ttk.Entry(self.MatchFrame1, font = self.ft, xscrollcommand = self.MatchScrollbarXTxtSource.set)
		self.MatchEntryTxtSource.pack(fill = X)

		self.MatchEntryTxtSource.drop_target_register(DND_FILES, DND_TEXT)
		self.MatchEntryTxtSource.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.MatchScrollbarXTxtSource.config( command = self.MatchEntryTxtSource.xview )
		# end Frame1

		# start Frame2
		self.MatchFrame2 = ttk.Frame(self.MatchFrameUpLeft)
		self.MatchFrame2.pack(side = TOP, fill = X)

		self.MatchScrollbarXTxtDict = ttk.Scrollbar(self.MatchFrame2, orient = HORIZONTAL)
		self.MatchScrollbarXTxtDict.pack( side = BOTTOM, fill = X )

		self.MatchLableTxtDict = ttk.Label(self.MatchFrame2, text = "Txt Dict Path ( put your keyword in the txt )", anchor = W)
		self.MatchLableTxtDict.pack(side = TOP, fill = X)
		
		self.MatchEntryTxtDict = ttk.Entry(self.MatchFrame2, font = self.ft, xscrollcommand = self.MatchScrollbarXTxtDict.set)
		self.MatchEntryTxtDict.pack(fill = X)

		self.MatchEntryTxtDict.drop_target_register(DND_FILES, DND_TEXT)
		self.MatchEntryTxtDict.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.MatchScrollbarXTxtDict.config( command = self.MatchEntryTxtDict.xview )
		# end Frame2
		# end up left Frame
		
		# start down left Frame
		self.MatchFrameDownLeft = ttk.Frame(self.MatchRoot)
		self.MatchFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.29, relheight = 0.70)
		
		# start down left frame 1
		self.MatchFrameDownLeft_1 = ttk.LabelFrame(self.MatchFrameDownLeft, text = r'Paste text here to match string')
		self.MatchFrameDownLeft_1.place(relx = 0.0, relwidth = 1.0, rely = 0.0, relheight = 0.5)

		self.MatchScrollbarXUpText = ttk.Scrollbar(self.MatchFrameDownLeft_1, orient = HORIZONTAL)
		self.MatchScrollbarXUpText.pack( side = BOTTOM, fill = X )
		
		self.MatchScrollbarYUpText = ttk.Scrollbar(self.MatchFrameDownLeft_1, orient = VERTICAL)
		self.MatchScrollbarYUpText.pack( side = RIGHT, fill = Y )
		
		self.MatchTextUp = Text(self.MatchFrameDownLeft_1, font = self.ft, xscrollcommand = self.MatchScrollbarXUpText.set, yscrollcommand = self.MatchScrollbarYUpText.set, wrap = 'none')
		self.MatchTextUp.pack(fill = BOTH)
		
		self.MatchScrollbarXUpText.config( command = self.MatchTextUp.xview )
		self.MatchScrollbarYUpText.config( command = self.MatchTextUp.yview )
		# end down left frame 1

		# start down left frame 2
		self.MatchFrameDownLeft_2 = ttk.LabelFrame(self.MatchFrameDownLeft, text = r'Matched')
		self.MatchFrameDownLeft_2.place(relx = 0.0, relwidth = 1.0, rely = 0.5, relheight = 0.5)

		self.MatchScrollbarXDownText = ttk.Scrollbar(self.MatchFrameDownLeft_2, orient = HORIZONTAL)
		self.MatchScrollbarXDownText.pack( side = BOTTOM, fill = X )
		
		self.MatchScrollbarYDownText = ttk.Scrollbar(self.MatchFrameDownLeft_2, orient = VERTICAL)
		self.MatchScrollbarYDownText.pack( side = RIGHT, fill = Y )
		
		self.MatchTextDown = Text(self.MatchFrameDownLeft_2, font = self.ft, xscrollcommand = self.MatchScrollbarXDownText.set, yscrollcommand = self.MatchScrollbarYDownText.set, wrap = 'none')
		self.MatchTextDown.pack(fill = BOTH)
		
		self.MatchScrollbarXDownText.config( command = self.MatchTextDown.xview )
		self.MatchScrollbarYDownText.config( command = self.MatchTextDown.yview )
		# end down left frame 2

		# end down left Frame
		
		# start right frame
		self.MatchFrameRight = ttk.LabelFrame(self.MatchRoot, text = "")
		self.MatchFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.MatchButtonReset = ttk.Button(self.MatchFrameRight, text = "Reset", command = self.MatchReset) 
		self.MatchButtonReset.pack(fill = X, side = TOP)

		self.MatchButtonSetSource = ttk.Button(self.MatchFrameRight, text = "Add Source txt", command = self.MatchAddSource) 
		self.MatchButtonSetSource.pack(fill = X, side = TOP)

		self.MatchButtonSetDict = ttk.Button(self.MatchFrameRight, text = "Set Dict Path", command = self.MatchAddDirection) 
		self.MatchButtonSetDict.pack(fill = X, side = TOP)

		self.MatchLableBlank = ttk.Label(self.MatchFrameRight)
		self.MatchLableBlank.pack(side = TOP, fill = X)

		self.MatchLableBlank = ttk.Label(self.MatchFrameRight, text = "mode 1: Use every line in dict as key")
		self.MatchLableBlank.pack(side = TOP, fill = X, pady = 2)

		self.MatchLableBlank = ttk.Label(self.MatchFrameRight, text = "mode 2: Use every two characters in dict as key")
		self.MatchLableBlank.pack(side = TOP, fill = X, pady = 2)

		self.MatchLableBlank = ttk.Label(self.MatchFrameRight, text = "mode 3: Use every single character in dict as key")
		self.MatchLableBlank.pack(side = TOP, fill = X, pady = 2)

		values = ('mode 1', 'mode 2', 'mode 3')

		self.MatchComboModeVar = StringVar()
		self.MatchComboMode = ttk.Combobox(self.MatchFrameRight, textvariable = self.MatchComboModeVar, state="readonly")
		self.MatchComboMode["values"] = values
		self.MatchComboMode.current(0) 
		self.MatchComboMode.pack(fill = X)

		self.MatchButtonCheckString = ttk.Button(self.MatchFrameRight, text = "Check String", command = self.MatchCheckText)
		self.MatchButtonCheckString.pack(side = TOP, fill = X)

		self.MatchLableBlank = ttk.Label(self.MatchFrameRight)
		self.MatchLableBlank.pack(side = TOP, fill = X)

		self.MatchButtonCheckTxt = ttk.Button(self.MatchFrameRight, text = "Check txt", command = self.MatchCheckTxt)
		self.MatchButtonCheckTxt.pack(side = TOP, fill = X)

		self.MatchLableBlank = ttk.Label(self.MatchFrameRight)
		self.MatchLableBlank.pack(side = TOP, fill = X)

		# end right frame