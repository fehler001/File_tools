#coding=utf-8
#File_tools/file/Move_copy_delete.py


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



class CreateFrameMove():

	def __init__(self):
		super().__init__()

		self.MoveRoot = None
		self.MovePath = ''
		


	def MoveDefault(self):
		self.MoveDefaultLog()
		self.CreateWidgetsFrameMove()
		self.MoveRestoreState()

		

	def MoveDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'move' in j['file_tools']['file']:
			j['file_tools']['file']['move'] = {}
		if not 'path_move' in j['file_tools']['file']['move']:
			j['file_tools']['file']['move']['path_move'] = ''
		if not 'check_new_folder' in j['file_tools']['file']['move']:
			j['file_tools']['file']['move']['check_new_folder'] = 0
		if not 'name_new_folder' in j['file_tools']['file']['move']:
			j['file_tools']['file']['move']['name_new_folder'] = ''
		if not 'check_seperate' in j['file_tools']['file']['move']:
			j['file_tools']['file']['move']['check_seperate'] = 0
		if not 'interval' in j['file_tools']['file']['move']:
			j['file_tools']['file']['move']['interval'] = ''
		if not 'check_skip_exist' in j['file_tools']['file']['move']:
			j['file_tools']['file']['move']['check_skip_exist'] = 0
		if not 'check_delete_including_readonly' in j['file_tools']['file']['move']:
			j['file_tools']['file']['move']['check_delete_including_readonly'] = 1
		if not 'check_delete_skip_error' in j['file_tools']['file']['move']:
			j['file_tools']['file']['move']['check_delete_skip_error'] = 0
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def MoveRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.MovePath = j['file_tools']['file']['move']['path_move']
		self.MoveEntryPath.insert(0, self.MovePath)
		self.MoveCheckCreatingVar.set( j['file_tools']['file']['move']['check_new_folder'])
		self.MoveEntryCreating.insert(0, j['file_tools']['file']['move']['name_new_folder'])
		self.MoveCheckIntervalVar.set( j['file_tools']['file']['move']['check_seperate'])
		self.MoveEntryInterval.insert(0, j['file_tools']['file']['move']['interval'])
		self.MoveCheckSkipVar.set( j['file_tools']['file']['move']['check_skip_exist'])
		self.MoveCheckReadOnlyVar.set( j['file_tools']['file']['move']['check_delete_including_readonly'])
		self.MoveCheckSkipDeleteVar.set( j['file_tools']['file']['move']['check_delete_skip_error'])
		f.close()

	

	def ReadMovePath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.FilterPath = j['file_tools']['file']['move']['path_move']
		f.close()
	

	def MoveSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['file']['move']['path_move'] = self.MoveEntryPath.get()
			j['file_tools']['file']['move']['check_new_folder'] = self.MoveCheckCreatingVar.get()
			j['file_tools']['file']['move']['name_new_folder'] = self.MoveEntryCreating.get()
			j['file_tools']['file']['move']['check_seperate'] = self.MoveCheckIntervalVar.get()
			j['file_tools']['file']['move']['interval'] = self.MoveEntryInterval.get()
			j['file_tools']['file']['move']['check_skip_exist'] = self.MoveCheckSkipVar.get()
			j['file_tools']['file']['move']['check_delete_including_readonly'] = self.MoveCheckReadOnlyVar.get()
			j['file_tools']['file']['move']['check_delete_skip_error'] = self.MoveCheckSkipDeleteVar.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def MoveReset(self):
		self.MoveEntryPath.delete(0, "end")
		self.MoveTextDownFiles.delete("1.0", "end")
		self.MoveSaveEntry()
	

	def MoveCheckRepeat(self):
		files = self.MoveTextDownFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.MoveTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		files = set(files)
		files = sorted(files, key=self.natsort_key2)
		for file in files:
			if file == '\n' or file == '':
				continue
			self.MoveTextDownFiles.insert(INSERT, file)
			self.MoveTextDownFiles.insert(INSERT, '\n')
	

	def MoveAddDirection(self):
		self.ReadMovePath()
		p = self.MovePath
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.MoveEntryPath.delete(0, "end")
			self.MoveEntryPath.insert(0, dir)
			self.MovePath = dir
			self.MoveSaveEntry()
		except:pass


	def Move(self):
		self.MoveOrCopy(IsMove = 1)


	def Copy(self):
		self.MoveOrCopy(IsMove = 0)


	def MoveOrCopy(self, IsMove):
		self.MoveSaveEntry()
		lines = self.MoveTextDownFiles.get("1.0", "end")
		if len(lines) < 5:
			messagebox.showerror ("Warrning", "_____EMPTY BOX_____")
			return
		dir = self.MovePath
		if not os.path.isdir(dir):
			messagebox.showerror ("Warrning", "_____PATH ERROR_____")
			return
		lines = lines.split('\n')
		new_folder_name = self.MoveEntryCreating.get()
		if self.bl.check_legit_string(new_folder_name) == -1:
			return
		is_creating_new_folder = self.MoveCheckCreatingVar.get()
		interval = self.MoveEntryInterval.get()
		if self.bl.check_legit_int(interval) == -1:
			return
		is_interval = self.MoveCheckIntervalVar.get()
		interval = abs(int(interval))
		skip = self.MoveCheckSkipVar.get()
		tmp = messagebox.askquestion("Excute", "This may cause your file 'CHAOS'\n\nAre you sure?")
		if tmp == 'no':
			return
		tmp = messagebox.askquestion("Second Confirming", "Are you really sure?")
		if tmp == 'no':
			return
		if self.fl.move_or_copy(lines, dir, is_creating_new_folder, new_folder_name, is_interval, interval, skip, IsMove) == -1:
			return
		self.MoveTextDownFiles.delete("1.0", "end")


	def Delete(self):
		self.MoveSaveEntry()
		lines = self.MoveTextDownFiles.get("1.0", "end")
		if len(lines) < 5:
			messagebox.showerror ("Warrning", "_____EMPTY BOX_____")
			return
		tmp = messagebox.askquestion("First Confirming", "Are you sure?")
		if tmp == 'no':
			return
		tmp = messagebox.askquestion("Second Confirming", "Are you really sure?")
		if tmp == 'no':
			return
		lines = lines.split('\n')
		read_only = self.MoveCheckReadOnlyVar.get()
		skip_error_delete = self.MoveCheckSkipDeleteVar.get()
		if self.fl.delete_list(lines, including_read_only = read_only, skip_error = skip_error_delete) == -1:
			return
		self.MoveTextDownFiles.delete("1.0", "end")



	def ReadRename(self):
		self.MoveSaveEntry()
		files = self.RenameTextUpFiles.get("1.0", "end")
		files = files.split('\n')
		for file in files:
			if file == '\n' or file == '':
				continue
			self.MoveTextDownFiles.insert(INSERT, file)
			self.MoveTextDownFiles.insert(INSERT, '\n')
		self.MoveCheckRepeat()


	def ReadFilter(self):
		self.MoveSaveEntry()
		files = self.FilterTextDownFiles.get("1.0", "end")
		files = files.split('\n')
		for file in files:
			if file == '\n' or file == '':
				continue
			self.MoveTextDownFiles.insert(INSERT, file)
			self.MoveTextDownFiles.insert(INSERT, '\n')
		self.MoveCheckRepeat()


	def ReadFind(self):
		self.MoveSaveEntry()
		files = self.FindTextDownFiles.get("1.0", "end")
		files = files.split('\n')
		for file in files:
			if file == '\n' or file == '':
				continue
			self.MoveTextDownFiles.insert(INSERT, file)
			self.MoveTextDownFiles.insert(INSERT, '\n')
		self.MoveCheckRepeat()


	def MoveClearLeft(self):
		self.MoveSaveEntry()
		self.MoveTextDownFiles.delete("1.0", "end")


	def MoveSetInterval(self):
		if self.MoveCheckCreatingVar.get() == 0:
			self.MoveCheckIntervalVar.set(0)


	def CreateWidgetsFrameMove(self):

		# start up left Frame
		self.MoveFrameUpLeft = ttk.LabelFrame(self.MoveRoot, text = "")
		self.MoveFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)

		self.MoveLabelMove = ttk.Label(self.MoveFrameUpLeft, text = "Path where you want to move something to", anchor = W)
		self.MoveLabelMove.pack(side = TOP, fill = X)
		
		self.MoveScrollbarXPath = ttk.Scrollbar(self.MoveFrameUpLeft, orient = HORIZONTAL)
		self.MoveScrollbarXPath.pack( side = BOTTOM, fill = X )
		
		self.MoveEntryPath = ttk.Entry(self.MoveFrameUpLeft, font = self.ft, xscrollcommand = self.MoveScrollbarXPath.set)
		self.MoveEntryPath.pack(fill = X)

		self.MoveEntryPath.drop_target_register(DND_FILES, DND_TEXT)
		self.MoveEntryPath.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.MoveLabelBlank = ttk.Label(self.MoveFrameUpLeft)
		self.MoveLabelBlank.pack(side = TOP, fill = X)

		self.MoveLabelDescription = ttk.Label(self.MoveFrameUpLeft, text = 'Usage:\n\n\
1. Set the destination path, Read files or folders from "Rename" upbox or "Filter"\n\n\
2. If you want to move files to a new folder in destination, check the "Creating..." and fill a folder name\n\n\
3. If you want to seperate files into multiple folders, check the "Seperating..." and fill a interval number \n\
   (example: "1.txt", "2.txt"..."10.txt" will be moved into new folder "xxx1-10" if you fill "10" in the entry)\n\n\
4. If you check "Skip...", this app will not show error when there is already a file or folder with same name in the destination\n\
   (Thought thoroughly when you choose to "Move")\n\n\
			', anchor = W)
		self.MoveLabelDescription.pack(side = TOP, fill = X)
		
		self.MoveScrollbarXPath.config( command = self.MoveEntryPath.xview )
		# end up left Frame
		
		# start down left Frame
		self.MoveFrameDownLeft = ttk.LabelFrame(self.MoveRoot, text = r'Files')
		self.MoveFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.MoveScrollbarXDownFolders = ttk.Scrollbar(self.MoveFrameDownLeft, orient = HORIZONTAL)
		self.MoveScrollbarXDownFolders.pack( side = BOTTOM, fill = X )
		
		self.MoveScrollbarYDownFolders = ttk.Scrollbar(self.MoveFrameDownLeft, orient = VERTICAL)
		self.MoveScrollbarYDownFolders.pack( side = RIGHT, fill = Y )
		
		self.MoveTextDownFiles = Text(self.MoveFrameDownLeft, font = self.ft, xscrollcommand = self.MoveScrollbarXDownFolders.set, yscrollcommand = self.MoveScrollbarYDownFolders.set, wrap = 'none')
		self.MoveTextDownFiles.pack(fill = BOTH)
		
		self.MoveScrollbarXDownFolders.config( command = self.MoveTextDownFiles.xview )
		self.MoveScrollbarYDownFolders.config( command = self.MoveTextDownFiles.yview )
		# end down left Frame
		
		# start right frame
		self.MoveFrameRight = ttk.LabelFrame(self.MoveRoot, text = "")
		self.MoveFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.MoveButtonReset = ttk.Button(self.MoveFrameRight, text = "Reset", command = self.MoveReset) 
		self.MoveButtonReset.pack(fill = X, side = TOP)
		
		self.MoveLabelBlank = ttk.Label(self.MoveFrameRight)
		self.MoveLabelBlank.pack(side = TOP, fill = X)

		self.MoveButtonSetDestination = ttk.Button(self.MoveFrameRight, text = "Set Move or Copy Root Path", command = self.MoveAddDirection) 
		self.MoveButtonSetDestination.pack(fill = X, side = TOP)

		self.MoveCheckCreatingVar = IntVar() # StringVar()
		self.MoveCheckCreating = ttk.Checkbutton(self.MoveFrameRight, text = "Creating New Folder ( in root direction )", \
variable = self.MoveCheckCreatingVar, onvalue = 1, offvalue = 0, command = self.MoveSetInterval )
		self.MoveCheckCreating.pack(fill = X, side = TOP)
		self.MoveCheckCreatingVar.set(0)
				
		self.MoveEntryCreating = ttk.Entry(self.MoveFrameRight, font = self.ft)
		self.MoveEntryCreating.pack(fill = X)

		self.MoveCheckIntervalVar = IntVar() # StringVar()
		self.MoveCheckInterval = ttk.Checkbutton(self.MoveFrameRight, text = "Seperating Files ( fill interval number )", \
variable = self.MoveCheckIntervalVar, onvalue = 1, offvalue = 0, command = lambda: self.MoveCheckCreatingVar.set(1) ) 
		self.MoveCheckInterval.pack(fill = X, side = TOP)
		self.MoveCheckIntervalVar.set(0)
				
		self.MoveEntryInterval = ttk.Entry(self.MoveFrameRight, font = self.ft)
		self.MoveEntryInterval.pack(fill = X)

		self.MoveLabelBlank = ttk.Label(self.MoveFrameRight)
		self.MoveLabelBlank.pack(side = TOP, fill = X)

		self.MoveCheckSkipVar = IntVar() # StringVar()
		self.MoveCheckSkip = ttk.Checkbutton(self.MoveFrameRight, text = "Skip when file (or folder) exists", \
											variable = self.MoveCheckSkipVar, onvalue = 1, offvalue = 0) 
		self.MoveCheckSkip.pack(fill = X, side = TOP)
		self.MoveCheckSkipVar.set(0)

		self.MoveButtonMove = ttk.Button(self.MoveFrameRight, text = "Move", command = self.Move) #bg = "#e1e1e1"
		self.MoveButtonMove.pack(side = TOP, fill = X)

		self.MoveLabelBlank = ttk.Label(self.MoveFrameRight)
		self.MoveLabelBlank.pack(side = TOP, fill = X)

		self.MoveButtonMove = ttk.Button(self.MoveFrameRight, text = "Copy", command = self.Copy) #bg = "#e1e1e1"
		self.MoveButtonMove.pack(side = TOP, fill = X)

		self.MoveLabelBlank = ttk.Label(self.MoveFrameRight)
		self.MoveLabelBlank.pack(side = TOP, fill = X)

		self.MoveLabelBlank = ttk.Label(self.MoveFrameRight)
		self.MoveLabelBlank.pack(side = TOP, fill = X)

		self.MoveLabelBlank = ttk.Label(self.MoveFrameRight, text = "TAKE RESPONSIBILITY BY YOUR SELF")
		self.MoveLabelBlank.pack(side = TOP, fill = X)

		self.MoveCheckReadOnlyVar = IntVar() # StringVar()
		self.MoveCheckReadOnly = ttk.Checkbutton(self.MoveFrameRight, text = "Including Read Only (recommended)", \
											variable = self.MoveCheckReadOnlyVar, onvalue = 1, offvalue = 0) 
		self.MoveCheckReadOnly.pack(fill = X, side = TOP)
		self.MoveCheckReadOnlyVar.set(1)

		self.MoveCheckSkipDeleteVar = IntVar() # StringVar()
		self.MoveCheckSkipDelete = ttk.Checkbutton(self.MoveFrameRight, text = "Skip When Get Error", \
											variable = self.MoveCheckSkipDeleteVar, onvalue = 1, offvalue = 0) 
		self.MoveCheckSkipDelete.pack(fill = X, side = TOP)
		self.MoveCheckSkipDeleteVar.set(0)

		self.MoveButtonMove = ttk.Button(self.MoveFrameRight, text = "DELETE ALL FILES IN LEFT BOX", command = self.Delete) #bg = "#e1e1e1"
		self.MoveButtonMove.pack(side = TOP, fill = X)

		self.MoveButtonReadFilter = ttk.Button(self.MoveFrameRight, text = "Read Find", command = self.ReadFind) #bg = "#e1e1e1"
		self.MoveButtonReadFilter.pack(side = BOTTOM, fill = X)

		self.MoveButtonReadFilter = ttk.Button(self.MoveFrameRight, text = "Read Filter", command = self.ReadFilter) #bg = "#e1e1e1"
		self.MoveButtonReadFilter.pack(side = BOTTOM, fill = X)

		self.MoveButtonReadRename = ttk.Button(self.MoveFrameRight, text = "Read Rename (upbox)", command = self.ReadRename) #bg = "#e1e1e1"
		self.MoveButtonReadRename.pack(side = BOTTOM, fill = X)

		self.MoveLabelBlank = ttk.Label(self.MoveFrameRight)
		self.MoveLabelBlank.pack(side = BOTTOM, fill = X)

		self.MoveButtonClear = ttk.Button(self.MoveFrameRight, text = "Clear Left", command = self.MoveClearLeft) #bg = "#e1e1e1"
		self.MoveButtonClear.pack(side = BOTTOM, fill = X)

		self.MoveLabelBlank = ttk.Label(self.MoveFrameRight)
		self.MoveLabelBlank.pack(side = BOTTOM, fill = X)
		# end right frame