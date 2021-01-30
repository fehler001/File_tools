#coding=utf-8
#File_tools/file/Refine_enfold.py

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



class CreateFrameRefine():

	def __init__(self):
		super().__init__()

		self.RefineRoot = None
		self.RefinePath = ''



	def RefineDefault(self):

		self.RefineDefaultLog()
		self.CreateWidgetsFrameRefine()
		self.RefineRestoreState()


	def RefineDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'refine' in j['file_tools']['file']:
			j['file_tools']['file']['refine'] = {}
		if not 'path_refine' in j['file_tools']['file']['refine']:
			j['file_tools']['file']['refine']['path_refine'] = ''
		if not 'check_samename' in j['file_tools']['file']['refine']:
			j['file_tools']['file']['refine']['check_samename'] = 1
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def RefineRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.RefineEntryPath.insert(0, j['file_tools']['file']['refine']['path_refine'])
		self.RefineCheckSamenameVar.set( j['file_tools']['file']['refine']['check_samename'] )
		f.close()


	

	def ReadRefinePath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.RefinePath = j['file_tools']['file']['refine']['path_refine']
		f.close()

	

	def RefineSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['file']['refine']['path_refine'] = self.RefineEntryPath.get()
			j['file_tools']['file']['refine']['check_samename'] = self.RefineCheckSamenameVar.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def RefineReset(self):
		self.RefineEntryPath.delete(0, "end")
		self.RefineTextDownFolders.delete("1.0", "end")
		self.RefineSaveEntry()
	

	def RefineCheckRepeat(self):
		folders = self.RefineTextDownFolders.get("1.0", "end")  #"end-1c" till second last charactor
		self.RefineTextDownFolders.delete("1.0", "end")
		folders = folders.split('\n')
		folders = set(folders)
		folders = sorted(folders, key=self.natsort_key2)
		folders.reverse()
		for folder in folders:
			if folder == '\n' or folder == '':
				continue
			self.RefineTextDownFolders.insert(INSERT, folder)
			self.RefineTextDownFolders.insert(INSERT, '\n')
	

	def RefineAddDirection(self):
		self.ReadRefinePath()
		p = self.RefinePath
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		self.RefineEntryPath.delete(0, "end")
		self.RefineEntryPath.insert(0, dir)
		self.RefinePath = dir



	def RefineDetect(self):
		self.ReadRefinePath()
		is_samename = self.RefineCheckSamenameVar.get()
		dir = self.RefinePath
		try: 
			if dir == '':
				return
			self.RefineTextDownFolders.delete("1.0", "end")
			self.RefineSaveEntry()
			enfolded = self.fl.find_enfold(dir, is_samename = is_samename)
			for folder in enfolded:
				self.RefineTextDownFolders.insert(INSERT, folder)
				self.RefineTextDownFolders.insert(INSERT, '\n')
		except: pass
		self.RefineCheckRepeat()
		if len(self.RefineTextDownFolders.get("1.0", "end") ) < 4:
			self.RefineTextDownFolders.insert(INSERT, "Nothing detected")
			self.RefineTextDownFolders.insert(INSERT, '\n')
		


	def Refine(self):
		folders = self.RefineTextDownFolders.get("1.0", "end")  #"end-1c" till second last charactor
		if len(folders) < 5:
			messagebox.showerror ("Warrning", "_____EMPTY BOX_____")
			return
		folders = folders.split('\n')
		tmp = messagebox.askquestion("Excute Refine", "There is no going back !\n\n        Are you sure?")
		if tmp != 'yes':
			return
		keep_name = self.RefineRadioKeepNameVar.get()
		self.fl.refine_enfold(folders, keep_name = keep_name)
		self.RefineTextDownFolders.delete("1.0", "end")
		self.RefineTextDownFolders.insert(INSERT, "Finished")




	def RefineRadioKeepNameToggle(self):
		pass



	def CreateWidgetsFrameRefine(self):

		# start up left Frame
		self.RefineFrameUpLeft = ttk.LabelFrame(self.RefineRoot, text = "")
		self.RefineFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)

		self.RefineLabelPath = ttk.Label(self.RefineFrameUpLeft, text = "Refine Folder Path", anchor = W)
		self.RefineLabelPath.pack(side = TOP, fill = X)
		
		self.RefineScrollbarXPath = ttk.Scrollbar(self.RefineFrameUpLeft, orient = HORIZONTAL)
		self.RefineScrollbarXPath.pack( side = BOTTOM, fill = X )
		
		self.RefineEntryPath = ttk.Entry(self.RefineFrameUpLeft, font = self.ft, xscrollcommand = self.RefineScrollbarXPath.set)
		self.RefineEntryPath.pack(fill = X)

		self.RefineEntryPath.drop_target_register(DND_FILES, DND_TEXT)
		self.RefineEntryPath.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.RefineLabelBlank = ttk.Label(self.RefineFrameUpLeft)
		self.RefineLabelBlank.pack(side = TOP, fill = X)

		self.RefineLabelDescription = ttk.Label(self.RefineFrameUpLeft, text = 'Description:     "c:\\foo\\bar\\bar  ->  c:\\foo\\bar"\n\n\
Walk through the root direction recursively, detect the folloing conditions and satisfying each of one in same time\n\n\
1. Child folder in parent folder and the names of two are exactly same\n\n\
2. Child is the solely folder with no other files in the parent\n\n\
3. Root folder is not counted\n\n\
( If you are in the "Refine" pending folder, it will not success )\n\n\
			', anchor = W)
		self.RefineLabelDescription.pack(side = TOP, fill = X)
		
		self.RefineScrollbarXPath.config( command = self.RefineEntryPath.xview )
		# end up left Frame
		
		# start down left Frame
		self.RefineFrameDownLeft = ttk.LabelFrame(self.RefineRoot, text = r'Detected     ( if multiple nested, it will process from inside to outside )')
		self.RefineFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.RefineScrollbarXDownFolders = ttk.Scrollbar(self.RefineFrameDownLeft, orient = HORIZONTAL)
		self.RefineScrollbarXDownFolders.pack( side = BOTTOM, fill = X )
		
		self.RefineScrollbarYDownFolders = ttk.Scrollbar(self.RefineFrameDownLeft, orient = VERTICAL)
		self.RefineScrollbarYDownFolders.pack( side = RIGHT, fill = Y )
		
		self.RefineTextDownFolders = Text(self.RefineFrameDownLeft, font = self.ft, xscrollcommand = self.RefineScrollbarXDownFolders.set, yscrollcommand = self.RefineScrollbarYDownFolders.set, wrap = 'none')
		self.RefineTextDownFolders.pack(fill = BOTH)
		
		self.RefineScrollbarXDownFolders.config( command = self.RefineTextDownFolders.xview )
		self.RefineScrollbarYDownFolders.config( command = self.RefineTextDownFolders.yview )
		# end down left Frame
		
		# start right frame
		self.RefineFrameRight = ttk.LabelFrame(self.RefineRoot, text = "")
		self.RefineFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.RefineButtonReset = ttk.Button(self.RefineFrameRight, text = "Reset", command = self.RefineReset) 
		self.RefineButtonReset.pack(fill = X, side = TOP)
		
		self.RefineLabelBlank = ttk.Label(self.RefineFrameRight)
		self.RefineLabelBlank.pack(side = TOP, fill = X)
		
		self.RefineButtonAddDirection = ttk.Button(self.RefineFrameRight, text = "Add Direction", command = self.RefineAddDirection) 
		self.RefineButtonAddDirection.pack(fill = X, side = TOP)
		
		self.RefineLabelBlank = ttk.Label(self.RefineFrameRight)
		self.RefineLabelBlank.pack(side = TOP, fill = X)

		self.RefineCheckSamenameVar = IntVar()
		self.RefineCheckSamename = ttk.Checkbutton(self.RefineFrameRight, text = "Exactly Samename ( condition 1 )", \
											variable = self.RefineCheckSamenameVar, onvalue = 1, offvalue = 0) 
		self.RefineCheckSamename.pack(fill = X, side = TOP)
		self.RefineCheckSamenameVar.set(1)
				
		self.RefineButtonDetect = ttk.Button(self.RefineFrameRight, text = "Detect", command = self.RefineDetect) 
		self.RefineButtonDetect.pack(fill = X, side = TOP)
		
		self.RefineLabelBlank = ttk.Label(self.RefineFrameRight)
		self.RefineLabelBlank.pack(side = TOP, fill = X)

		self.RefineRadioKeepNameVar = StringVar()
		self.RefineRadioKeepName = ttk.Radiobutton(self.RefineFrameRight, text = 'Keep Name = Outside  ', 
					variable = self.RefineRadioKeepNameVar, value = 'outside', command = self.RefineRadioKeepNameToggle)
		self.RefineRadioKeepName.pack(fill = X, side = TOP)
		self.RefineRadioKeepName.invoke()

		self.RefineRadioZip = ttk.Radiobutton(self.RefineFrameRight, text = "Keep Name = Inside", 
					variable = self.RefineRadioKeepNameVar, value = 'inside', command = self.RefineRadioKeepNameToggle)
		self.RefineRadioZip.pack(fill = X, side = TOP)

		self.RefineButtonRefine = ttk.Button(self.RefineFrameRight, text = "Refine", command = self.Refine) #bg = "#e1e1e1"
		self.RefineButtonRefine.pack(side = TOP, fill = X)
		# end right frame