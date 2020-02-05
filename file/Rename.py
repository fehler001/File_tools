#coding=utf-8
#File_tools/file/Rename.py


import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog 
import os
import sys
import json
import copy



class CreateFrameRename():

	def __init__(self):
		super().__init__()
		self.NRenameTimes = 0
		self.RenameVarNameUp = []
		self.RenameVarNameDown = []

		self.RenameRoot = None
		self.RenamePath = ''
		self.RenameDigit = 1
		self.RenameOutset = 1
		self.RenamePosition = 0
		


	def RenameDefault(self):

		self.RenameDefaultLog()
		self.CreateWidgetsFrameRename()
		self.RenameRestoreState()



	def RenameDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'rename' in j['file_tools']['file']:
			j['file_tools']['file']['rename'] = {}
		if not 'path_rename' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['path_rename'] = '.'
		if not 'check_files' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['check_files'] = '1'
		if not 'check_folders' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['check_folders'] = '0'
		if not 'entry_digit' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['entry_digit'] = ''
		if not 'entry_outset' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['entry_outset'] = ''
		if not 'insert_string' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['insert_string'] = ''
		if not 'insert_position' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['insert_position'] = ''
		if not 'replace_original' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['replace_original'] = ''
		if not 'replace_substitute' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['replace_substitute'] = ''
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def RenameRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.RenamePath = j['file_tools']['file']['rename']['path_rename']
		self.RenameCheckFileVar.set( int(j['file_tools']['file']['rename']['check_files']) )
		self.RenameCheckFolderVar.set( int(j['file_tools']['file']['rename']['check_folders']) )
		self.RenameEntryDigit.insert(0, j['file_tools']['file']['rename']['entry_digit'])
		self.RenameEntryOutset.insert(0, j['file_tools']['file']['rename']['entry_outset'])
		self.RenameEntryInsertPosition.insert(0, j['file_tools']['file']['rename']['insert_position'])
		self.RenameEntryInsertString.insert(0, j['file_tools']['file']['rename']['insert_string'])
		self.RenameEntryReplaceOriginal.insert(0, j['file_tools']['file']['rename']['replace_original'])
		self.RenameEntryReplaceSubstitute.insert(0, j['file_tools']['file']['rename']['replace_substitute'])
		f.close()

	

	def ReadRenamePath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.RenamePath = j['file_tools']['file']['rename']['path_rename']
		f.close()
	


	def RenameSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['file']['rename']['path_rename'] = self.RenamePath
			j['file_tools']['file']['rename']['check_files'] = str( self.RenameCheckFileVar.get() )
			j['file_tools']['file']['rename']['check_folders'] = str( self.RenameCheckFolderVar.get() )
			j['file_tools']['file']['rename']['entry_digit'] = self.RenameEntryDigit.get()
			j['file_tools']['file']['rename']['entry_outset'] = self.RenameEntryOutset.get()
			j['file_tools']['file']['rename']['insert_position'] = self.RenameEntryInsertPosition.get()
			j['file_tools']['file']['rename']['insert_string'] = self.RenameEntryInsertString.get()
			j['file_tools']['file']['rename']['replace_original'] = self.RenameEntryReplaceOriginal.get()
			j['file_tools']['file']['rename']['replace_substitute'] = self.RenameEntryReplaceSubstitute.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def RenameReset(self):
		self.RenameTextUpFiles.delete("1.0", "end")
		self.RenameTextDownFiles.delete("1.0", "end")
		self.RenameSaveEntry()
	

	def RenameCheckRepeatUp(self):
		files = self.RenameTextUpFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.RenameTextUpFiles.delete("1.0", "end")
		files = files.split('\n')
		files = set(files)
		files = sorted(files, key=self.natsort_key2)
		for file in files:
			if file == '\n' or file == '':
				continue
			self.RenameTextUpFiles.insert(INSERT, file)
			self.RenameTextUpFiles.insert(INSERT, '\n')
	

	def RenameEliminateNullDown(self):
		files = self.RenameTextDownFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.RenameTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		for file in files:
			if file == '\n' or file == '':
				continue
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
	

	def RenameAddFiles(self):
		self.ReadRenamePath()
		if os.path.isdir(self.RenamePath):
			files = filedialog.askopenfilenames(initialdir = self.RenamePath) 
		else:
			files = filedialog.askopenfilenames(initialdir = self.RenamePath[0 : self.RenamePath.rfind(r'/')] ) 
		try: 
			self.RenamePath =  files[0][0 : files[0].rfind(r'/')] 
			self.RenameSaveEntry()
			for file in files:
				self.RenameTextUpFiles.insert(INSERT, file)
				self.RenameTextUpFiles.insert(INSERT, '\n')
			self.RenameTextDownFiles.delete("1.0", "end")
		except: pass
		self.RenameCheckRepeatUp()


	def RenameAddDirection(self):
		self.ReadRenamePath()
		if os.path.isdir(self.RenamePath):
			direction = filedialog.askdirectory(initialdir = self.RenamePath) 
		else:
			direction = filedialog.askdirectory(initialdir = self.RenamePath[0 : self.RenamePath.rfind(r'/')] ) 
		try: 
			self.RenamePath =  direction
			self.RenameSaveEntry()
			files = self.fl.collect_files_and_folders(direction, self.RenameCheckFileVar.get(), self.RenameCheckFolderVar.get() )
			for file in files:
				self.RenameTextUpFiles.insert(INSERT, file)
				self.RenameTextUpFiles.insert(INSERT, '\n')
			self.RenameTextDownFiles.delete("1.0", "end")
		except: pass
		self.RenameCheckRepeatUp()


	def RenameAddOneFolder(self):
		self.ReadRenamePath()
		if os.path.isdir(self.RenamePath):
			direction = filedialog.askdirectory(initialdir = self.RenamePath) 
		else:
			direction = filedialog.askdirectory(initialdir = self.RenamePath[0 : self.RenamePath.rfind(r'/')] ) 
		try: 
			self.RenamePath =  direction
			self.RenameSaveEntry()
			self.RenameTextUpFiles.insert(INSERT, direction)
			self.RenameTextUpFiles.insert(INSERT, '\n')
			self.RenameTextDownFiles.delete("1.0", "end")
		except: pass
		self.RenameCheckRepeatUp()
	

	def RenameInitializeEntry(self):
		if self.RenameEntryOutset.get() == '':
			self.RenameEntryOutset.insert(0, 1)
		outset = self.RenameEntryOutset.get()
		if self.bl.check_legit_int(outset) == -1:
			return
		self.RenameOutset = int(outset)

		if self.RenameEntryDigit.get() == '':
			self.RenameEntryDigit.insert(0, 1)
		digit = self.RenameEntryDigit.get()
		if self.bl.check_legit_int(digit) == -1:
			return
		self.RenameDigit = int(digit)

		if self.RenameEntryInsertPosition.get() == '':
			self.RenameEntryInsertPosition.insert(0, 0)
		pos = self.RenameEntryInsertPosition.get()
		if self.bl.check_legit_int(pos) == -1:
			return
		self.RenamePosition = int(pos)


	def RenameByOrdinal(self):
		self.RenameInitializeEntry()
		self.RenameSaveEntry()
		if len(str(self.RenameEntryDigit.get() )) > 2:
			messagebox.showerror ("ERROR", "Rename By Ordinal: Digit\n\n" + 'Under 100, please')
			return
		files = self.RenameTextUpFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.RenameTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		
		files = self.fl.rename_by_ordinal(files, self.RenameDigit, self.RenameOutset)
		for file in files:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameEliminateNullDown()
	

	def InsertString(self):
		self.RenameInitializeEntry()
		self.RenameSaveEntry()
		files = self.RenameTextUpFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.RenameTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		cont = self.RenameEntryInsertString.get()
		if self.bl.check_legit_string(cont) == -1:
			return
		files = self.fl.insert(files, self.RenamePosition, cont)
		for file in files:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameEliminateNullDown()




	def InsertOrdinal(self):
		self.RenameInitializeEntry()
		self.RenameSaveEntry()
		files = self.RenameTextUpFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.RenameTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		files = self.fl.insert(files, pos = self.RenamePosition, cont = '', is_ordinal = True, digit = self.RenameDigit, outset = self.RenameOutset)
		for file in files:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameEliminateNullDown()
	

	def Replace(self):
		self.RenameSaveEntry()
		files = self.RenameTextUpFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.RenameTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		original = self.RenameEntryReplaceOriginal.get()
		substitute = self.RenameEntryReplaceSubstitute.get()
		if self.bl.check_legit_string(substitute) == -1:
			return
		files = self.fl.replace_string(files, original, substitute)
		for file in files:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameEliminateNullDown()
	

	def Rename(self, SwitchRevoke = False):
		self.RenameSaveEntry()
		self.RenameCheckRepeatUp()
		self.RenameEliminateNullDown()
		UpFiles = self.RenameTextUpFiles.get("1.0", "end")  #"end-1c" till second last charactor
		DownFiles = self.RenameTextDownFiles.get("1.0", "end")
		if (len(UpFiles) < 5 or len(DownFiles) < 5):
			messagebox.showerror ("Warrning", "_____EMPTY BOX_____")
			return
		UpFiles = UpFiles.split('\n')
		DownFiles = DownFiles.split('\n')
		if len(UpFiles) != len(DownFiles):
			messagebox.showerror ("Warrning", "The quantity of files in two boxes are not equal\n\nPlease check again\n\n( Maybe missing one 'enter' )")
			return
		if SwitchRevoke is False:
			tmp = messagebox.askquestion("Excute Rename", "Are you sure?")
			if tmp == 'no':
				return
		for i in range(len(UpFiles)):
			if UpFiles[i] == DownFiles[i]:
				continue
			if os.path.exists(DownFiles[i]):
				messagebox.showerror ("Warrning", DownFiles[i] + "\nalready exist")
				return
		for i in range(len(UpFiles)):
			if UpFiles[i] == DownFiles[i]:
				continue
			try:
				os.rename(UpFiles[i], DownFiles[i])
			except:
				pass
		self.RenameTextUpFiles.delete("1.0", "end")
		self.RenameTextUpFiles.insert(INSERT, self.RenameTextDownFiles.get("1.0", "end"))
		self.RenameTextDownFiles.delete("1.0", "end")
		
		if SwitchRevoke is False:
			self.RenameVarNameUp.append('TextUp' + str(self.NRenameTimes))
			globals()[self.RenameVarNameUp[self.NRenameTimes]] = UpFiles     # local var declare: exec(VarNameUp[NRenameTimes] + " = UpFiles")
			self.RenameVarNameDown.append('TextDown' + str(self.NRenameTimes))
			globals()[self.RenameVarNameDown[self.NRenameTimes]] = DownFiles
			self.NRenameTimes = self.NRenameTimes + 1
		self.RenameCheckRepeatUp()

	

	def Revoke(self):
		if self.NRenameTimes == 0:
			messagebox.showerror ("ERROR", "There is no back anymore!")
			return
		tmp = messagebox.askquestion("Excute Revoke", "Are you really sure?")
		if tmp == 'no':
			return
		self.RenameTextUpFiles.delete("1.0", "end")
		files = globals()[self.RenameVarNameDown[self.NRenameTimes - 1]]
		for file in files:
			self.RenameTextUpFiles.insert(INSERT, file)
			self.RenameTextUpFiles.insert(INSERT, '\n')
		self.RenameTextDownFiles.delete("1.0", "end")
		files = globals()[self.RenameVarNameUp[self.NRenameTimes - 1]]
		for file in files:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.Rename(SwitchRevoke = True)
		self.RenameVarNameUp.pop()        # or del VarNameUp[-1]
		self.RenameVarNameDown.pop()
		self.NRenameTimes = self.NRenameTimes - 1
		self.RenameCheckRepeatUp()


	def CreateWidgetsFrameRename(self):

		

		# start up left Frame
		self.RenameFrameUpLeft = ttk.LabelFrame(self.RenameRoot, text = "Files")
		self.RenameFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)
		
		self.RenameScrollbarXUpfiles = ttk.Scrollbar(self.RenameFrameUpLeft, orient = HORIZONTAL)
		self.RenameScrollbarXUpfiles.pack( side = BOTTOM, fill = X )
		
		self.RenameScrollbarYUpfiles = ttk.Scrollbar(self.RenameFrameUpLeft, orient = VERTICAL)
		self.RenameScrollbarYUpfiles.pack( side = RIGHT, fill = Y )
		
		self.RenameTextUpFiles = Text(self.RenameFrameUpLeft, xscrollcommand = self.RenameScrollbarXUpfiles.set, yscrollcommand = self.RenameScrollbarYUpfiles.set, wrap = 'none')
		self.RenameTextUpFiles.pack(fill = BOTH)
		
		self.RenameScrollbarXUpfiles.config( command = self.RenameTextUpFiles.xview )
		self.RenameScrollbarYUpfiles.config( command = self.RenameTextUpFiles.yview )
		# end up left Frame
		
		# start down left Frame
		self.RenameFrameDownLeft = ttk.LabelFrame(self.RenameRoot, text = "Results    ( Revoke files and folders at same time could cause your filename 'CAHOS' )")
		self.RenameFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.RenameScrollbarXDownfiles = ttk.Scrollbar(self.RenameFrameDownLeft, orient = HORIZONTAL)
		self.RenameScrollbarXDownfiles.pack( side = BOTTOM, fill = X )
		
		self.RenameScrollbarYDownfiles = ttk.Scrollbar(self.RenameFrameDownLeft, orient = VERTICAL)
		self.RenameScrollbarYDownfiles.pack( side = RIGHT, fill = Y )
		
		self.RenameTextDownFiles = Text(self.RenameFrameDownLeft, xscrollcommand = self.RenameScrollbarXDownfiles.set, yscrollcommand = self.RenameScrollbarYDownfiles.set, wrap = 'none')
		self.RenameTextDownFiles.pack(fill = BOTH)
		
		self.RenameScrollbarXDownfiles.config( command = self.RenameTextDownFiles.xview )
		self.RenameScrollbarYDownfiles.config( command = self.RenameTextDownFiles.yview )
		# end down left Frame
		
		# start right frame
		self.RenameFrameRight = ttk.LabelFrame(self.RenameRoot, text = "")
		self.RenameFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.RenameButtonReset = ttk.Button(self.RenameFrameRight, text = "Reset", command = self.RenameReset) 
		self.RenameButtonReset.pack(fill = X, side = TOP)

		self.RenameButtonAddOneFolder = ttk.Button(self.RenameFrameRight, text = "Add One Folder", command = self.RenameAddOneFolder) 
		self.RenameButtonAddOneFolder.pack(fill = X, side = TOP)
			
		self.RenameButtonAddFiles = ttk.Button(self.RenameFrameRight, text = "Add Files", command = self.RenameAddFiles) 
		self.RenameButtonAddFiles.pack(fill = X, side = TOP)
		
		self.RenameCheckFileVar = IntVar() # StringVar()
		self.RenameCheckFile = ttk.Checkbutton(self.RenameFrameRight, text = "Including Files", \
											variable = self.RenameCheckFileVar, onvalue = 1, offvalue = 0) 
		self.RenameCheckFile.pack(fill = X, side = TOP)
		self.RenameCheckFileVar.set(1)

		self.RenameCheckFolderVar = IntVar()
		self.RenameCheckFolder = ttk.Checkbutton(self.RenameFrameRight, text = "Including Folders", \
											variable = self.RenameCheckFolderVar, onvalue = 1, offvalue = 0) 
		self.RenameCheckFolder.pack(fill = X, side = TOP)
		self.RenameCheckFolderVar.set(0)

		self.RenameButtonAddDirection = ttk.Button(self.RenameFrameRight, text = "Add Direction", command = self.RenameAddDirection) 
		self.RenameButtonAddDirection.pack(fill = X, side = TOP)

		
		
		self.RenameLableDigit = ttk.Label(self.RenameFrameRight, text = "Digit", anchor = W)
		self.RenameLableDigit.pack(side = TOP, fill = X)
		
		self.RenameEntryDigit = ttk.Entry(self.RenameFrameRight)
		self.RenameEntryDigit.pack(side = TOP, fill = X)

		self.RenameLableOutset = ttk.Label(self.RenameFrameRight, text = "Outset", anchor = W)
		self.RenameLableOutset.pack(side = TOP, fill = X)
		
		self.RenameEntryOutset = ttk.Entry(self.RenameFrameRight)
		self.RenameEntryOutset.pack(side = TOP, fill = X)
		
		self.RenameButtonRenameByOrdinal = ttk.Button(self.RenameFrameRight, text = "Rename By Ordinal", command = self.RenameByOrdinal)
		self.RenameButtonRenameByOrdinal.pack(side = TOP, fill = X)
		
		self.RenameLableInsertString = ttk.Label(self.RenameFrameRight, text = "Insert: String", anchor = W)
		self.RenameLableInsertString.pack(side = TOP, fill = X)
		
		self.RenameEntryInsertString = ttk.Entry(self.RenameFrameRight)
		self.RenameEntryInsertString.pack(side = TOP, fill = X)

		self.RenameLableInsertPosition = ttk.Label(self.RenameFrameRight, text = "Insert: Postion ('-1' = end)", anchor = W)
		self.RenameLableInsertPosition.pack(side = TOP, fill = X)
		
		self.RenameEntryInsertPosition = ttk.Entry(self.RenameFrameRight)
		self.RenameEntryInsertPosition.pack(side = TOP, fill = X)
		
		self.RenameButtonInsertString = ttk.Button(self.RenameFrameRight, text = "Insert String", command = self.InsertString)
		self.RenameButtonInsertString.pack(side = TOP, fill = X)
		
		self.RenameButtonInsertOrdinal = ttk.Button(self.RenameFrameRight, text = "Insert Ordinal", command = self.InsertOrdinal)
		self.RenameButtonInsertOrdinal.pack(side = TOP, fill = X)
		
		self.RenameLableReplaceOriginal = ttk.Label(self.RenameFrameRight, text = "Replce: Original ", anchor = W)
		self.RenameLableReplaceOriginal.pack(side = TOP, fill = X)
		
		self.RenameEntryReplaceOriginal = ttk.Entry(self.RenameFrameRight)
		self.RenameEntryReplaceOriginal.pack(side = TOP, fill = X)
		
		self.RenameLableReplaceSubstitute = ttk.Label(self.RenameFrameRight, text = "Replce: Substitute", anchor = W)
		self.RenameLableReplaceSubstitute.pack(side = TOP, fill = X)
		
		self.RenameEntryReplaceSubstitute = ttk.Entry(self.RenameFrameRight)
		self.RenameEntryReplaceSubstitute.pack(side = TOP, fill = X)
		
		self.RenameButtonInsertEnd = ttk.Button(self.RenameFrameRight, text = "Replace", command = self.Replace)
		self.RenameButtonInsertEnd.pack(side = TOP, fill = X)
		
		self.RenameButtonRevoke = ttk.Button(self.RenameFrameRight, text = "Revoke", command = self.Revoke) #bg = "#e1e1e1"
		self.RenameButtonRevoke.pack(fill = X, side = BOTTOM)
		
		self.RenameButtonRename = ttk.Button(self.RenameFrameRight, text = "Rename", command = self.Rename) #bg = "#e1e1e1"
		self.RenameButtonRename.pack(fill = X, side = BOTTOM)
		# end right frame