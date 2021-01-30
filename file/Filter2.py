#coding=utf-8
#File_tools/file/Filter22.py

import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog 
import os
import sys
import json
import copy
import subprocess
import time

import tkinterdnd2 
from tkinterdnd2 import *



class CreateFrameFilter2():

	def __init__(self):
		super().__init__()

		self.Filter2Root = None
		self.Filter2Source = ''
		


	def Filter2Default(self):

		self.Filter2DefaultLog()
		self.CreateWidgetsFrameFilter2()
		self.Filter2RestoreState()



	def Filter2DefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'filter2' in j['file_tools']['file']:
			j['file_tools']['file']['filter2'] = {}
		if not 'source_filter2' in j['file_tools']['file']['filter2']:
			j['file_tools']['file']['filter2']['source_filter2'] = ''
		if not 'destination_filter2' in j['file_tools']['file']['filter2']:
			j['file_tools']['file']['filter2']['destination_filter2'] = ''
		if not 'check_name' in j['file_tools']['file']['filter2']:
			j['file_tools']['file']['filter2']['check_name'] = 1
		if not 'check_size' in j['file_tools']['file']['filter2']:
			j['file_tools']['file']['filter2']['check_size'] = 1
		if not 'check_case' in j['file_tools']['file']['filter2']:
			j['file_tools']['file']['filter2']['check_case'] = 0
		if not 'check_reverse' in j['file_tools']['file']['filter2']:
			j['file_tools']['file']['filter2']['check_reverse'] = 0
		if not 'check_filter1' in j['file_tools']['file']['filter2']:
			j['file_tools']['file']['filter2']['check_filter1'] = 0
		if not 'check_checksum' in j['file_tools']['file']['filter2']:
			j['file_tools']['file']['filter2']['check_checksum'] = 0
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def Filter2RestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.Filter2Source = j['file_tools']['file']['filter2']['source_filter2']
		self.Filter2EntrySource.insert(0, self.Filter2Source)
		self.Filter2Destination = j['file_tools']['file']['filter2']['destination_filter2']
		self.Filter2EntryDestination.insert(0, self.Filter2Destination)
		self.Filter2CheckNameVar.set( j['file_tools']['file']['filter2']['check_name'])
		self.Filter2CheckSizeVar.set( j['file_tools']['file']['filter2']['check_size'])
		self.Filter2CheckCaseVar.set( j['file_tools']['file']['filter2']['check_case'])
		self.Filter2CheckReverseVar.set( j['file_tools']['file']['filter2']['check_reverse'])
		self.Filter2CheckFilter1Var.set( j['file_tools']['file']['filter2']['check_filter1'])
		self.Filter2CheckChecksumVar.set( j['file_tools']['file']['filter2']['check_checksum'])
		f.close()

	

	def ReadFilter2Path(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.Filter2Source = self.Filter2EntrySource.get()
		self.Filter2Source = j['file_tools']['file']['filter2']['source_filter2']
		self.Filter2Destination = self.Filter2EntryDestination.get()
		self.Filter2Destination = j['file_tools']['file']['filter2']['destination_filter2']
		f.close()
	

	def Filter2SaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['file']['filter2']['source_filter2'] = self.Filter2EntrySource.get()
			j['file_tools']['file']['filter2']['destination_filter2'] = self.Filter2EntryDestination.get()
			j['file_tools']['file']['filter2']['check_name'] = self.Filter2CheckNameVar.get()
			j['file_tools']['file']['filter2']['check_size'] = self.Filter2CheckSizeVar.get()
			j['file_tools']['file']['filter2']['check_case'] = self.Filter2CheckCaseVar.get()
			j['file_tools']['file']['filter2']['check_reverse'] = self.Filter2CheckReverseVar.get()
			j['file_tools']['file']['filter2']['check_filter1'] = self.Filter2CheckFilter1Var.get()
			j['file_tools']['file']['filter2']['check_checksum'] = self.Filter2CheckChecksumVar.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def Filter2Reset(self):
		self.Filter2EntrySource.delete(0, "end")
		self.Filter2EntryDestination.delete(0, "end")
		self.Filter2TextDownFiles.delete("1.0", "end")
		self.Filter2SaveEntry()


	def Filter2CheckRepeat(self):
		files = self.Filter2TextDownFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.Filter2TextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		files = set(files)
		files = sorted(files, key=self.natsort_key2)
		for file in files:
			if file == '\n' or file == '':
				continue
			self.Filter2TextDownFiles.insert(INSERT, file)
			self.Filter2TextDownFiles.insert(INSERT, '\n')
	

	def Filter2AddSource(self):
		self.ReadFilter2Path()
		p = self.Filter2Source
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.Filter2TextDownFiles.delete("1.0", "end")
			self.Filter2EntrySource.delete(0, "end")
			self.Filter2EntrySource.insert(0, dir)
			self.Filter2Source = dir
			self.Filter2SaveEntry()
		except:pass

	def Filter2AddDestination(self):
		self.ReadFilter2Path()
		p = self.Filter2Destination
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.Filter2TextDownFiles.delete("1.0", "end")
			self.Filter2EntryDestination.delete(0, "end")
			self.Filter2EntryDestination.insert(0, dir)
			self.Filter2Destination = dir
			self.Filter2SaveEntry()
		except:pass


	def Filter2(self):
		self.ReadFilter2Path()
		src = self.Filter2Source
		dst = self.Filter2Destination
		if self.bl.compare_dir(src, dst) == 1:
			is_same_dir = 1
		else:
			is_same_dir = 0
		self.Filter2SaveEntry()
		self.Filter2TextDownFiles.delete("1.0", "end")
		dir = self.Filter2Source
		if self.fl.check_banned_path(dir) == -1:
			return
		check_name = self.Filter2CheckNameVar.get()
		check_size = self.Filter2CheckSizeVar.get()
		case = self.Filter2CheckCaseVar.get()
		is_reverse = self.Filter2CheckReverseVar.get()
		is_filter1 = self.Filter2CheckFilter1Var.get()

		if is_same_dir == 0:
			files = self.fl.filter2(src = src, dst = dst, check_name = check_name, check_size = check_size, case_insensitive = case, 
																		is_reverse = is_reverse, is_filter1 = is_filter1)
		if is_same_dir == 1:
			checksum = self.Filter2CheckChecksumVar.get()
			if checksum == 1:
				self.Filter2TextDownFiles.insert(INSERT, "Calculating Checksum, please wait......")
				self.root.update()
			files = self.fl.filter2_same_dir(src = src, check_name = check_name, check_size = check_size, 
															case_insensitive = case, checksum = checksum)
			self.Filter2TextDownFiles.delete("1.0", "end")
			n = 0
			for file in files:
				self.Filter2TextDownFiles.insert(INSERT, file)
				self.Filter2TextDownFiles.insert(INSERT, '\n')
				if file[0] == '-': n = n + 1
			self.Filter2FrameDownLeft.config(text = 'Filtered    ' + str(n) + ' pairs')
			if checksum == 1:
				self.Filter2FrameDownLeft.config(text = 'Filtered    ' + str(n) + ' pairs' + ' ( Checksum Calculated )')
			if len(self.Filter2TextDownFiles.get("1.0", "end") ) < 4:
				self.Filter2TextDownFiles.insert(INSERT, "Nothing detected")
				self.Filter2TextDownFiles.insert(INSERT, '\n')
			return


		if is_filter1 == 1:
			self.Filter(is_from_outside = 1, outside_path = files)
			self.Filter2TextDownFiles.insert(INSERT, 
				    self.FilterTextDownFiles.get("1.0", "end") )
			return

		n = 0
		for file in files:
			self.Filter2TextDownFiles.insert(INSERT, file)
			self.Filter2TextDownFiles.insert(INSERT, '\n')
			n = n + 1
		self.Filter2FrameDownLeft.config(text = 'Filtered  ' + str(n) )
		if len(self.Filter2TextDownFiles.get("1.0", "end") ) < 4:
			self.Filter2TextDownFiles.insert(INSERT, "Nothing detected")
			self.Filter2TextDownFiles.insert(INSERT, '\n')

		

	def OpenAll(self):
		self.Filter2SaveEntry()
		tmp = messagebox.askquestion("Excute OPEN ALL !", "THIS IS EXTREMELY DANGERS !\n\nYet, still want to open them all?")
		if tmp == 'no':
			return
		files = self.Filter2TextDownFiles.get("1.0", "end")
		files = files.split('\n')
		files = self.bl.clean_list(files)
		for file in files:
			os.startfile(file)
			#self.root.after(5000, [fun]) or self.Filter2TextDownFiles.after(1000)
				


	def CreateWidgetsFrameFilter2(self):

		# start up left Frame
		self.Filter2FrameUpLeft = ttk.LabelFrame(self.Filter2Root, text = "")
		self.Filter2FrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)

		## start up left Frame_01
		self.Filter2FrameUpLeft_01 = ttk.Frame(self.Filter2FrameUpLeft)
		self.Filter2FrameUpLeft_01.pack(side = TOP, fill = X)

		self.Filter2LabelSource = ttk.Label(self.Filter2FrameUpLeft_01, text = "Source", anchor = W)
		self.Filter2LabelSource.pack(side = TOP, fill = X)
		
		self.Filter2ScrollbarXSource = ttk.Scrollbar(self.Filter2FrameUpLeft_01, orient = HORIZONTAL)
		self.Filter2ScrollbarXSource.pack( side = BOTTOM, fill = X )
		
		self.Filter2EntrySource = ttk.Entry(self.Filter2FrameUpLeft_01, font = self.ft, xscrollcommand = self.Filter2ScrollbarXSource.set)
		self.Filter2EntrySource.pack(fill = X)

		self.Filter2EntrySource.drop_target_register(DND_FILES, DND_TEXT)
		self.Filter2EntrySource.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.Filter2ScrollbarXSource.config( command = self.Filter2EntrySource.xview )
		## end up left Frame_01


		## start up left Frame_02
		self.Filter2FrameUpLeft_02 = ttk.Frame(self.Filter2FrameUpLeft)
		self.Filter2FrameUpLeft_02.pack(side = TOP, fill = X)

		self.Filter2LabelDestination = ttk.Label(self.Filter2FrameUpLeft_02, text = "Destination", anchor = W)
		self.Filter2LabelDestination.pack(side = TOP, fill = X)
		
		self.Filter2ScrollbarXDestination = ttk.Scrollbar(self.Filter2FrameUpLeft_02, orient = HORIZONTAL)
		self.Filter2ScrollbarXDestination.pack( side = BOTTOM, fill = X )
		
		self.Filter2EntryDestination = ttk.Entry(self.Filter2FrameUpLeft_02, font = self.ft, xscrollcommand = self.Filter2ScrollbarXDestination.set)
		self.Filter2EntryDestination.pack(fill = X)

		self.Filter2EntryDestination.drop_target_register(DND_FILES, DND_TEXT)
		self.Filter2EntryDestination.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.Filter2ScrollbarXDestination.config( command = self.Filter2EntryDestination.xview )
		## end up left Frame_02


		self.Filter2LabelDescription = ttk.Label(self.Filter2FrameUpLeft, text = 'Description:\n\n\
1. Walk through the Source and Destination direction recursively\n\n\
2. Collecting all the file name or size, compare every file in Source to Destination \n\
    If same, shows in below\n\n\
3. If set Source and Destination same, it will filter out the same file in the direction \n\
    ( "Does not exist (reverse result)" and "After Filter2 done, do Filter1"  DO NOT WORK IN  "3" ) \n\
			', anchor = W)
		self.Filter2LabelDescription.pack(side = TOP, fill = X)
		# end up left Frame
		

		# start down left Frame
		self.Filter2FrameDownLeft = ttk.LabelFrame(self.Filter2Root, text = r'Filtered')
		self.Filter2FrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.Filter2ScrollbarXDownFolders = ttk.Scrollbar(self.Filter2FrameDownLeft, orient = HORIZONTAL)
		self.Filter2ScrollbarXDownFolders.pack( side = BOTTOM, fill = X )
		
		self.Filter2ScrollbarYDownFolders = ttk.Scrollbar(self.Filter2FrameDownLeft, orient = VERTICAL)
		self.Filter2ScrollbarYDownFolders.pack( side = RIGHT, fill = Y )
		
		self.Filter2TextDownFiles = Text(self.Filter2FrameDownLeft, font = self.ft, \
xscrollcommand = self.Filter2ScrollbarXDownFolders.set, yscrollcommand = self.Filter2ScrollbarYDownFolders.set, wrap = 'none')
		self.Filter2TextDownFiles.pack(fill = BOTH)
		
		self.Filter2ScrollbarXDownFolders.config( command = self.Filter2TextDownFiles.xview )
		self.Filter2ScrollbarYDownFolders.config( command = self.Filter2TextDownFiles.yview )
		# end down left Frame
		
		# start right frame
		self.Filter2FrameRight = ttk.LabelFrame(self.Filter2Root, text = "")
		self.Filter2FrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.Filter2ButtonReset = ttk.Button(self.Filter2FrameRight, text = "Reset", command = self.Filter2Reset) 
		self.Filter2ButtonReset.pack(fill = X, side = TOP)
		
		self.Filter2ButtonAddSource = ttk.Button(self.Filter2FrameRight, text = "Add Source", command = self.Filter2AddSource) 
		self.Filter2ButtonAddSource.pack(fill = X, side = TOP)

		self.Filter2ButtonAddDestination = ttk.Button(self.Filter2FrameRight, text = "Add Destination", command = self.Filter2AddDestination) 
		self.Filter2ButtonAddDestination.pack(fill = X, side = TOP)
						

		self.Filter2LabelBlank = ttk.Label(self.Filter2FrameRight)
		self.Filter2LabelBlank.pack(side = TOP, fill = X)


		self.Filter2CheckNameVar = IntVar()
		self.Filter2CheckName = ttk.Checkbutton(self.Filter2FrameRight, text = "Same Name", \
											variable = self.Filter2CheckNameVar, onvalue = 1, offvalue = 0) 
		self.Filter2CheckName.pack(fill = X, side = TOP)
		self.Filter2CheckNameVar.set(0)

		self.Filter2CheckSizeVar = IntVar()
		self.Filter2CheckSize = ttk.Checkbutton(self.Filter2FrameRight, text = "Same Size", \
											variable = self.Filter2CheckSizeVar, onvalue = 1, offvalue = 0) 
		self.Filter2CheckSize.pack(fill = X, side = TOP)
		self.Filter2CheckSizeVar.set(1)

		self.Filter2CheckCaseVar = IntVar()
		self.Filter2CheckCase = ttk.Checkbutton(self.Filter2FrameRight, text = "Case Insensitive", \
											variable = self.Filter2CheckCaseVar, onvalue = 1, offvalue = 0) 
		self.Filter2CheckCase.pack(fill = X, side = TOP)
		self.Filter2CheckCaseVar.set(0)

		self.Filter2ButtonFilter2 = ttk.Button(self.Filter2FrameRight, text = "Filter2", command = self.Filter2) #bg = "#e1e1e1"
		self.Filter2ButtonFilter2.pack(side = TOP, fill = X)

		self.Filter2CheckReverseVar = IntVar()
		self.Filter2CheckReverse = ttk.Checkbutton(self.Filter2FrameRight, text = "Does not exist (reverse result)", \
											variable = self.Filter2CheckReverseVar, onvalue = 1, offvalue = 0) 
		self.Filter2CheckReverse.pack(fill = X, side = TOP)
		self.Filter2CheckReverseVar.set(0)

		self.Filter2CheckFilter1Var = IntVar()
		self.Filter2CheckFilter1 = ttk.Checkbutton(self.Filter2FrameRight, text = 'After "Filter2" done, do "Filter1"', \
											variable = self.Filter2CheckFilter1Var, onvalue = 1, offvalue = 0) 
		self.Filter2CheckFilter1.pack(fill = X, side = TOP)
		self.Filter2CheckFilter1Var.set(0)


		self.Filter2LabelBlank = ttk.Label(self.Filter2FrameRight)
		self.Filter2LabelBlank.pack(side = TOP, fill = X)


		self.Filter2CheckChecksumVar = IntVar()
		self.Filter2CheckChecksum = ttk.Checkbutton(self.Filter2FrameRight, text = 'Do Checksum in "Description 3" (slow)', \
											variable = self.Filter2CheckChecksumVar, onvalue = 1, offvalue = 0) 
		self.Filter2CheckChecksum.pack(fill = X, side = TOP)
		self.Filter2CheckChecksumVar.set(0)


		self.Filter2ButtonOpen = ttk.Button(self.Filter2FrameRight, text = "OPEN ALL", command = self.OpenAll) #bg = "#e1e1e1"
		self.Filter2ButtonOpen.pack(side = BOTTOM, fill = X)

		self.Filter2LabelBlank = ttk.Label(self.Filter2FrameRight, text = 'EXTREMELY DANGERS !')
		self.Filter2LabelBlank.pack(side = BOTTOM, fill = X)
		
		# end right frame