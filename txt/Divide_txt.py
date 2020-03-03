#coding=utf-8
#File_tools/txt/Divide_txt.py

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



class CreateFrameDivide():

	def __init__(self):
		super().__init__()

		self.DivideRoot = None

		self.DivideTxtPath = ''
		self.DivideSavePath = ''



	def DivideDefault(self):

		self.DivideDefaultLog()
		self.CreateWidgetsFrameDivide()
		self.DivideRestoreState()
		

	def DivideDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'divide_txt' in j['file_tools']['txt']:
			j['file_tools']['txt']['divide_txt'] = {}
		if not 'path_txt' in j['file_tools']['txt']['divide_txt']:
			j['file_tools']['txt']['divide_txt']['path_txt'] = ''
		if not 'path_save' in j['file_tools']['txt']['divide_txt']:
			j['file_tools']['txt']['divide_txt']['path_save'] = ''
		if not 'entry_digit' in j['file_tools']['txt']['divide_txt']:
			j['file_tools']['txt']['divide_txt']['entry_digit'] = ''
		if not 'entry_limit' in j['file_tools']['txt']['divide_txt']:
			j['file_tools']['txt']['divide_txt']['entry_limit'] = ''
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()




	def DivideRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.DivideTxtPath = j['file_tools']['txt']['divide_txt']['path_txt']
		self.DivideSavePath = j['file_tools']['txt']['divide_txt']['path_save']
		self.DivideEntryTxtSource.insert(0, self.DivideTxtPath)
		self.DivideEntryTxtDestination.insert(0, self.DivideSavePath )
		self.DivideEntryDigit.insert(0, j['file_tools']['txt']['divide_txt']['entry_digit'])
		self.DivideEntryLimit.insert(0, j['file_tools']['txt']['divide_txt']['entry_limit'])
		f.close()


	

	def ReadDividePath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.DivideTxtPath = j['file_tools']['txt']['divide_txt']['path_txt']
		self.DivideSavePath = j['file_tools']['txt']['divide_txt']['path_save']
		f.close()



	def DivideSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['txt']['divide_txt']['path_txt'] = self.DivideEntryTxtSource.get()
			j['file_tools']['txt']['divide_txt']['path_save'] = self.DivideEntryTxtDestination.get()
			j['file_tools']['txt']['divide_txt']['entry_digit'] = self.DivideEntryDigit.get()
			j['file_tools']['txt']['divide_txt']['entry_limit'] = self.DivideEntryLimit.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def DivideReset(self):
		self.DivideEntryTxtSource.delete(0, "end")
		self.DivideEntryTxtDestination.delete(0, "end")
		self.DivideSaveEntry()
	
	'''
	def DivideCheckRepeat(self):
		files = self.DivideTextDownFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.DivideTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		files = set(files)
		files = sorted(files, key=self.natsort_key2)
		for file in files:
			if file == '\n' or file == '':
				continue
			self.DivideTextDownFiles.insert(INSERT, file)
			self.DivideTextDownFiles.insert(INSERT, '\n')
	'''

	def DivideAddSource(self):
		self.ReadDividePath()
		p = self.DivideTxtPath
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(initialdir = p) 
		else:
			dir = filedialog.askopenfilename(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.DivideEntryTxtSource.delete(0, "end")
			self.DivideEntryTxtSource.insert(0, dir)
			self.DivideTxtPath = dir
			self.DivideSaveEntry()
		except:pass
	

	def DivideAddDirection(self):
		self.ReadDividePath()
		p = self.DivideSavePath
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.DivideEntryTxtDestination.delete(0, "end")
			self.DivideEntryTxtDestination.insert(0, dir)
			self.DivideSavePath = dir
			self.DivideSaveEntry()
		except:pass


	def Divide(self):
		self.DivideSaveEntry()
		self.DivideTextDownFiles.delete("1.0", "end")
		src = self.DivideEntryTxtSource.get()
		if not os.path.isfile(src):
			messagebox.showerror ("Warrning", "_____TXT SOURCE ERROR_____")
			return
		dst = self.DivideEntryTxtDestination.get()
		if not os.path.isdir(dst):
			messagebox.showerror ("Warrning", "_____PATH ERROR_____")
			return
		lines_limit = self.DivideEntryLimit.get()
		if self.bl.check_legit_int(lines_limit) == -1:
			return
		lines_limit = abs(int(lines_limit))
		digit = self.DivideEntryDigit.get()
		if self.bl.check_legit_int(digit) == -1:
			return
		digit = abs(int(digit))
		tmp = messagebox.askquestion("Excute", "Devide txt into multiple txt files?")
		if tmp == 'no':
			return
		if self.tl.divide_txt(src, dst, lines_limit = lines_limit, digit = digit) == -1:
			return
		self.DivideTextDownFiles.delete("1.0", "end")
		


	def CreateWidgetsFrameDivide(self):

		# start up left Frame
		self.DivideFrameUpLeft = ttk.LabelFrame(self.DivideRoot, text = "")
		self.DivideFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)

		# start Frame1
		self.DivideFrame1 = ttk.Frame(self.DivideFrameUpLeft)
		self.DivideFrame1.pack(side = TOP, fill = X)

		self.DivideScrollbarXTxtSource = ttk.Scrollbar(self.DivideFrame1, orient = HORIZONTAL)
		self.DivideScrollbarXTxtSource.pack( side = BOTTOM, fill = X )

		self.DivideLableTxtSource = ttk.Label(self.DivideFrame1, text = "Txt Source Path", anchor = W)
		self.DivideLableTxtSource.pack(side = TOP, fill = X)
		
		self.DivideEntryTxtSource = ttk.Entry(self.DivideFrame1, font = self.ft, xscrollcommand = self.DivideScrollbarXTxtSource.set)
		self.DivideEntryTxtSource.pack(fill = X)

		self.DivideEntryTxtSource.drop_target_register(DND_FILES, DND_TEXT)
		self.DivideEntryTxtSource.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.DivideScrollbarXTxtSource.config( command = self.DivideEntryTxtSource.xview )
		# end Frame1

		# start Frame2
		self.DivideFrame2 = ttk.Frame(self.DivideFrameUpLeft)
		self.DivideFrame2.pack(side = TOP, fill = X)

		self.DivideScrollbarXTxtDestination = ttk.Scrollbar(self.DivideFrame2, orient = HORIZONTAL)
		self.DivideScrollbarXTxtDestination.pack( side = BOTTOM, fill = X )

		self.DivideLableTxtDestination = ttk.Label(self.DivideFrame2, text = "Path where you want to put your new multiple txts", anchor = W)
		self.DivideLableTxtDestination.pack(side = TOP, fill = X)
		
		self.DivideEntryTxtDestination = ttk.Entry(self.DivideFrame2, font = self.ft, xscrollcommand = self.DivideScrollbarXTxtDestination.set)
		self.DivideEntryTxtDestination.pack(fill = X)

		self.DivideEntryTxtDestination.drop_target_register(DND_FILES, DND_TEXT)
		self.DivideEntryTxtDestination.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.DivideScrollbarXTxtDestination.config( command = self.DivideEntryTxtDestination.xview )
		# end Frame2

		self.DivideLableTxtDescription = ttk.Label(self.DivideFrameUpLeft, text = 'Description:\n\n\
src: mytxt.txt( line1, line2......line5000 )\n\n\
limit = 500, digit = 6\n\n\
dst: 000001.txt( line1, line2.....line500 ), ...... 000010.txt( line4501, line4502.....line5000 )\n\n\
			', anchor = W)
		self.DivideLableTxtDescription.pack(side = TOP, fill = X)
		# end up left Frame
		
		# start down left Frame
		self.DivideFrameDownLeft = ttk.LabelFrame(self.DivideRoot, text = r'Files')
		#self.DivideFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.DivideScrollbarXDownFolders = ttk.Scrollbar(self.DivideFrameDownLeft, orient = HORIZONTAL)
		self.DivideScrollbarXDownFolders.pack( side = BOTTOM, fill = X )
		
		self.DivideScrollbarYDownFolders = ttk.Scrollbar(self.DivideFrameDownLeft, orient = VERTICAL)
		self.DivideScrollbarYDownFolders.pack( side = RIGHT, fill = Y )
		
		self.DivideTextDownFiles = Text(self.DivideFrameDownLeft, xscrollcommand = self.DivideScrollbarXDownFolders.set, yscrollcommand = self.DivideScrollbarYDownFolders.set, wrap = 'none')
		self.DivideTextDownFiles.pack(fill = BOTH)
		
		self.DivideScrollbarXDownFolders.config( command = self.DivideTextDownFiles.xview )
		self.DivideScrollbarYDownFolders.config( command = self.DivideTextDownFiles.yview )
		# end down left Frame
		
		# start right frame
		self.DivideFrameRight = ttk.LabelFrame(self.DivideRoot, text = "")
		self.DivideFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.DivideButtonReset = ttk.Button(self.DivideFrameRight, text = "Reset", command = self.DivideReset) 
		self.DivideButtonReset.pack(fill = X, side = TOP)

		self.DivideLableBlank = ttk.Label(self.DivideFrameRight)
		self.DivideLableBlank.pack(side = TOP, fill = X)

		self.DivideButtonSetSource = ttk.Button(self.DivideFrameRight, text = "Add txt", command = self.DivideAddSource) 
		self.DivideButtonSetSource.pack(fill = X, side = TOP)
		
		self.DivideLableBlank = ttk.Label(self.DivideFrameRight)
		self.DivideLableBlank.pack(side = TOP, fill = X)

		self.DivideButtonSetDestination = ttk.Button(self.DivideFrameRight, text = "Set Save Path", command = self.DivideAddDirection) 
		self.DivideButtonSetDestination.pack(fill = X, side = TOP)

		self.DivideLableBlank = ttk.Label(self.DivideFrameRight)
		self.DivideLableBlank.pack(side = TOP, fill = X)

		self.DivideLableBlank = ttk.Label(self.DivideFrameRight, text = "txt Name Digit")
		self.DivideLableBlank.pack(side = TOP, fill = X)

		self.DivideEntryDigit = ttk.Entry(self.DivideFrameRight, font = self.ft)
		self.DivideEntryDigit.pack(fill = X)

		self.DivideLableBlank = ttk.Label(self.DivideFrameRight, text = "Set Limit Lines in Each txt")
		self.DivideLableBlank.pack(side = TOP, fill = X)

		self.DivideEntryLimit = ttk.Entry(self.DivideFrameRight, font = self.ft)
		self.DivideEntryLimit.pack(fill = X)

		self.DivideButtonDivide = ttk.Button(self.DivideFrameRight, text = "Divide txt", command = self.Divide) #bg = "#e1e1e1"
		self.DivideButtonDivide.pack(side = TOP, fill = X)

		self.DivideLableBlank = ttk.Label(self.DivideFrameRight)
		self.DivideLableBlank.pack(side = TOP, fill = X)

		# end right frame