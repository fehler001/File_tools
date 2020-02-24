#coding=utf-8
#File_tools/file/Date.py

import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog 
import os
import sys
import json
import copy
import time
import stat

import tkinterdnd2 
from tkinterdnd2 import *



class CreateFrameDate():

	def __init__(self):
		super().__init__()

		self.DateRoot = None
		
		self.DateOutset = '2020.01.01.0.0.0'
		self.DateOutput = '%Y-%m-%d_%H.%M.%S'
		self.DateInterval = 1
		self.DateUnit = 'second'
		self.DatePosition = 0
		self.DateOriginat = {}
		self.DateOriginmt = {}
		self.DateFiles = {}
		self.NDateTimes = 0


	def DateDefault(self):

		self.DateDefaultLog()
		self.CreateWidgetsFrameDate()
		self.DateRestoreState()



	def DateDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'date' in j['file_tools']['file']:
			j['file_tools']['file']['date'] = {}
		if not 'check_create' in j['file_tools']['file']['date']:
			j['file_tools']['file']['date']['check_create'] = 0
		if not 'check_modify' in j['file_tools']['file']['date']:
			j['file_tools']['file']['date']['check_modify'] = 0
		if not 'check_access' in j['file_tools']['file']['date']:
			j['file_tools']['file']['date']['check_access'] = 0
		if not 'position' in j['file_tools']['file']['date']:
			j['file_tools']['file']['date']['position'] = ''
		if not 'outset' in j['file_tools']['file']['date']:
			j['file_tools']['file']['date']['outset'] = ''
		if not 'output' in j['file_tools']['file']['date']:
			j['file_tools']['file']['date']['output'] = ''
		if not 'unit' in j['file_tools']['file']['date']:
			j['file_tools']['file']['date']['unit'] = 'day'
		if not 'interval' in j['file_tools']['file']['date']:
			j['file_tools']['file']['date']['interval'] = ''
		if not 'check_increment' in j['file_tools']['file']['date']:
			j['file_tools']['file']['date']['check_increment'] = 0

		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def DateRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.DateCheckCreateVar.set( j['file_tools']['file']['date']['check_create'])
		self.DateCheckModifyVar.set( j['file_tools']['file']['date']['check_modify'])
		self.DateCheckAccessVar.set( j['file_tools']['file']['date']['check_access'])
		self.DateEntryInsertPosition.insert(0, j['file_tools']['file']['date']['position'])
		self.DateEntryOutset.insert(0, j['file_tools']['file']['date']['outset'])
		self.DateEntryOutput.insert(0, j['file_tools']['file']['date']['output'])
		self.DateComboUnitVar.set( j['file_tools']['file']['date']['unit'])
		self.DateEntryInterval.insert(0, j['file_tools']['file']['date']['interval'])
		self.DateCheckIncrementVar.set( j['file_tools']['file']['date']['check_increment'])
		f.close()

		


	def DateSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['file']['date']['check_create'] = self.DateCheckCreateVar.get()
			j['file_tools']['file']['date']['check_modify'] = self.DateCheckModifyVar.get()
			j['file_tools']['file']['date']['check_access'] = self.DateCheckAccessVar.get()
			j['file_tools']['file']['date']['position'] = self.DateEntryInsertPosition.get()
			j['file_tools']['file']['date']['outset'] = self.DateEntryOutset.get()
			j['file_tools']['file']['date']['output'] = self.DateEntryOutput.get()
			j['file_tools']['file']['date']['unit'] = self.DateComboUnitVar.get()
			j['file_tools']['file']['date']['interval'] = self.DateEntryInterval.get()
			j['file_tools']['file']['date']['check_increment'] = self.DateCheckIncrementVar.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def DateReset(self):
		self.DateTextUpFiles.delete("1.0", "end")
		self.DateTextDownFiles.delete("1.0", "end")
		self.DateSaveEntry()
	

	

	def DateEliminateNullDown(self):
		files = self.DateTextDownFiles.get("1.0", "end")  
		self.DateTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		files = self.bl.clean_list(files)
		for file in files:
			self.DateTextDownFiles.insert(INSERT, file)
			self.DateTextDownFiles.insert(INSERT, '\n')
	


	def DateReadRename(self):
		files = self.RenameTextUpFiles.get("1.0", "end")
		files = files.split('\n')
		files = self.bl.clean_list(files)
		for file in files:
			self.DateTextUpFiles.insert(INSERT, file)
			self.DateTextUpFiles.insert(INSERT, '\n')
		self.DateTextDownFiles.delete("1.0", "end")
		self.DateSaveEntry()


	def DateWriteRename(self):
		self.DateSaveEntry()
		self.RenameTextDownFiles.delete("1.0", "end")
		files = self.DateTextDownFiles.get("1.0", "end")
		files = files.split('\n')
		files = self.bl.clean_list(files)
		for file in files:
			self.RenameTextDownFiles.insert(INSERT, file)
			self.RenameTextDownFiles.insert(INSERT, '\n')
		self.RenameSaveEntry()


			


	def DateInitializeEntry(self):
		if self.DateEntryOutset.get() == '':
			self.DateEntryOutset.insert(0, '2020.01.01.0.0.0')
		outset = self.DateEntryOutset.get()
		try:
		   t2 = time.strptime(outset, self.bl.date_format)
		except:
			messagebox.showerror ("DATE ERROR", '"Start From Date:" got error !')
			return -1
		self.DateOutset = outset

		if self.DateEntryOutput.get() == '':
			self.DateEntryOutput.insert(0, '%Y-%m-%d_%H.%M.%S')
		output = self.DateEntryOutput.get()
		try:
		   t3 = time.strftime(output, t2)
		except:
			messagebox.showerror ("DATE ERROR", '"Output Format:" Wrong Format !')
			return -1
		self.DateOutput = output

		if self.DateEntryInterval.get() == '':
			self.DateEntryInterval.insert(0, 1)
		interval = self.DateEntryInterval.get()
		if self.bl.check_legit_int(interval) == -1:
			return -1
		self.DateInterval = int(interval)

		self.DateUnit = self.DateComboUnit.get()

		if self.DateEntryInsertPosition.get() == '':
			self.DateEntryInsertPosition.insert(0, 0)
		pos = self.DateEntryInsertPosition.get()
		if self.bl.check_legit_int(pos) == -1:
			return -1
		self.DatePosition = int(pos)



	def InsertSelfDate(self):
		self.DateSaveEntry()
		if self.DateInitializeEntry() == -1:
			return
		files = self.DateTextUpFiles.get("1.0", "end") 
		files = files.split('\n')
		files = self.bl.clean_list(files)

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(files) == -1:
				return

		ordinal = []
		n = 0
		for file in files:
			dinfo = self.bl.get_path_date(file)
			ordinal.append('')
			if self.DateCheckCreateVar.get() == 1:
				t2 = time.localtime(dinfo['ctime'])
				t3 = time.strftime(self.DateOutput, t2)
				ordinal[n] = ordinal[n] + t3
			if self.DateCheckModifyVar.get() == 1:
				t2 = time.localtime(dinfo['mtime'])
				t3 = time.strftime(self.DateOutput, t2)
				ordinal[n] = ordinal[n] + t3
			if self.DateCheckAccessVar.get() == 1:
				t2 = time.localtime(dinfo['atime'])
				t3 = time.strftime(self.DateOutput, t2)
				ordinal[n] = ordinal[n] + t3
			n = n + 1

		rst = self.fl.insert(files, pos = self.DatePosition, cont = '', ordinal = ordinal)
		self.DateTextDownFiles.delete("1.0", "end")
		for file in rst:
			self.DateTextDownFiles.insert(INSERT, file)
			self.DateTextDownFiles.insert(INSERT, '\n')
		self.DateEliminateNullDown()




	def InsertDateIncrement(self):
		self.DateSaveEntry()
		if self.DateInitializeEntry() == -1:
			return
		files = self.DateTextUpFiles.get("1.0", "end") 
		files = files.split('\n')
		files = self.bl.clean_list(files)

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(files) == -1:
				return

		unit = self.DateComboUnit.get()
		ordinal = self.bl.generate_date_ordinal( length = len(files), outset = self.DateOutset, output_format = self.DateOutput, 
			interval = self.DateInterval, unit = unit, is_str = 1, is_mktime = 0)
		if ordinal == -1:
			return
		rst = self.fl.insert(files, pos = self.DatePosition, cont = '', ordinal = ordinal)
		self.DateTextDownFiles.delete("1.0", "end")
		for file in rst:
			self.DateTextDownFiles.insert(INSERT, file)
			self.DateTextDownFiles.insert(INSERT, '\n')
		self.DateEliminateNullDown()
	


	def DateModifyPreview(self):
		self.DateSaveEntry()
		if self.DateInitializeEntry() == -1:
			return
		files = self.DateTextUpFiles.get("1.0", "end") 
		files = files.split('\n')
		files = self.bl.clean_list(files)

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(files) == -1:
				return
		
		is_increment = self.DateCheckIncrementVar.get()
		unit = self.DateComboUnit.get()

		if is_increment == 1:
			ordinal = self.bl.generate_date_ordinal( len(files), outset = self.DateOutset, output_format = self.DateOutput, 
				interval = self.DateInterval, unit = self.DateUnit, is_str = 1, is_mktime = 0)
			if ordinal == -1:
				return
		else:
			ordinal = []
			t1 = time.mktime( time.strptime(self.DateOutset, self.bl.date_format) )
			t2 = time.localtime(t1)
			t3 = time.strftime(self.DateOutput, t2)
			for i in range(len(files)):
				ordinal.append(t3)

		if self.bl.check_date_range(ordinal, format = self.DateOutput) == -1:
			return

		self.DateTextDownFiles.delete("1.0", "end")
		n = 0
		for file in files:
			self.DateTextDownFiles.insert(INSERT, " ' date -> " +ordinal[n] + " '   " + file)
			self.DateTextDownFiles.insert(INSERT, '\n')
			n = n + 1
		self.DateEliminateNullDown()





	def DateModify(self, SwitchRevoke = False):
		self.DateSaveEntry()
		if self.DateInitializeEntry() == -1:
			return

		raw_files = self.DateTextUpFiles.get("1.0", "end") 
		if len(raw_files) < 4:
			messagebox.showerror ("Warrning", "_____EMPTY BOX_____")
			return
		files = raw_files.split('\n')
		files = self.bl.clean_list(files)

		if self.CheckPathExist == 1:
			if self.bl.check_path_exist(files) == -1:
				return

		is_at = self.DateCheckAccessVar.get()
		is_mt = self.DateCheckModifyVar.get()
		if is_at == 0 and is_mt == 0:
			messagebox.showerror ("Warrning", 'Please check at least one ("Modified" or "Accessed")')
			return
		is_increment = self.DateCheckIncrementVar.get()
		unit = self.DateComboUnit.get()

		if is_increment == 1:
			ordinal = self.bl.generate_date_ordinal( len(files), outset = self.DateOutset, 
				interval = self.DateInterval, unit = self.DateUnit, is_str = 0, is_mktime = 1)
			if ordinal == -1:
				return
		else:
			ordinal = []
			t = time.mktime( time.strptime(self.DateOutset, self.bl.date_format) )
			for i in range(len(files)):
				ordinal.append(t)

		if self.bl.check_date_range(ordinal) == -1:
			return

		if SwitchRevoke is False:
			tmp = messagebox.askquestion("Excute Date Modify", "Are you sure ?")
			if tmp == 'no':
				return
		for i in range(len(files)):
			#try:
			if 1:
				dinfo = self.bl.get_path_date(files[i])
				self.DateOriginat[str(self.NDateTimes) + '-' + str(i)] = dinfo['atime']
				self.DateOriginmt[str(self.NDateTimes) + '-' + str(i)] = dinfo['mtime']
				if is_at == 1:
					at = ordinal[i]
				else:
					at = dinfo['atime']
				if is_mt == 1:
					mt = ordinal[i]
				else:
					mt = dinfo['mtime']
				#os.chmod(files[i], stat.S_IRWXU)
				os.utime(files[i], (at, mt))    # (accessed time, modified time)
			#except:
				#pass
		self.DateFiles[self.NDateTimes] = files
		self.NDateTimes = self.NDateTimes + 1

		self.DateTextDownFiles.delete("1.0", "end")
		self.DateTextDownFiles.insert(INSERT, 'Modify Complete')
		

	

	def DateUndoModify(self):
		if self.NDateTimes == 0:
			messagebox.showerror ("ERROR", "There is no back anymore!")
			return
		tmp = messagebox.askquestion("Excute Undo", "Are you really sure?")
		if tmp == 'no':
			return

		self.NDateTimes = self.NDateTimes - 1
		files = self.DateFiles[self.NDateTimes]
		for i in range(len(files)):
			#try:
			if 1:
				at = self.DateOriginat[str(self.NDateTimes) + '-' + str(i)]
				mt = self.DateOriginmt[str(self.NDateTimes) + '-' + str(i)]
				del self.DateOriginat[str(self.NDateTimes) + '-' + str(i)]
				del self.DateOriginmt[str(self.NDateTimes) + '-' + str(i)]
				os.utime(files[i], (at, mt))    # (accessed time, modified time)
			#except:
			#	pass
		del self.DateFiles[self.NDateTimes]
		self.DateTextDownFiles.delete("1.0", "end")
		self.DateTextDownFiles.insert(INSERT, 'Undo Complete')




	def CreateWidgetsFrameDate(self):

		# start up left Frame		
		self.DateFrameUpLeft = ttk.LabelFrame(self.DateRoot, text = "Files")
		self.DateFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)
		
		self.DateScrollbarXUpfiles = ttk.Scrollbar(self.DateFrameUpLeft, orient = HORIZONTAL)
		self.DateScrollbarXUpfiles.pack( side = BOTTOM, fill = X )
		
		self.DateScrollbarYUpfiles = ttk.Scrollbar(self.DateFrameUpLeft, orient = VERTICAL)
		self.DateScrollbarYUpfiles.pack( side = RIGHT, fill = Y )

		self.DateTextUpFiles = Text(self.DateFrameUpLeft, font = self.ft, 
								xscrollcommand = self.DateScrollbarXUpfiles.set, yscrollcommand = self.DateScrollbarYUpfiles.set, wrap = 'none')
		self.DateTextUpFiles.pack(fill = BOTH)
		
		self.DateScrollbarXUpfiles.config( command = self.DateTextUpFiles.xview )
		self.DateScrollbarYUpfiles.config( command = self.DateTextUpFiles.yview )
		# end up left Frame
		
		# start down left Frame
		self.DateFrameDownLeft = ttk.LabelFrame(self.DateRoot, text = "Results")
		self.DateFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.DateScrollbarXDownfiles = ttk.Scrollbar(self.DateFrameDownLeft, orient = HORIZONTAL)
		self.DateScrollbarXDownfiles.pack( side = BOTTOM, fill = X )
		
		self.DateScrollbarYDownfiles = ttk.Scrollbar(self.DateFrameDownLeft, orient = VERTICAL)
		self.DateScrollbarYDownfiles.pack( side = RIGHT, fill = Y )
		
		self.DateTextDownFiles = Text(self.DateFrameDownLeft, font = self.ft, 
								  xscrollcommand = self.DateScrollbarXDownfiles.set, yscrollcommand = self.DateScrollbarYDownfiles.set, wrap = 'none')
		self.DateTextDownFiles.pack(fill = BOTH)
		
		self.DateScrollbarXDownfiles.config( command = self.DateTextDownFiles.xview )
		self.DateScrollbarYDownfiles.config( command = self.DateTextDownFiles.yview )
		# end down left Frame
		
		# start right frame
		self.DateFrameRight = ttk.LabelFrame(self.DateRoot, text = "")
		self.DateFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)


		self.DateButtonReset = ttk.Button(self.DateFrameRight, text = "Reset", command = self.DateReset) 
		self.DateButtonReset.pack(fill = X, side = TOP)

		self.DateButtonAddOneFolder = ttk.Button(self.DateFrameRight, text = "Read Rename ( Upbox )", command = self.DateReadRename) 
		self.DateButtonAddOneFolder.pack(fill = X, side = TOP)
						
		self.DateCheckCreateVar = IntVar() # StringVar()
		self.DateCheckCreate = ttk.Checkbutton(self.DateFrameRight, text = "Created Time", \
											variable = self.DateCheckCreateVar, onvalue = 1, offvalue = 0) 
		self.DateCheckCreate.pack(fill = X, side = TOP)
		self.DateCheckCreateVar.set(0)

		self.DateCheckModifyVar = IntVar()
		self.DateCheckModify = ttk.Checkbutton(self.DateFrameRight, text = "Modified Time", \
											variable = self.DateCheckModifyVar, onvalue = 1, offvalue = 0) 
		self.DateCheckModify.pack(fill = X, side = TOP)
		self.DateCheckModifyVar.set(0)

		self.DateCheckAccessVar = IntVar()
		self.DateCheckAccess = ttk.Checkbutton(self.DateFrameRight, text = "Accessed Time", \
											variable = self.DateCheckAccessVar, onvalue = 1, offvalue = 0) 
		self.DateCheckAccess.pack(fill = X, side = TOP)
		self.DateCheckAccessVar.set(0)
		
		self.DateLableInsertPosition = ttk.Label(self.DateFrameRight, text = "Insert: Postion ( -1 = end )", anchor = W)
		self.DateLableInsertPosition.pack(side = TOP, fill = X)
		
		self.DateEntryInsertPosition = ttk.Entry(self.DateFrameRight, font = self.ft)
		self.DateEntryInsertPosition.pack(side = TOP, fill = X)

		self.DateLableOutput = ttk.Label(self.DateFrameRight, text = 'Output Format: ( like %Y-%m-%d_%H.%M.%S )', anchor = W)
		self.DateLableOutput.pack(side = TOP, fill = X)
		
		self.DateEntryOutput = ttk.Entry(self.DateFrameRight, font = self.ft)
		self.DateEntryOutput.pack(side = TOP, fill = X)

		self.DateButtonInsertSelf = ttk.Button(self.DateFrameRight, text = "Insert Self Date", command = self.InsertSelfDate) 
		self.DateButtonInsertSelf.pack(fill = X, side = TOP)

		self.DateLableOutset = ttk.Label(self.DateFrameRight, text = 'Date Start From: ( fill like: 2001.01.01.12.00.00 )', anchor = W)
		self.DateLableOutset.pack(side = TOP, fill = X)
		
		self.DateEntryOutset = ttk.Entry(self.DateFrameRight, font = self.ft)
		self.DateEntryOutset.pack(side = TOP, fill = X)

		self.DateLableUnit = ttk.Label(self.DateFrameRight, text = "Interval Unit:", anchor = W)
		self.DateLableUnit.pack(side = TOP, fill = X)

		values = ('year', 'month', 'day', 'hour', 'minute', 'second')

		self.DateComboUnitVar = StringVar()
		self.DateComboUnit = ttk.Combobox(self.DateFrameRight, textvariable = self.DateComboUnitVar, state="readonly")
		self.DateComboUnit["values"] = values
		self.DateComboUnit.current(2) 
		self.DateComboUnit.pack(fill = X)

		self.DateLableInterval = ttk.Label(self.DateFrameRight, text = 'Interval:', anchor = W)
		self.DateLableInterval.pack(side = TOP, fill = X)
		
		self.DateEntryInterval = ttk.Entry(self.DateFrameRight, font = self.ft)
		self.DateEntryInterval.pack(side = TOP, fill = X)

		self.DateButtonInsertIncrement = ttk.Button(self.DateFrameRight, text = "Insert Date Ordinal", command = self.InsertDateIncrement) 
		self.DateButtonInsertIncrement.pack(fill = X, side = TOP)

		self.DateLableBlank = ttk.Label(self.DateFrameRight)
		self.DateLableBlank.pack(side = TOP, fill = X)

		self.DateButtonWriteRename = ttk.Button(self.DateFrameRight, text = "Write Results to Rename ( Downbox )", command = self.DateWriteRename) 
		self.DateButtonWriteRename.pack(fill = X, side = TOP)

		

		self.DateButtonModifyDate = ttk.Button(self.DateFrameRight, text = "Undo Modify", command = self.DateUndoModify) 
		self.DateButtonModifyDate.pack(fill = X, side = BOTTOM)

		self.DateButtonModifyDate = ttk.Button(self.DateFrameRight, text = "Modify Self Date", command = self.DateModify) 
		self.DateButtonModifyDate.pack(fill = X, side = BOTTOM)

		self.DateLableBlank = ttk.Label(self.DateFrameRight)
		self.DateLableBlank.pack(fill = X, side = BOTTOM)

		self.DateButtonModifyDatePreview = ttk.Button(self.DateFrameRight, text = "Modify Self Date ( Preview )", command = self.DateModifyPreview) 
		self.DateButtonModifyDatePreview.pack(fill = X, side = BOTTOM)

		self.DateCheckIncrementVar = IntVar()
		self.DateCheckIncrement = ttk.Checkbutton(self.DateFrameRight, text = "Date Increment", \
											variable = self.DateCheckIncrementVar, onvalue = 1, offvalue = 0) 
		self.DateCheckIncrement.pack(fill = X, side = BOTTOM)
		self.DateCheckIncrementVar.set(0)

		self.DateLableModify = ttk.Label(self.DateFrameRight, text = 'Notice: "Created Time" not supported', anchor = W)
		self.DateLableModify.pack(fill = X, side = BOTTOM)

		

		

		
		
		

		
		
		

		
		
