#coding=utf-8
#File_tools/file/Remove_empty_folder.py

import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog 
import os
import sys
import json
import copy

import tkinterdnd2 
from tkinterdnd2 import *



class CreateFrameRemove():

	def __init__(self):
		
		self.RemoveRoot = None
		self.RemovePath = ''



	def RemoveDefault(self):

		self.RemoveDefaultLog()
		self.CreateWidgetsFrameRemove()
		self.RemoveRestoreState()
		

	def RemoveDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'remove_empty_folder' in j['file_tools']['file']:
			j['file_tools']['file']['remove_empty_folder'] = {}
		if not 'path_remove' in j['file_tools']['file']['remove_empty_folder']:
			j['file_tools']['file']['remove_empty_folder']['path_remove'] = ''
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def RemoveRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.RemoveEntryPath.insert(0, j['file_tools']['file']['remove_empty_folder']['path_remove'] )
		f.close()

	

	def ReadRemovePath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.RemovePath = j['file_tools']['file']['remove_empty_folder']['path_remove']
		f.close()
	

	def RemoveSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['file']['remove_empty_folder']['path_remove'] = self.RemoveEntryPath.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def RemoveReset(self):
		self.RemoveEntryPath.delete(0, "end")
		self.RemoveTextDownFolders.delete("1.0", "end")
		self.RemoveSaveEntry()
	

	def RemoveCheckRepeat(self):
		folders = self.RemoveTextDownFolders.get("1.0", "end")  #"end-1c" till second last charactor
		self.RemoveTextDownFolders.delete("1.0", "end")
		folders = folders.split('\n')
		folders = set(folders)
		folders = sorted(folders, key=self.natsort_key2)
		for folder in folders:
			if folder == '\n' or folder == '':
				continue
			self.RemoveTextDownFolders.insert(INSERT, folder)
			self.RemoveTextDownFolders.insert(INSERT, '\n')
	

	def RemoveAddDirection(self):
		self.ReadRemovePath()
		p = self.RemovePath
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		self.RemoveEntryPath.delete(0, "end")
		self.RemoveEntryPath.insert(0, dir)
		self.RemovePath = dir
		self.RemoveSaveEntry()



	def RemoveDetect(self):
		self.ReadRemovePath()
		self.RemoveSaveEntry()
		self.RemoveTextDownFolders.delete("1.0", "end")
		dir = self.RemovePath
		if dir == '':
			return
		folders = self.fl.find_empty_folder(dir)
		for folder in folders:
			self.RemoveTextDownFolders.insert(INSERT, folder)
			self.RemoveTextDownFolders.insert(INSERT, '\n')
		self.RemoveCheckRepeat()
		if len(self.RemoveTextDownFolders.get("1.0", "end") ) < 4:
			self.RemoveTextDownFolders.insert(INSERT, "Nothing detected")
			self.RemoveTextDownFolders.insert(INSERT, '\n')
		


	def Remove(self):
		folders = self.RemoveTextDownFolders.get("1.0", "end")  #"end-1c" till second last charactor
		if len(folders) < 5:
			messagebox.showerror ("Warrning", "_____EMPTY BOX_____")
			return
		folders = folders.split('\n')
		tmp = messagebox.askquestion("Excute Remove", "There is no going back !\n\n        Are you sure?")
		if tmp != 'yes':
			return
		for i in range(len(folders)):
			if len(folders[i]) < 5:
				continue
			try:
				os.rmdir(folders[i])
			except:
				pass
		self.RemoveTextDownFolders.delete("1.0", "end")
		self.RemoveTextDownFolders.insert(INSERT, "Finished")



	def CreateWidgetsFrameRemove(self):


		# start up left Frame
		self.RemoveFrameUpLeft = ttk.LabelFrame(self.RemoveRoot, text = "")
		self.RemoveFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)

		self.RemoveLabelPath = ttk.Label(self.RemoveFrameUpLeft, text = "Search Empty Folder Path", anchor = W)
		self.RemoveLabelPath.pack(side = TOP, fill = X)
		
		self.RemoveScrollbarXPath = ttk.Scrollbar(self.RemoveFrameUpLeft, orient = HORIZONTAL)
		self.RemoveScrollbarXPath.pack( side = BOTTOM, fill = X )
		
		self.RemoveEntryPath = ttk.Entry(self.RemoveFrameUpLeft, font = self.ft, xscrollcommand = self.RemoveScrollbarXPath.set)
		self.RemoveEntryPath.pack(fill = X)

		self.RemoveEntryPath.drop_target_register(DND_FILES, DND_TEXT)
		self.RemoveEntryPath.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.RemoveLabelBlank = ttk.Label(self.RemoveFrameUpLeft)
		self.RemoveLabelBlank.pack(side = TOP, fill = X)

		self.RemoveLabelDescription = ttk.Label(self.RemoveFrameUpLeft, text = "Description:\n\n\
1. Walk through the root direction recursively\n\n\
2. Scan for any empty folder then fill in the downside area\n\n\
			", anchor = W)
		self.RemoveLabelDescription.pack(side = TOP, fill = X)
		
		self.RemoveScrollbarXPath.config( command = self.RemoveEntryPath.xview )
		# end up left Frame
		
		# start down left Frame
		self.RemoveFrameDownLeft = ttk.LabelFrame(self.RemoveRoot, text = r'Empty Folders')
		self.RemoveFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.RemoveScrollbarXDownFolders = ttk.Scrollbar(self.RemoveFrameDownLeft, orient = HORIZONTAL)
		self.RemoveScrollbarXDownFolders.pack( side = BOTTOM, fill = X )
		
		self.RemoveScrollbarYDownFolders = ttk.Scrollbar(self.RemoveFrameDownLeft, orient = VERTICAL)
		self.RemoveScrollbarYDownFolders.pack( side = RIGHT, fill = Y )
		
		self.RemoveTextDownFolders = Text(self.RemoveFrameDownLeft, font = self.ft, \
xscrollcommand = self.RemoveScrollbarXDownFolders.set, yscrollcommand = self.RemoveScrollbarYDownFolders.set, wrap = 'none')
		self.RemoveTextDownFolders.pack(fill = BOTH)
		
		self.RemoveScrollbarXDownFolders.config( command = self.RemoveTextDownFolders.xview )
		self.RemoveScrollbarYDownFolders.config( command = self.RemoveTextDownFolders.yview )
		# end down left Frame
		
		# start right frame
		self.RemoveFrameRight = ttk.LabelFrame(self.RemoveRoot, text = "")
		self.RemoveFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.RemoveButtonReset = ttk.Button(self.RemoveFrameRight, text = "Reset", command = self.RemoveReset) 
		self.RemoveButtonReset.pack(fill = X, side = TOP)
		
		self.RemoveLabelBlank = ttk.Label(self.RemoveFrameRight)
		self.RemoveLabelBlank.pack(side = TOP, fill = X)
		
		self.RemoveButtonAddDirection = ttk.Button(self.RemoveFrameRight, text = "Add Direction", command = self.RemoveAddDirection) 
		self.RemoveButtonAddDirection.pack(fill = X, side = TOP)
		
		self.RemoveLabelBlank = ttk.Label(self.RemoveFrameRight)
		self.RemoveLabelBlank.pack(side = TOP, fill = X)
				
		self.RemoveLabelBlank = ttk.Label(self.RemoveFrameRight)
		self.RemoveLabelBlank.pack(side = TOP, fill = X)

		

		self.RemoveButtonDetect = ttk.Button(self.RemoveFrameRight, text = "Detect", command = self.RemoveDetect) 
		self.RemoveButtonDetect.pack(fill = X, side = TOP)

		self.RemoveLabelBlank = ttk.Label(self.RemoveFrameRight)
		self.RemoveLabelBlank.pack(side = TOP, fill = X)

		self.RemoveButtonRemove = ttk.Button(self.RemoveFrameRight, text = "Remove", command = self.Remove) #bg = "#e1e1e1"
		self.RemoveButtonRemove.pack(side = TOP, fill = X)
		# end right frame