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

import tkinterdnd2 
from tkinterdnd2 import *


class CreateFrameRename():

	def __init__(self):
		super().__init__()
		self.NRenameTimes = 0
		self.TextUp = {}
		self.TextDown = {}

		self.RenameRoot = None
		self.RenamePath = ''
		self.RenameDigit = 1
		self.RenameOutset = 1
		self.RenamePosition = 0
		self.RenameInterval = 'interval: 1'
		self.RenameP1 = 'Left Position: 0'
		self.RenameP2 = 'Right Position: -1'

		self.RenameN = 0
		


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
		if not 'n' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['n'] = 0
		if not 'path_rename' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['path_rename'] = ''
		if not 'check_files' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['check_files'] = 1
		if not 'check_folders' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['check_folders'] = 0
		if not 'check_recur' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['check_recur'] = 0
		if not 'combo_digit' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['combo_digit'] = 'digit: 1'
		if not 'combo_outset' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['combo_outset'] = 'outset: 1'
		if not 'combo_interval' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['combo_interval'] = 'interval: 1'
		if not 'insert_string' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['insert_string'] = ''
		if not 'insert_position' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['insert_position'] = ''
		if not 'check_old' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['check_old'] = 0
		if not 'replace_original' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['replace_original'] = ''
		if not 'replace_substitute' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['replace_substitute'] = ''
		if not 'replace_match' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['replace_match'] = 'match all'
		if not 'positon_left' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['positon_left'] = 'Left Positon: 0'
		if not 'positon_right' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['positon_right'] = 'Right Positon: -1'
		if not 'text_up' in j['file_tools']['file']['rename']:
			j['file_tools']['file']['rename']['text_up'] = ''
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def RenameRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.RenameN = j['file_tools']['file']['rename']['n']
		self.RenameFrameUpLeft.config(text = 'Files  ' + str(self.RenameN) )
		self.RenamePath = j['file_tools']['file']['rename']['path_rename']
		self.RenameCheckFileVar.set( j['file_tools']['file']['rename']['check_files'])
		self.RenameCheckFolderVar.set( j['file_tools']['file']['rename']['check_folders'])
		self.RenameCheckRecurVar.set( j['file_tools']['file']['rename']['check_recur'])
		self.RenameComboDigit.set( j['file_tools']['file']['rename']['combo_digit'])
		self.RenameComboOutset.set( j['file_tools']['file']['rename']['combo_outset'])
		self.RenameComboIntervalVar.set( j['file_tools']['file']['rename']['combo_interval'])
		self.RenameEntryInsertPosition.insert(0, j['file_tools']['file']['rename']['insert_position'])
		self.RenameEntryInsertString.insert(0, j['file_tools']['file']['rename']['insert_string'])
		self.RenameCheckDeleteOldVar.set( j['file_tools']['file']['rename']['check_old'] )
		self.RenameEntryReplaceOriginal.insert(0, j['file_tools']['file']['rename']['replace_original'])
		self.RenameEntryReplaceOriginal.focus()
		self.RenameTextUpFiles.focus()
		self.RenameEntryReplaceSubstitute.insert(0, j['file_tools']['file']['rename']['replace_substitute'])
		self.RenameComboMatchVar.set( j['file_tools']['file']['rename']['replace_match'])
		self.RenameComboP1.set( j['file_tools']['file']['rename']['positon_left'])
		self.RenameComboP2.set( j['file_tools']['file']['rename']['positon_right'])
		self.RenameTextUpFiles.delete('1.0', 'end')
		self.RenameTextUpFiles.insert(INSERT, j['file_tools']['file']['rename']['text_up'])
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
			j['file_tools']['file']['rename']['n'] = self.RenameN
			j['file_tools']['file']['rename']['path_rename'] = self.RenamePath
			j['file_tools']['file']['rename']['check_files'] = self.RenameCheckFileVar.get()
			j['file_tools']['file']['rename']['check_folders'] = self.RenameCheckFolderVar.get()
			j['file_tools']['file']['rename']['check_recur'] = self.RenameCheckRecurVar.get()
			j['file_tools']['file']['rename']['combo_digit'] = self.RenameComboDigit.get()
			j['file_tools']['file']['rename']['combo_outset'] = self.RenameComboOutset.get()
			j['file_tools']['file']['rename']['combo_interval'] = self.RenameComboIntervalVar.get()
			j['file_tools']['file']['rename']['insert_position'] = self.RenameEntryInsertPosition.get()
			j['file_tools']['file']['rename']['insert_string'] = self.RenameEntryInsertString.get()
			j['file_tools']['file']['rename']['check_old'] = self.RenameCheckDeleteOldVar.get()
			j['file_tools']['file']['rename']['replace_original'] = self.RenameEntryReplaceOriginal.get()
			j['file_tools']['file']['rename']['replace_substitute'] = self.RenameEntryReplaceSubstitute.get()
			j['file_tools']['file']['rename']['replace_match'] = self.RenameComboMatchVar.get()
			j['file_tools']['file']['rename']['positon_left'] = self.RenameComboP1.get()
			j['file_tools']['file']['rename']['positon_right'] = self.RenameComboP2.get()
			tmp = self.RenameTextUpFiles.get('1.0', 'end')
			if tmp[-1] == '\n': tmp = tmp[ :-1]
			j['file_tools']['file']['rename']['text_up'] = tmp 
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def RenameReset(self):
		self.RenameTextUpFiles.delete("1.0", "end")
		self.RenameTextDownFiles.delete("1.0", "end")
		self.RenameFrameUpLeft.config(text = 'Files')
		self.RenameN = 0
		self.RenameSaveEntry()
	

	def RenameCheckRepeatUp(self):
		files = self.RenameTextUpFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.RenameTextUpFiles.delete("1.0", "end")
		files = files.split('\n')
		files = set(files)
		files = sorted(files, key=self.natsort_key2)
		files = self.bl.clean_list(files)
		n = 0
		for file in files:
			file = file.replace('\\', '/')
			self.RenameTextUpFiles.insert(INSERT, file)
			self.RenameTextUpFiles.insert(INSERT, '\n')
			n = n + 1
		self.RenameFrameUpLeft.config(text = 'Files  ' + str(n) )
		self.RenameN = n
	

	def RenameEliminateNullDown(self):
		files = self.RenameTextDownFiles.get("1.0", "end")  
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
			files = self.fl.collect_files_and_folders(direction, \
				self.RenameCheckFileVar.get(), self.RenameCheckFolderVar.get(), self.RenameCheckRecurVar.get() )
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
		if self.RenameComboOutset.get() == '':
			self.RenameComboOutset.set('outset: 1')
		outset = self.RenameComboOutset.get()
		outset = outset[7:]
		if self.bl.check_legit_int(outset) == -1:
			return -1
		self.RenameOutset = int(outset)

		if self.RenameComboDigit.get() == '':
			self.RenameComboDigit.set('digit: 1')
		digit = self.RenameComboDigit.get()
		digit = digit[6:]
		if self.bl.check_legit_int(digit) == -1:
			return -1
		self.RenameDigit = int(digit)

		if self.RenameEntryInsertPosition.get() == '':
			self.RenameEntryInsertPosition.insert(0, 0)
		pos = self.RenameEntryInsertPosition.get()
		if self.bl.check_legit_int(pos) == -1:
			return -1
		self.RenamePosition = int(pos)

		if self.RenameComboIntervalVar.get() == '':
			self.RenameComboIntervalVar.set('interval: 1')
		interval = self.RenameComboIntervalVar.get()
		interval = interval[9:]
		if self.bl.check_legit_int(interval) == -1:
			return -1
		self.RenameInterval = int(interval)

		if self.RenameComboP1.get() == '':
			self.RenameComboP1.set('Left Positon: 0')
		left = self.RenameComboP1Var.get()
		left = left[13:]
		if self.bl.check_legit_int(left) == -1:
			return -1
		self.RenameP1 = int(left)

		if self.RenameComboP2.get() == '':
			self.RenameComboP2.set('Right Positon: 0')
		right = self.RenameComboP2Var.get()
		right = right[14:]
		if self.bl.check_legit_int(right) == -1:
			return -1
		self.RenameP2 = int(right)



	def RenameByOrdinal(self):
		self.RenameSaveEntry()
		if self.RenameInitializeEntry() == -1:
			return
		if len(str(self.RenameDigit )) > 2:
			messagebox.showerror ("ERROR", "Rename By Ordinal: Digit\n\n" + 'Under 100, please')
			return
		files = self.RenameTextUpFiles.get("1.0", "end") 
		files = files.split('\n')
		files = self.bl.clean_list(files)

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(files) == -1:
				return
		
		files = self.fl.rename_by_ordinal(files, self.RenameDigit, self.RenameOutset, self.RenameInterval)
		self.RenameTextDownFiles.delete("1.0", "end")
		for file in files:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameEliminateNullDown()
	

	def InsertString(self):
		self.RenameSaveEntry()
		if self.RenameInitializeEntry() == -1:
			return
		files = self.RenameTextUpFiles.get("1.0", "end") 
		files = files.split('\n')
		files = self.bl.clean_list(files)

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(files) == -1:
				return

		cont = self.RenameEntryInsertString.get()
		if self.bl.check_legit_string(cont) == -1:
			return
		files = self.fl.insert(files, pos = self.RenamePosition, cont = cont)
		self.RenameTextDownFiles.delete("1.0", "end")
		for file in files:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameEliminateNullDown()




	def InsertOrdinal(self):
		self.RenameSaveEntry()
		if self.RenameInitializeEntry() == -1:
			return
		files = self.RenameTextUpFiles.get("1.0", "end") 
		files = files.split('\n')
		files = self.bl.clean_list(files)

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(files) == -1:
				return

		new_files = []
		if self.RenameCheckDeleteOldVar.get() == 1:
			for file in files:
				file = self.fl.delete_front_ordinal(file)
				new_files.append(file)
		else:
			new_files = files
		ordinal = self.bl.generate_ordinal(length = len(new_files), 
								digit = self.RenameDigit, outset = self.RenameOutset, interval = self.RenameInterval)
		rst = self.fl.insert(new_files, pos = self.RenamePosition, cont = '', ordinal = ordinal)
		self.RenameTextDownFiles.delete("1.0", "end")
		for file in rst:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameEliminateNullDown()
	

	def Replace(self):
		self.RenameSaveEntry()
		files = self.RenameTextUpFiles.get("1.0", "end")
		files = files.split('\n')
		files = self.bl.clean_list(files)

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(files) == -1:
				return

		original = self.RenameEntryReplaceOriginal.get()
		substitute = self.RenameEntryReplaceSubstitute.get()
		match = self.RenameComboMatchVar.get()
		if self.bl.check_legit_string(substitute) == -1:
			return
		files = self.fl.replace_string(files, original, substitute, match)

		if files == -1: return
		if self.bl.check_has_repeat(files) == -1: return

		self.RenameTextDownFiles.delete("1.0", "end")
		for file in files:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameEliminateNullDown()
	


	def GetMiddle(self, get_middle = 1):
		self.RenameSaveEntry()
		if self.RenameInitializeEntry() == -1:
			return
		p1 = self.RenameP1
		p2 = self.RenameP2
		if p1 >= 0 and p2 >=0:
			if p1 >= p2:
				messagebox.showerror ("ERROR", '"Left Position" MUST < "Right position" !')
				return
		if p1 < 0 and p2 < 0:
			if p1 >= p2:
				messagebox.showerror ("ERROR", '"Left Position" MUST < "Right position" !')
				return
		files = self.RenameTextUpFiles.get("1.0", "end") 
		files = files.split('\n')
		files = self.bl.clean_list(files)

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(files) == -1:
				return
		
		new_files = []
		for file in files:
			new_file = self.fl.get_or_delete_middle_filename(file, p1, p2, get_middle = get_middle)
			if new_file == -1:
				new_files.append(file)
			else:
				new_files.append(new_file)
		if self.bl.check_has_repeat(new_files) == -1:
			return

		self.RenameTextDownFiles.delete("1.0", "end")
		for new_file in new_files:
			self.RenameTextDownFiles.insert(INSERT, new_file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameEliminateNullDown()


	def DeleteMiddle(self):
		self.GetMiddle(get_middle = 0)



	def Rename(self, SwitchRevoke = False):
		self.RenameSaveEntry()
		self.RenameEliminateNullDown()
		raw_UpFiles = self.RenameTextUpFiles.get("1.0", "end") 
		raw_DownFiles = self.RenameTextDownFiles.get("1.0", "end")
		if (len(raw_UpFiles) < 4 or len(raw_DownFiles) < 4):
			messagebox.showerror ("Warrning", "_____EMPTY BOX_____")
			return
		UpFiles = raw_UpFiles.split('\n')

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(UpFiles) == -1:
				return

		DownFiles = raw_DownFiles.split('\n')
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

		self.RenameCheckRepeatUp()
		
		if SwitchRevoke is False:
			if raw_UpFiles[-1] == '\n':
				self.TextUp[self.NRenameTimes] = raw_UpFiles[0:-1]     # local var declare: exec(VarNameUp[NRenameTimes] + " = UpFiles")
			else:
				self.TextUp[self.NRenameTimes] = raw_UpFiles

			if raw_DownFiles[-1] == '\n':
				self.TextDown[self.NRenameTimes] = raw_DownFiles[0:-1]
			else:
				self.TextDown[self.NRenameTimes] = raw_DownFiles

			self.NRenameTimes = self.NRenameTimes + 1
		

	

	def Revoke(self):
		if self.NRenameTimes == 0:
			messagebox.showerror ("ERROR", "There is no back anymore!")
			return
		tmp = messagebox.askquestion("Excute Revoke", "Are you really sure?")
		if tmp == 'no':
			return

		self.RenameTextUpFiles.delete("1.0", "end")
		files = self.TextDown[self.NRenameTimes - 1]
		self.RenameTextUpFiles.insert(INSERT, files)

		self.RenameTextDownFiles.delete("1.0", "end")
		files = self.TextUp[self.NRenameTimes - 1]
		self.RenameTextDownFiles.insert(INSERT, files)

		self.Rename(SwitchRevoke = True)
		del self.TextDown[self.NRenameTimes - 1]
		del self.TextUp[self.NRenameTimes - 1]
		self.NRenameTimes = self.NRenameTimes - 1

		self.RenameCheckRepeatUp()




	def RenameEntryOriginalFocusIn(self, _):
			if self.RenameEntryReplaceOriginal.get() == " ? = one character, * = any characters":
				self.RenameEntryReplaceOriginal.delete(0, END)
				self.RenameEntryReplaceOriginal.config( foreground = "black" )
				#print(full_name_entry.config()['foreground'][-1])   # get foreground colour
			
	def RenameEntryOriginalFocusOut(self, _):
		if self.RenameEntryReplaceOriginal.get() == '':
			self.RenameEntryReplaceOriginal.delete(0, END)
			self.RenameEntryReplaceOriginal.config( foreground = "grey")
			self.RenameEntryReplaceOriginal.insert(0, " ? = one character, * = any characters")
	
	#def RenameEntryOriginalFocusEnter(self):
	#	print( self.RenameEntryReplaceOriginal.get() )



	def CreateWidgetsFrameRename(self):

		# start up left Frame		
		self.RenameFrameUpLeft = ttk.LabelFrame(self.RenameRoot, text = "Files")
		self.RenameFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)
		
		self.RenameScrollbarXUpfiles = ttk.Scrollbar(self.RenameFrameUpLeft, orient = HORIZONTAL)
		self.RenameScrollbarXUpfiles.pack( side = BOTTOM, fill = X )
		
		self.RenameScrollbarYUpfiles = ttk.Scrollbar(self.RenameFrameUpLeft, orient = VERTICAL)
		self.RenameScrollbarYUpfiles.pack( side = RIGHT, fill = Y )

		self.RenameTextUpFiles = Text(self.RenameFrameUpLeft, font = self.ft, 
								xscrollcommand = self.RenameScrollbarXUpfiles.set, yscrollcommand = self.RenameScrollbarYUpfiles.set, wrap = 'none')
		self.RenameTextUpFiles.pack(fill = BOTH)

		self.RenameTextUpFiles.drop_target_register(DND_FILES, DND_TEXT)
		self.RenameTextUpFiles.dnd_bind('<<Drop>>', self.drop_in_text)
		
		self.RenameScrollbarXUpfiles.config( command = self.RenameTextUpFiles.xview )
		self.RenameScrollbarYUpfiles.config( command = self.RenameTextUpFiles.yview )
		# end up left Frame
		
		# start down left Frame
		self.RenameFrameDownLeft = ttk.LabelFrame(self.RenameRoot, text = "Results")
		self.RenameFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.RenameScrollbarXDownfiles = ttk.Scrollbar(self.RenameFrameDownLeft, orient = HORIZONTAL)
		self.RenameScrollbarXDownfiles.pack( side = BOTTOM, fill = X )
		
		self.RenameScrollbarYDownfiles = ttk.Scrollbar(self.RenameFrameDownLeft, orient = VERTICAL)
		self.RenameScrollbarYDownfiles.pack( side = RIGHT, fill = Y )
		
		self.RenameTextDownFiles = Text(self.RenameFrameDownLeft, font = self.ft, 
								  xscrollcommand = self.RenameScrollbarXDownfiles.set, yscrollcommand = self.RenameScrollbarYDownfiles.set, wrap = 'none')
		self.RenameTextDownFiles.pack(fill = BOTH)
		
		self.RenameScrollbarXDownfiles.config( command = self.RenameTextDownFiles.xview )
		self.RenameScrollbarYDownfiles.config( command = self.RenameTextDownFiles.yview )
		# end down left Frame
		
		# start right frame
		self.RenameFrameRight = ttk.LabelFrame(self.RenameRoot, text = "")
		self.RenameFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)

		# start RenameFrameRight_00
		self.RenameFrameRight_00 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_00.pack(fill = X, side = TOP)

		self.RenameButtonReset = ttk.Button(self.RenameFrameRight_00, text = "          Reset         ", command = self.RenameReset) 
		self.RenameButtonReset.pack(fill = X, side = LEFT, expand = True)

		self.RenameButtonAddOneFolder = ttk.Button(self.RenameFrameRight_00, text = "Add One Folder", command = self.RenameAddOneFolder) 
		self.RenameButtonAddOneFolder.pack(fill = X, side = LEFT, expand = True)
		# end RenameFrameRight_00
						
		self.RenameCheckFileVar = IntVar() # StringVar()
		self.RenameCheckFile = ttk.Checkbutton(self.RenameFrameRight, text = "Including Files", \
											variable = self.RenameCheckFileVar, onvalue = 1, offvalue = 0) 
		self.RenameCheckFile.pack(fill = X, side = TOP)
		self.RenameCheckFileVar.set(1)

		# start RenameFrameRight_1
		self.RenameFrameRight_1 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_1.pack(fill = X, side = TOP)

		self.RenameCheckFolderVar = IntVar()
		self.RenameCheckFolder = ttk.Checkbutton(self.RenameFrameRight_1, text = "Including Folders          ", \
											variable = self.RenameCheckFolderVar, onvalue = 1, offvalue = 0) 
		self.RenameCheckFolder.pack(fill = X, side = LEFT)
		self.RenameCheckFolderVar.set(0)

		self.RenameCheckRecurVar = IntVar()
		self.RenameCheckRecur = ttk.Checkbutton(self.RenameFrameRight_1, text = "Recursively", \
											variable = self.RenameCheckRecurVar, onvalue = 1, offvalue = 0) 
		self.RenameCheckRecur.pack(fill = X, side = LEFT)
		self.RenameCheckRecurVar.set(0)
		# end RenameFrameRight_1

		# start RenameFrameRight_0
		self.RenameFrameRight_0 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_0.pack(fill = X, side = TOP)

		self.RenameButtonAddFiles = ttk.Button(self.RenameFrameRight_0, text = "     Add Files    ", command = self.RenameAddFiles) 
		self.RenameButtonAddFiles.pack(fill = X, side = LEFT, expand = True)

		self.RenameButtonAddDirection = ttk.Button(self.RenameFrameRight_0, text = "Add Direction", command = self.RenameAddDirection) 
		self.RenameButtonAddDirection.pack(fill = X, side = LEFT, expand = True)
		# end RenameFrameRight_0
		
		values = ('digit: 1', 'digit: 2', 'digit: 3', 'digit: 4', 'digit: 5', 'digit: 6', 'digit: 7', 'digit: 8', 'digit: 9', 'digit: 10', 'digit: 20', 'digit: 99', )

		self.RenameComboDigitVar = StringVar()
		self.RenameComboDigit = ttk.Combobox(self.RenameFrameRight, textvariable = self.RenameComboDigitVar)
		self.RenameComboDigit["values"] = values
		self.RenameComboDigit.current(0) 
		self.RenameComboDigit.pack(fill = X, side = TOP, pady = 2)

		values = ('outset: 0', 'outset: 1', 'outset: 2', 'outset: 10', 'outset: 11', 'outset: 100', 'outset: 101', )

		self.RenameComboOutsetVar = StringVar()
		self.RenameComboOutset = ttk.Combobox(self.RenameFrameRight, textvariable = self.RenameComboOutsetVar)
		self.RenameComboOutset["values"] = values
		self.RenameComboOutset.current(1) 
		self.RenameComboOutset.pack(fill = X, side = TOP, pady = 2)

		# start RenameFrameRight_7
		self.RenameFrameRight_7 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_7.pack(fill = X, side = TOP)

		values = ('inteval: 1', 'inteval: 2', 'inteval: 3', 'inteval: 5', 'inteval: 10', 'inteval: 20', 'inteval: 50', 'inteval: 100')

		self.RenameComboIntervalVar = StringVar()
		self.RenameComboInterval = ttk.Combobox(self.RenameFrameRight_7, textvariable = self.RenameComboIntervalVar)
		self.RenameComboInterval["values"] = values
		self.RenameComboInterval.current(0) 
		self.RenameComboInterval.pack(fill = X, side = LEFT)
		
		self.RenameButtonRenameByOrdinal = ttk.Button(self.RenameFrameRight_7, text = "Rename By Ordinal", command = self.RenameByOrdinal)
		self.RenameButtonRenameByOrdinal.pack(fill = X, side = LEFT, expand = True)
		# end RenameFrameRight_7
		
		self.RenameLableInsertString = ttk.Label(self.RenameFrameRight, text = "Insert: String", anchor = W)
		self.RenameLableInsertString.pack(side = TOP, fill = X)
		
		self.RenameEntryInsertString = ttk.Entry(self.RenameFrameRight, font = self.ft)
		self.RenameEntryInsertString.pack(side = TOP, fill = X)

		self.RenameLableInsertPosition = ttk.Label(self.RenameFrameRight, text = "Insert: Postion ( -1 = end )", anchor = W)
		self.RenameLableInsertPosition.pack(side = TOP, fill = X)
		
		self.RenameEntryInsertPosition = ttk.Entry(self.RenameFrameRight, font = self.ft)
		self.RenameEntryInsertPosition.pack(side = TOP, fill = X)

		# start RenameFrameRight_2
		self.RenameFrameRight_2 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_2.pack(fill = X, side = TOP)
		
		self.RenameButtonInsertString = ttk.Button(self.RenameFrameRight_2, text = "Insert String", command = self.InsertString)
		self.RenameButtonInsertString.pack(fill = X, side = LEFT, expand = True)
		
		self.RenameButtonInsertOrdinal = ttk.Button(self.RenameFrameRight_2, text = "Insert Ordinal", command = self.InsertOrdinal)
		self.RenameButtonInsertOrdinal.pack(fill = X, side = LEFT, expand = True)
		# end RenameFrameRight_2
		
		# start RenameFrameRight_3
		self.RenameFrameRight_3 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_3.pack(fill = X, side = TOP)

		self.RenameLableReplaceOriginal = ttk.Label(self.RenameFrameRight_3, text = "Replce: Original       ", anchor = W)
		self.RenameLableReplaceOriginal.pack(side = LEFT, fill = X, expand = True)

		self.RenameCheckDeleteOldVar = IntVar()
		self.RenameCheckDeleteOld = ttk.Checkbutton(self.RenameFrameRight_3, text = "delete old ordinal", \
											variable = self.RenameCheckDeleteOldVar, onvalue = 1, offvalue = 0) 
		self.RenameCheckDeleteOld.pack(fill = X, side = LEFT, expand = True)
		self.RenameCheckDeleteOldVar.set(0)
		# end RenameFrameRight_3
		
		self.RenameEntryReplaceOriginal = ttk.Entry(self.RenameFrameRight, font = self.ft, )
		self.RenameEntryReplaceOriginal.pack(side = TOP, fill = X)

		self.RenameEntryReplaceOriginal.bind("<FocusIn>", self.RenameEntryOriginalFocusIn)
		self.RenameEntryReplaceOriginal.bind("<FocusOut>", self.RenameEntryOriginalFocusOut)
		#self.RenameEntryReplaceOriginal.bind("<Return>", handle_enter)
		
		self.RenameLableReplaceSubstitute = ttk.Label(self.RenameFrameRight, text = "Replce: Substitute", anchor = W)
		self.RenameLableReplaceSubstitute.pack(side = TOP, fill = X)
		
		self.RenameEntryReplaceSubstitute = ttk.Entry(self.RenameFrameRight, font = self.ft)
		self.RenameEntryReplaceSubstitute.pack(side = TOP, fill = X)

		# start RenameFrameRight_6
		self.RenameFrameRight_6 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_6.pack(fill = X, side = TOP)

		values = ('match all', 'match first', 'match second', 'match third', 'match fourth', 'match fifth', 'match last')

		self.RenameComboMatchVar = StringVar()
		self.RenameComboMatch = ttk.Combobox(self.RenameFrameRight_6, textvariable = self.RenameComboMatchVar)
		self.RenameComboMatch["values"] = values
		self.RenameComboMatch.current(0) 
		self.RenameComboMatch.pack(fill = X, side = LEFT)
		
		self.RenameButtonInsertEnd = ttk.Button(self.RenameFrameRight_6, text = "Replace", command = self.Replace)
		self.RenameButtonInsertEnd.pack(fill = X, side = LEFT, expand = True)
		# end RenameFrameRight_6

		

		# start RenameFrameRight_10
		self.RenameFrameRight_10 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_10.pack(fill = X, side = TOP)

		values = ('Left Position: 0', 'Left Position: 1', 'Left Position: 2', 'Left Position: 3', 'Left Position: -2', 'Left Position: -3' )

		self.RenameComboP1Var = StringVar()
		self.RenameComboP1 = ttk.Combobox(self.RenameFrameRight_10, textvariable = self.RenameComboP1Var)
		self.RenameComboP1["values"] = values
		self.RenameComboP1.current(0) 
		self.RenameComboP1.pack(side = LEFT, pady = 2)

		self.RenameLableP1 = ttk.Label(self.RenameFrameRight_10, text = "Filename Left Position", anchor = W)
		self.RenameLableP1.pack(fill = X, side = LEFT)

		# start RenameFrameRight_11
		self.RenameFrameRight_11 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_11.pack(fill = X, side = TOP)

		values = ('Right Position: -1', 'Right Position: -2', 'Right Position: -3', 'Right Position: 5', 'Right Position: 10')

		self.RenameComboP2Var = StringVar()
		self.RenameComboP2 = ttk.Combobox(self.RenameFrameRight_11, textvariable = self.RenameComboP2Var)
		self.RenameComboP2["values"] = values
		self.RenameComboP2.current(0) 
		self.RenameComboP2.pack(fill = X, side = LEFT, pady = 2)

		self.RenameLableP2 = ttk.Label(self.RenameFrameRight_11, text = "Filename Right Position", anchor = W)
		self.RenameLableP2.pack(fill = X, side = LEFT)
		# end RenameFrameRight_10

		# start RenameFrameRight_4
		self.RenameFrameRight_4 = ttk.Frame(self.RenameFrameRight)
		self.RenameFrameRight_4.pack(fill = X, side = TOP)

		self.RenameButtonGetMiddle = ttk.Button(self.RenameFrameRight_4, text = "   Get Middle  ", command = self.GetMiddle)
		self.RenameButtonGetMiddle.pack(fill = X, side = LEFT, expand = True)

		self.RenameButtonDeleteMiddle = ttk.Button(self.RenameFrameRight_4, text = "Delete Middle", command = self.DeleteMiddle)
		self.RenameButtonDeleteMiddle.pack(fill = X, side = LEFT, expand = True)
		# end RenameFrameRight_4

		self.RenameButtonRevoke = ttk.Button(self.RenameFrameRight, text = "Revoke", command = self.Revoke)
		self.RenameButtonRevoke.pack(fill = X, side = BOTTOM)

		self.RenameButtonRename = ttk.Button(self.RenameFrameRight, text = "Rename", command = self.Rename)
		self.RenameButtonRename.pack(fill = X, side = BOTTOM, pady = 12)
		# end right frame





		
		'''
			def drop_enter(self, event):
		event.widget.focus_force()
		print('Entering widget: %s' % event.widget)
		return event.action

	def drop_position(self, event):
	    print('Position: x %d, y %d' %(event.x_root, event.y_root))
	    return event.action
	
	def drop_leave(self, event):
	    print('Leaving %s' % event.widget)
	    return event.action
	
	def drop(self, event):
		if event.data:
			print('Dropped data:\n', event.data)
			if event.widget == self.RenameTextUpFiles:
				files = self.RenameTextUpFiles.tk.splitlist(event.data)
				for f in files:
					if os.path.exists(f):
						print('Dropped file: "%s"' % f)
						self.RenameTextUpFiles.insert(INSERT, f)
						self.RenameTextUpFiles.insert(INSERT, '\n')
					else:
						print('Not dropping file "%s": file does not exist.' % f)
			else:
				print('Error: reported event.widget not known')
		return event.action



	
	def drag_init_text(self, event):
		print_event_info(event)
		data = ()
		if self.RenameTextUpFiles.curselection():
			data = tuple([self.RenameTextUpFiles.get(i) for i in self.RenameTextUpFiles.curselection()])
			print('Dragging :\n', data)
		return ((ASK, COPY), (DND_FILES, DND_TEXT), data)
	
	def drag_end(self, event):
	    print('Drag ended for widget:', event.widget)



	self.RenameTextUpFiles = Text(self.RenameFrameUpLeft, font = self.ft, 
								xscrollcommand = self.RenameScrollbarXUpfiles.set, yscrollcommand = self.RenameScrollbarYUpfiles.set, wrap = 'none')
	self.RenameTextUpFiles.pack(fill = BOTH)

	self.RenameTextUpFiles.drop_target_register(DND_FILES, DND_TEXT)
	self.RenameTextUpFiles.dnd_bind('<<DropEnter>>', self.drop_enter)
	self.RenameTextUpFiles.dnd_bind('<<DropPosition>>', self.drop_position)
	self.RenameTextUpFiles.dnd_bind('<<DropLeave>>', self.drop_leave)
	self.RenameTextUpFiles.dnd_bind('<<Drop>>', self.drop)

	self.RenameTextUpFiles.drag_source_register(1, DND_TEXT, DND_FILES)

	self.RenameTextUpFiles.dnd_bind('<<DragInitCmd>>', self.drag_init_text)
	self.RenameTextUpFiles.dnd_bind('<<DragEndCmd>>', self.drag_end)

	'''