#coding=utf-8
#File_tools/file/Filter.py

import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog 
import os
import sys
import json
import copy



class CreateFrameFilter():

	def __init__(self):
		super().__init__()

		self.FilterRoot = None
		self.FilterPath = ''
		


	def FilterDefault(self):

		self.FilterDefaultLog()
		self.CreateWidgetsFrameFilter()
		self.FilterRestoreState()



	def FilterDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'filter' in j['file_tools']['file']:
			j['file_tools']['file']['filter'] = {}
		if not 'path_filter' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['path_filter'] = '.'
		if not 'including_string' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['including_string'] = ''
		if not 'excluding_string' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['excluding_string'] = ''
		if not 'file_size_max' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['file_size_max'] = ''
		if not 'file_size_min' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['file_size_min'] = ''
		if not 'filename_length_max' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['filename_length_max'] = ''
		if not 'filename_length_min' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['filename_length_min'] = ''
		if not 'check_files' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['check_files'] = '1'
		if not 'check_folders' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['check_folders'] = '1'
		if not 'check_case' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['check_case'] = '0'
		if not 'check_same_finename' in j['file_tools']['file']['filter']:
			j['file_tools']['file']['filter']['check_same_finename'] = '0'
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def FilterRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.FilterPath = j['file_tools']['file']['filter']['path_filter']
		self.FilterEntryPath.insert(0, self.FilterPath)
		self.FilterEntryIncluding.insert(0, j['file_tools']['file']['filter']['including_string'])
		self.FilterEntryExcluding.insert(0, j['file_tools']['file']['filter']['excluding_string'])
		self.FilterEntryMax.insert(0, j['file_tools']['file']['filter']['file_size_max'])
		self.FilterEntryMin.insert(0, j['file_tools']['file']['filter']['file_size_min'])
		self.FilterEntryNameMax.insert(0, j['file_tools']['file']['filter']['filename_length_max'])
		self.FilterEntryNameMin.insert(0, j['file_tools']['file']['filter']['filename_length_min'])
		self.FilterCheckFileVar.set( int(j['file_tools']['file']['filter']['check_files']) )
		self.FilterCheckFolderVar.set( int(j['file_tools']['file']['filter']['check_folders']) )
		self.FilterCheckCaseVar.set( int(j['file_tools']['file']['filter']['check_case']) )
		self.FilterCheckSameVar.set( int(j['file_tools']['file']['filter']['check_same_finename']) )
		f.close()

	

	def ReadFilterPath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.FilterPath = j['file_tools']['file']['filter']['path_filter']
		f.close()
	

	def FilterSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['file']['filter']['path_filter'] = self.FilterEntryPath.get()
			j['file_tools']['file']['filter']['including_string'] = self.FilterEntryIncluding.get()
			j['file_tools']['file']['filter']['excluding_string'] = self.FilterEntryExcluding.get()
			j['file_tools']['file']['filter']['file_size_max'] = self.FilterEntryMax.get()
			j['file_tools']['file']['filter']['file_size_min'] = self.FilterEntryMin.get()
			j['file_tools']['file']['filter']['filename_length_max'] = self.FilterEntryNameMax.get()
			j['file_tools']['file']['filter']['filename_length_min'] = self.FilterEntryNameMin.get()
			j['file_tools']['file']['filter']['check_files'] = str( self.FilterCheckFileVar.get() )
			j['file_tools']['file']['filter']['check_folders'] = str( self.FilterCheckFolderVar.get() )
			j['file_tools']['file']['filter']['check_case'] = str(self.FilterCheckCaseVar.get() )
			j['file_tools']['file']['filter']['check_same_finename'] = str( self.FilterCheckSameVar.get() )
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def FilterReset(self):
		self.FilterEntryPath.delete(0, "end")
		self.FilterTextDownFiles.delete("1.0", "end")
		self.FilterSaveEntry()


	def FilterCheckRepeat(self):
		files = self.FilterTextDownFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.FilterTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		files = set(files)
		files = sorted(files, key=self.natsort_key2)
		for file in files:
			if file == '\n' or file == '':
				continue
			self.FilterTextDownFiles.insert(INSERT, file)
			self.FilterTextDownFiles.insert(INSERT, '\n')
	

	def FilterAddDirection(self):
		self.ReadFilterPath()
		p = self.FilterPath
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.FilterTextDownFiles.delete("1.0", "end")
			self.FilterEntryPath.delete(0, "end")
			self.FilterEntryPath.insert(0, dir)
			self.FilterPath = dir
			self.FilterSaveEntry()
		except:pass


	def Filter(self):
		self.FilterSaveEntry()
		self.FilterTextDownFiles.delete("1.0", "end")
		dir = self.FilterPath
		include = self.FilterEntryIncluding.get()
		exclude = self.FilterEntryExcluding.get()
		including_file = self.FilterCheckFileVar.get()
		including_folder = self.FilterCheckFolderVar.get()
		case = self.FilterCheckCaseVar.get()
		is_exactly_same = self.FilterCheckSameVar.get()
		try:
			if self.FilterEntryMax.get() != '':
				max = int(self.FilterEntryMax.get().replace(',', '') )
			else:
				max = ''
			if self.FilterEntryMin.get() != '':
				min = int(self.FilterEntryMin.get().replace(',', '') )
			else:
				min = ''
		except:
			messagebox.showerror ("ERROR", "File Size:\n\nPlease fill a number")
			return
		try:
			if self.FilterEntryNameMax.get() != '':
				name_max = int( self.FilterEntryNameMax.get() ) 
			else:
				name_max = ''
			if self.FilterEntryNameMin.get() != '':
				name_min = int( self.FilterEntryNameMin.get()  )
			else:
				name_min = ''
		except:
			messagebox.showerror ("ERROR", "Filename Length:\n\nPlease fill a number")
			return
		files = self.fl.filter(dir, include, exclude, max, min, including_file, including_folder, case, is_exactly_same, name_max, name_min)
		for file in files:
			self.FilterTextDownFiles.insert(INSERT, file)
			self.FilterTextDownFiles.insert(INSERT, '\n')
		self.FilterCheckRepeat()
		if len(self.FilterTextDownFiles.get("1.0", "end") ) < 5:
			self.FilterTextDownFiles.insert(INSERT, "Nothing detected")
			self.FilterTextDownFiles.insert(INSERT, '\n')
		

	def OpenAll(self):
		self.FilterSaveEntry()
		tmp = messagebox.askquestion("Excute OPEN ALL !", "THIS IS EXTREMELY DANGERS !\n\nYet, still want to open them all?")
		if tmp == 'no':
			return
		files = self.FilterTextDownFiles.get("1.0", "end")
		files = files.split('\n')
		for file in files:
			if file == '\n' or file == '':
				continue
			os.startfile(file)

	def CreateWidgetsFrameFilter(self):

		# start up left Frame
		self.FilterFrameUpLeft = ttk.LabelFrame(self.FilterRoot, text = "")
		self.FilterFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)

		self.FilterLablePath = ttk.Label(self.FilterFrameUpLeft, text = "Filter Path", anchor = W)
		self.FilterLablePath.pack(side = TOP, fill = X)
		
		self.FilterScrollbarXPath = ttk.Scrollbar(self.FilterFrameUpLeft, orient = HORIZONTAL)
		self.FilterScrollbarXPath.pack( side = BOTTOM, fill = X )
		
		self.FilterEntryPath = ttk.Entry(self.FilterFrameUpLeft, xscrollcommand = self.FilterScrollbarXPath.set)
		self.FilterEntryPath.pack(fill = X)

		self.FilterLableBlank = ttk.Label(self.FilterFrameUpLeft)
		self.FilterLableBlank.pack(side = TOP, fill = X)

		self.FilterLableDescription = ttk.Label(self.FilterFrameUpLeft, text = 'Description:\n\n\
1. Walk through the root direction recursively\n\n\
2. Filter out every file(or folder) with specified string in it\n\
   (leaves blank means every file(or folder) )\n\n\
3. File(or folder) size will be between "Max" and "Min", same as "Filename Length"\n\
   (leaves blank means unlimited, set them same will be filtering out the exactly size of file(or folder) )\n\
    \
			', anchor = W)
		self.FilterLableDescription.pack(side = TOP, fill = X)
		
		self.FilterScrollbarXPath.config( command = self.FilterEntryPath.xview )
		# end up left Frame
		
		# start down left Frame
		self.FilterFrameDownLeft = ttk.LabelFrame(self.FilterRoot, text = r'Filtered')
		self.FilterFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.FilterScrollbarXDownFolders = ttk.Scrollbar(self.FilterFrameDownLeft, orient = HORIZONTAL)
		self.FilterScrollbarXDownFolders.pack( side = BOTTOM, fill = X )
		
		self.FilterScrollbarYDownFolders = ttk.Scrollbar(self.FilterFrameDownLeft, orient = VERTICAL)
		self.FilterScrollbarYDownFolders.pack( side = RIGHT, fill = Y )
		
		self.FilterTextDownFiles = Text(self.FilterFrameDownLeft, \
xscrollcommand = self.FilterScrollbarXDownFolders.set, yscrollcommand = self.FilterScrollbarYDownFolders.set, wrap = 'none')
		self.FilterTextDownFiles.pack(fill = BOTH)
		
		self.FilterScrollbarXDownFolders.config( command = self.FilterTextDownFiles.xview )
		self.FilterScrollbarYDownFolders.config( command = self.FilterTextDownFiles.yview )
		# end down left Frame
		
		# start right frame
		self.FilterFrameRight = ttk.LabelFrame(self.FilterRoot, text = "")
		self.FilterFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.FilterButtonReset = ttk.Button(self.FilterFrameRight, text = "Reset", command = self.FilterReset) 
		self.FilterButtonReset.pack(fill = X, side = TOP)
		
		self.FilterLableBlank = ttk.Label(self.FilterFrameRight)
		self.FilterLableBlank.pack(side = TOP, fill = X)
		
		self.FilterButtonAddDirection = ttk.Button(self.FilterFrameRight, text = "Add Direction", command = self.FilterAddDirection) 
		self.FilterButtonAddDirection.pack(fill = X, side = TOP)
		
		self.FilterLableBlank = ttk.Label(self.FilterFrameRight)
		self.FilterLableBlank.pack(side = TOP, fill = X)

		self.FilterLableBlank = ttk.Label(self.FilterFrameRight, text = 'Including String (like ".py" "asd")')
		self.FilterLableBlank.pack(side = TOP, fill = X)
				
		self.FilterEntryIncluding = ttk.Entry(self.FilterFrameRight)
		self.FilterEntryIncluding.pack(fill = X)

		self.FilterLableBlank = ttk.Label(self.FilterFrameRight, text = 'Excluding String (like ".pyc" "asdf")')
		self.FilterLableBlank.pack(side = TOP, fill = X)
				
		self.FilterEntryExcluding = ttk.Entry(self.FilterFrameRight)
		self.FilterEntryExcluding.pack(fill = X)

		self.FilterLableBlank = ttk.Label(self.FilterFrameRight, text = 'File Size: Max (Unit: Byte, 10240 = 10m)')
		self.FilterLableBlank.pack(side = TOP, fill = X)
				
		self.FilterEntryMax = ttk.Entry(self.FilterFrameRight)
		self.FilterEntryMax.pack(fill = X)

		self.FilterLableBlank = ttk.Label(self.FilterFrameRight, text = 'File Size: Min (Unit: Byte)')
		self.FilterLableBlank.pack(side = TOP, fill = X)
				
		self.FilterEntryMin = ttk.Entry(self.FilterFrameRight)
		self.FilterEntryMin.pack(fill = X)

		self.FilterLableBlank = ttk.Label(self.FilterFrameRight, text = 'Filename Length: Max')
		self.FilterLableBlank.pack(side = TOP, fill = X)
				
		self.FilterEntryNameMax = ttk.Entry(self.FilterFrameRight)
		self.FilterEntryNameMax.pack(fill = X)

		self.FilterLableBlank = ttk.Label(self.FilterFrameRight, text = 'Filename Length: Min')
		self.FilterLableBlank.pack(side = TOP, fill = X)
				
		self.FilterEntryNameMin = ttk.Entry(self.FilterFrameRight)
		self.FilterEntryNameMin.pack(fill = X)

		self.FilterCheckFileVar = IntVar()
		self.FilterCheckFile = ttk.Checkbutton(self.FilterFrameRight, text = "Including Files", \
											variable = self.FilterCheckFileVar, onvalue = 1, offvalue = 0) 
		self.FilterCheckFile.pack(fill = X, side = TOP)
		self.FilterCheckFileVar.set(1)

		self.FilterCheckFolderVar = IntVar()
		self.FilterCheckFolder = ttk.Checkbutton(self.FilterFrameRight, text = "Including Folders", \
											variable = self.FilterCheckFolderVar, onvalue = 1, offvalue = 0) 
		self.FilterCheckFolder.pack(fill = X, side = TOP)
		self.FilterCheckFolderVar.set(1)

		self.FilterCheckCaseVar = IntVar()
		self.FilterCheckCase = ttk.Checkbutton(self.FilterFrameRight, text = "Case Insensitive", \
											variable = self.FilterCheckCaseVar, onvalue = 1, offvalue = 0) 
		self.FilterCheckCase.pack(fill = X, side = TOP)
		self.FilterCheckCaseVar.set(0)

		self.FilterButtonFilter = ttk.Button(self.FilterFrameRight, text = "Filter", command = self.Filter) #bg = "#e1e1e1"
		self.FilterButtonFilter.pack(side = TOP, fill = X)

		self.FilterCheckSameVar = IntVar()
		self.FilterCheckSame = ttk.Checkbutton(self.FilterFrameRight, text = "Exactly Same Filename", \
											variable = self.FilterCheckSameVar, onvalue = 1, offvalue = 0) 
		self.FilterCheckSame.pack(fill = X, side = TOP)
		self.FilterCheckSameVar.set(0)

		self.FilterButtonOpen = ttk.Button(self.FilterFrameRight, text = "OPEN ALL", command = self.OpenAll) #bg = "#e1e1e1"
		self.FilterButtonOpen.pack(side = BOTTOM, fill = X)

		self.FilterLableBlank = ttk.Label(self.FilterFrameRight, text = 'EXTREMELY DANGERS !')
		self.FilterLableBlank.pack(side = BOTTOM, fill = X)
		
		# end right frame