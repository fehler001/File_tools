#coding=utf-8
#File_tools/file/Checksum.py

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


class CreateFrameCsum():

	def __init__(self):
		super().__init__()

		self.CsumRoot = None

		self.CsumPath = ''



	def CsumDefault(self):

		self.CsumDefaultLog()
		self.CreateWidgetsFrameCsum()
		self.CsumRestoreState()
		

	def CsumDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'checksum' in j['file_tools']['file']:
			j['file_tools']['file']['checksum'] = {}
		if not 'path' in j['file_tools']['file']['checksum']:
			j['file_tools']['file']['checksum']['path'] = ''
		if not 'combo_mode' in j['file_tools']['file']['checksum']:
			j['file_tools']['file']['checksum']['combo_mode'] = 'MD5'
		if not 'entry_compare' in j['file_tools']['file']['checksum']:
			j['file_tools']['file']['checksum']['entry_compare'] = ''
		if not 'text' in j['file_tools']['file']['checksum']:
			j['file_tools']['file']['checksum']['text'] = ''
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()




	def CsumRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.CsumPath = j['file_tools']['file']['checksum']['path']
		self.CsumEntryPath.insert(0, self.CsumPath)
		self.CsumEntrySum2.insert(0, j['file_tools']['file']['checksum']['entry_compare'] )
		self.CsumComboMode.set(j['file_tools']['file']['checksum']['combo_mode'])
		self.CsumText.insert(INSERT, j['file_tools']['file']['checksum']['text'] )
		f.close()


	

	def ReadCsumPath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.CsumPath = j['file_tools']['file']['checksum']['path']
		f.close()



	def CsumSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['file']['checksum']['path'] = self.CsumEntryPath.get()
			j['file_tools']['file']['checksum']['entry_compare'] = self.CsumEntrySum2.get()
			j['file_tools']['file']['checksum']['combo_mode'] = self.CsumComboMode.get()
			t = self.CsumText.get('1.0', 'end')
			if t[-1] == '\n':
				j['file_tools']['file']['checksum']['text'] = t[0:-1]
			else:
				j['file_tools']['file']['checksum']['text'] = t
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def CsumReset(self):
		self.CsumEntryPath.delete(0, "end")
		self.CsumEntrySum1.delete(0, "end")
		self.CsumSaveEntry()
	


	def CsumAddFile(self):
		self.ReadCsumPath()
		p = self.CsumPath
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(initialdir = p) 
		else:
			dir = filedialog.askopenfilename(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.CsumEntryPath.delete(0, "end")
			self.CsumEntryPath.insert(0, dir)
			self.CsumPath = dir
			self.CsumSaveEntry()
		except:pass
	


	def CsumReadClipboard(self):
		self.CsumEntrySum2.delete(0, "end")
		self.CsumEntrySum2.insert(INSERT, self.root.clipboard_get() )



	def CsumCopyResult(self):
		self.root.clipboard_append( self.CsumEntrySum1.get() )
		


	def CsumCalculate(self):
		self.CsumSaveEntry()
		self.CsumEntrySum1.delete(0, "end")
		if self.bl.check_path_exist([self.CsumPath], isfile = 1) == -1:
			return
		mode = self.CsumComboMode.get()
		f = open(self.CsumPath, 'rb')
		b = f.read()
		rst = self.bl.get_checksum(b, mode)
		if rst == -1:
			return
		self.CsumEntrySum1.insert(0, rst)



	def CsumCompare(self):
		self.CsumSaveEntry()
		s1 = self.CsumEntrySum1.get()
		s2 = self.CsumEntrySum2.get()
		if s1.lower() == s2.lower():
			messagebox.showinfo("", 'same')
		else:
			messagebox.showinfo("", 'different')





	def CreateWidgetsFrameCsum(self):

		# start up left Frame
		self.CsumFrameUpLeft = ttk.LabelFrame(self.CsumRoot, text = "")
		self.CsumFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.55)

		# start Frame1
		self.CsumFrame1 = ttk.Frame(self.CsumFrameUpLeft)
		self.CsumFrame1.pack(side = TOP, fill = X)

		self.CsumScrollbarXPath = ttk.Scrollbar(self.CsumFrame1, orient = HORIZONTAL)
		self.CsumScrollbarXPath.pack( side = BOTTOM, fill = X )

		self.CsumLablePath = ttk.Label(self.CsumFrame1, text = "File", anchor = W)
		self.CsumLablePath.pack(side = TOP, fill = X)
		
		self.CsumEntryPath = ttk.Entry(self.CsumFrame1, font = self.ft, xscrollcommand = self.CsumScrollbarXPath.set)
		self.CsumEntryPath.pack(fill = X)

		self.CsumEntryPath.drop_target_register(DND_FILES, DND_TEXT)
		self.CsumEntryPath.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.CsumScrollbarXPath.config( command = self.CsumEntryPath.xview )
		# end Frame1

		self.CsumLableBlank = ttk.Label(self.CsumFrameUpLeft)
		self.CsumLableBlank.pack(side = TOP, fill = X)

		# start Frame2
		self.CsumFrame2 = ttk.Frame(self.CsumFrameUpLeft)
		self.CsumFrame2.pack(side = TOP, fill = X)

		self.CsumScrollbarXSum1 = ttk.Scrollbar(self.CsumFrame2, orient = HORIZONTAL)
		self.CsumScrollbarXSum1.pack( side = BOTTOM, fill = X )

		self.CsumLableSum1 = ttk.Label(self.CsumFrame2, text = "Result", anchor = W)
		self.CsumLableSum1.pack(side = TOP, fill = X)
		
		self.CsumEntrySum1 = ttk.Entry(self.CsumFrame2, font = self.ft, xscrollcommand = self.CsumScrollbarXSum1.set)
		self.CsumEntrySum1.pack(fill = X)

		self.CsumScrollbarXSum1.config( command = self.CsumEntrySum1.xview )
		# end Frame2

		self.CsumButtonCopy = ttk.Button(self.CsumFrameUpLeft, text = "             Copy             ", command = self.CsumCopyResult) 
		self.CsumButtonCopy.pack(anchor = W, side = TOP)

		self.CsumLableBlank = ttk.Label(self.CsumFrameUpLeft)
		self.CsumLableBlank.pack(side = TOP, fill = X)

		# start Frame3
		self.CsumFrame3 = ttk.Frame(self.CsumFrameUpLeft)
		self.CsumFrame3.pack(side = TOP, fill = X)

		self.CsumScrollbarXSum2 = ttk.Scrollbar(self.CsumFrame3, orient = HORIZONTAL)
		self.CsumScrollbarXSum2.pack( side = BOTTOM, fill = X )

		self.CsumLableSum2 = ttk.Label(self.CsumFrame3, text = "Paste here to compare ( this entry will be saved when exit )", anchor = W)
		self.CsumLableSum2.pack(side = TOP, fill = X)
		
		self.CsumEntrySum2 = ttk.Entry(self.CsumFrame3, font = self.ft, xscrollcommand = self.CsumScrollbarXSum2.set)
		self.CsumEntrySum2.pack(fill = X)

		self.CsumScrollbarXSum2.config( command = self.CsumEntrySum2.xview )
		# end Frame3

		# start Frame4
		self.CsumFrame3 = ttk.Frame(self.CsumFrameUpLeft)
		self.CsumFrame3.pack(side = TOP, fill = X)

		self.CsumButtonCompare = ttk.Button(self.CsumFrame3, text = "         Compare          ", command = self.CsumCompare)
		self.CsumButtonCompare.pack(side = LEFT, fill = X)

		self.CsumButtonRead = ttk.Button(self.CsumFrame3, text = "    Read Clipboard    ", command = self.CsumReadClipboard) 
		self.CsumButtonRead.pack(anchor = W, side = LEFT)
		# end Frame4

		# end up left Frame
		

		# start down left Frame
		self.CsumFrameDownLeft = ttk.LabelFrame(self.CsumRoot, text = '')
		self.CsumFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.56, relheight = 0.43)

		self.CsumScrollbarXText = ttk.Scrollbar(self.CsumFrameDownLeft, orient = HORIZONTAL)
		self.CsumScrollbarXText.pack( side = BOTTOM, fill = X )
		
		self.CsumScrollbarYText = ttk.Scrollbar(self.CsumFrameDownLeft, orient = VERTICAL)
		self.CsumScrollbarYText.pack( side = RIGHT, fill = Y )
		
		self.CsumText = Text(self.CsumFrameDownLeft, font = self.ft, xscrollcommand = self.CsumScrollbarXText.set, yscrollcommand = self.CsumScrollbarYText.set, wrap = 'none')
		self.CsumText.pack(fill = BOTH)
		
		self.CsumScrollbarXText.config( command = self.CsumText.xview )
		self.CsumScrollbarYText.config( command = self.CsumText.yview )
		# end down left Frame
		
		# start right frame
		self.CsumFrameRight = ttk.LabelFrame(self.CsumRoot, text = "")
		self.CsumFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.CsumButtonReset = ttk.Button(self.CsumFrameRight, text = "Reset", command = self.CsumReset) 
		self.CsumButtonReset.pack(fill = X, side = TOP)

		self.CsumLableBlank = ttk.Label(self.CsumFrameRight)
		self.CsumLableBlank.pack(side = TOP, fill = X)

		self.CsumButtonAddFile = ttk.Button(self.CsumFrameRight, text = "Add File", command = self.CsumAddFile) 
		self.CsumButtonAddFile.pack(fill = X, side = TOP)

		self.CsumLableBlank = ttk.Label(self.CsumFrameRight)
		self.CsumLableBlank.pack(side = TOP, fill = X)

		self.CsumLableBlank = ttk.Label(self.CsumFrameRight, text = "Mode:")
		self.CsumLableBlank.pack(side = TOP, fill = X)

		values = ('MD5', 'SHA1', 'SHA256', 'SHA384', 'SHA512', 'CRC-8', 'CRC-16', 'CRC-32', 'CRC-64')

		self.CsumComboModeVar = StringVar()
		self.CsumComboMode = ttk.Combobox(self.CsumFrameRight, textvariable = self.CsumComboModeVar, state="readonly")
		self.CsumComboMode["values"] = values
		self.CsumComboMode.current(0) 
		self.CsumComboMode.pack(fill = X)
		#comboxlist.bind("<<ComboboxSelected>>", fun)   # when one item selected, fun()

		self.CsumButtonCalculate = ttk.Button(self.CsumFrameRight, text = "Calculate", command = self.CsumCalculate)
		self.CsumButtonCalculate.pack(side = TOP, fill = X)

		self.CsumLableBlank = ttk.Label(self.CsumFrameRight)
		self.CsumLableBlank.pack(side = TOP, fill = X)

		

		# end right frame