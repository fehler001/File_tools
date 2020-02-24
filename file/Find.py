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



class CreateFrameFind():

	def __init__(self):
		super().__init__()
		self.FindRoot = None
		self.FindSource = ''
		self.Destination = ''



	def FindDefault(self):

		self.FindDefaultLog()
		self.CreateWidgetsFrameFind()
		self.FindRestoreState()

		


	def FindDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'find' in j['file_tools']['file']:
			j['file_tools']['file']['find'] = {}
		if not 'path_find_src' in j['file_tools']['file']['find']:
			j['file_tools']['file']['find']['path_find_src'] = ''
		if not 'path_find_dst' in j['file_tools']['file']['find']:
			j['file_tools']['file']['find']['path_find_dst'] = ''
		if not 'check_sub' in j['file_tools']['file']['find']:
			j['file_tools']['file']['find']['check_sub'] = 0
		if not 'check_files' in j['file_tools']['file']['find']:
			j['file_tools']['file']['find']['check_files'] = 1
		if not 'check_folders' in j['file_tools']['file']['find']:
			j['file_tools']['file']['find']['check_folders'] = 0
		if not 'check_recur_src' in j['file_tools']['file']['find']:
			j['file_tools']['file']['find']['check_recur_src'] = 1
		if not 'check_recur_dst' in j['file_tools']['file']['find']:
			j['file_tools']['file']['find']['check_recur_dst'] = 1
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def FindRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.FindSource = j['file_tools']['file']['find']['path_find_src']
		self.FindEntrySource.insert(0, self.FindSource)
		self.Destination = j['file_tools']['file']['find']['path_find_dst']
		self.FindEntryDestination.insert(0, self.Destination)
		self.FindCheckSubfolderVar.set( j['file_tools']['file']['find']['check_sub'])
		self.FindCheckFileVar.set( j['file_tools']['file']['find']['check_files'])
		self.FindCheckFolderVar.set( j['file_tools']['file']['find']['check_folders'])
		self.FindCheckSourceVar.set( j['file_tools']['file']['find']['check_recur_src'])
		self.FindCheckDestinationVar.set( j['file_tools']['file']['find']['check_recur_dst'])
		f.close()



	def FindReadPath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.FindSource = j['file_tools']['file']['find']['path_find_src']
		self.Destination = j['file_tools']['file']['find']['path_find_dst']
		f.close()
	


	def FindSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['file']['find']['path_find_src'] = self.FindEntrySource.get()
			j['file_tools']['file']['find']['path_find_dst'] = self.FindEntryDestination.get()
			j['file_tools']['file']['find']['check_sub'] = self.FindCheckSubfolderVar.get()
			j['file_tools']['file']['find']['check_files'] = self.FindCheckFileVar.get()
			j['file_tools']['file']['find']['check_folders'] = self.FindCheckFolderVar.get()
			j['file_tools']['file']['find']['check_recur_src'] = self.FindCheckSourceVar.get()
			j['file_tools']['file']['find']['check_recur_dst'] = self.FindCheckDestinationVar.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()




	def FindReset(self):
		self.FindEntrySource.delete(0, "end")
		self.FindEntryDestination.delete(0, "end")
		self.FindTextDownFiles.delete("1.0", "end")
		self.FindSaveEntry()
	

	def FindCheckRepeat(self):
		files = self.FindTextDownFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.FindTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		files = set(files)
		files = sorted(files, key=self.natsort_key2)
		files = self.bl.clean_list(files)
		for file in files:
			self.FindTextDownFiles.insert(INSERT, file)
			self.FindTextDownFiles.insert(INSERT, '\n')
			

	def FindAddSource(self):
		self.FindReadPath()
		p = self.FindSource
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.FindTextDownFiles.delete("1.0", "end")
			self.FindEntrySource.delete(0, "end")
			self.FindEntrySource.insert(0, dir)
			self.FindSource = dir
			self.FindSaveEntry()
		except:pass


	def FindAddDestination(self):
		self.FindReadPath()
		p = self.Destination
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.FindTextDownFiles.delete("1.0", "end")
			self.FindEntryDestination.delete(0, "end")
			self.FindEntryDestination.insert(0, dir)
			self.Destination = dir
			self.FindSaveEntry()
		except:pass


	def Find(self, mode = 1):
		self.FindSaveEntry()
		self.FindTextDownFiles.delete("1.0", "end")
		src = self.FindEntrySource.get()
		dst = self.FindEntryDestination.get()
		including_file = self.FindCheckFileVar.get()
		including_folder = self.FindCheckFolderVar.get()
		is_subfolder_with_same_name = self.FindCheckSubfolderVar.get()
		is_recur_src = self.FindCheckSourceVar.get()
		is_recur_dst = self.FindCheckDestinationVar.get()
		is_rename = self.FindCheckRenameVar.get()
		if mode == 1:
			files = self.fl.find_same_folder_strctrue(src, dst, is_subfolder_with_same_name)
		if mode == 2:
			if is_rename == 1:
				src = self.RenameTextUpFiles.get('1.0', 'end')
				src = src.split('\n')
			files = self.fl.find_files_with_same_name_by_list(src, dst, including_file, including_folder, \
				is_recur_src = is_recur_src, is_recur_dst = is_recur_dst, is_list = is_rename)
		n = 0
		for file in files:
			self.FindTextDownFiles.insert(INSERT, file)
			self.FindTextDownFiles.insert(INSERT, '\n')
			n = n + 1
		self.FindFrameDownLeft.config(text = r'Found  ' + str(n))

		self.FindCheckRepeat()
		if len(self.FindTextDownFiles.get("1.0", "end") ) < 4:
			self.FindTextDownFiles.insert(INSERT, "Nothing detected")
			self.FindTextDownFiles.insert(INSERT, '\n')



	def Find2(self):
		self.Find(mode = 2)



	def CreateWidgetsFrameFind(self):

		# start up left Frame
		self.FindFrameUpLeft = ttk.LabelFrame(self.FindRoot, text = "")
		self.FindFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)

		# start Frame1
		self.FindFrame1 = ttk.Frame(self.FindFrameUpLeft)
		self.FindFrame1.pack(side = TOP, fill = X)

		self.FindScrollbarXSource = ttk.Scrollbar(self.FindFrame1, orient = HORIZONTAL)
		self.FindScrollbarXSource.pack( side = BOTTOM, fill = X )

		self.FindLableSource = ttk.Label(self.FindFrame1, text = "Find Same File Strcture: Source Path", anchor = W)
		self.FindLableSource.pack(side = TOP, fill = X)
		
		self.FindEntrySource = ttk.Entry(self.FindFrame1, font = self.ft, xscrollcommand = self.FindScrollbarXSource.set)
		self.FindEntrySource.pack(fill = X)

		self.FindEntrySource.drop_target_register(DND_FILES, DND_TEXT)
		self.FindEntrySource.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.FindScrollbarXSource.config( command = self.FindEntrySource.xview )
		# end Frame1

		# start Frame2
		self.FindFrame2 = ttk.Frame(self.FindFrameUpLeft)
		self.FindFrame2.pack(side = TOP, fill = X)

		self.FindScrollbarXDestination = ttk.Scrollbar(self.FindFrame2, orient = HORIZONTAL)
		self.FindScrollbarXDestination.pack( side = BOTTOM, fill = X )

		self.FindLableDestination = ttk.Label(self.FindFrame2, text = "Find Same File Strcture: Destination Path", anchor = W)
		self.FindLableDestination.pack(side = TOP, fill = X)
		
		self.FindEntryDestination = ttk.Entry(self.FindFrame2, font = self.ft, xscrollcommand = self.FindScrollbarXDestination.set)
		self.FindEntryDestination.pack(fill = X)

		self.FindEntryDestination.drop_target_register(DND_FILES, DND_TEXT)
		self.FindEntryDestination.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.FindScrollbarXDestination.config( command = self.FindEntryDestination.xview )
		# end Frame2

		self.FindLableDescription = ttk.Label(self.FindFrameUpLeft, text = '\
src  =  folder A { a.txt, b.txt, folder B { c.mp4 } }\n\
dst  =  folder X { a.txt, b.txt, c.mp4, d.txt, folder B { c.mp4, e.mp4, b.txt, folder A { a.txt, b.txt, folder B { c.mp4 } }  }  }\n\n\
"Find Same File Structure"\n\
Found: folder X { a.txt, b.txt, folder B { c.mp4,  if "Including..." checked: folder A { a.txt, b.txt, folder B { c.mp4 }} }\n\n\
"Find All Files in Same Name"\n\
Found:  All the files or folders in dst with exactly same name in "a.txt, b.txt, c.mp4, folder B"\n\n\
	\
			', anchor = W)
		self.FindLableDescription.pack(side = TOP, fill = X)
		# end up left Frame
		
		# start down left Frame
		self.FindFrameDownLeft = ttk.LabelFrame(self.FindRoot, text = r'Found        ( Quantity of files determine the elapsed time of process )')
		self.FindFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.FindScrollbarXDownFiles = ttk.Scrollbar(self.FindFrameDownLeft, orient = HORIZONTAL)
		self.FindScrollbarXDownFiles.pack( side = BOTTOM, fill = X )
		
		self.FindScrollbarYDownFiles = ttk.Scrollbar(self.FindFrameDownLeft, orient = VERTICAL)
		self.FindScrollbarYDownFiles.pack( side = RIGHT, fill = Y )
		
		self.FindTextDownFiles = Text(self.FindFrameDownLeft, font = self.ft, xscrollcommand = self.FindScrollbarXDownFiles.set, yscrollcommand = self.FindScrollbarYDownFiles.set, wrap = 'none')
		self.FindTextDownFiles.pack(fill = BOTH)
		
		self.FindScrollbarXDownFiles.config( command = self.FindTextDownFiles.xview )
		self.FindScrollbarYDownFiles.config( command = self.FindTextDownFiles.yview )
		# end down left Frame
		
		# start right frame
		self.FindFrameRight = ttk.LabelFrame(self.FindRoot, text = "")
		self.FindFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.FindButtonReset = ttk.Button(self.FindFrameRight, text = "Reset", command = self.FindReset) 
		self.FindButtonReset.pack(fill = X, side = TOP)
		
		self.FindLableBlank = ttk.Label(self.FindFrameRight)
		self.FindLableBlank.pack(side = TOP, fill = X)
		
		self.FindButtonAddSource = ttk.Button(self.FindFrameRight, text = "Add Source", command = self.FindAddSource) 
		self.FindButtonAddSource.pack(fill = X, side = TOP)
		
		self.FindLableBlank = ttk.Label(self.FindFrameRight)
		self.FindLableBlank.pack(side = TOP, fill = X)

		self.FindButtonAddDestination = ttk.Button(self.FindFrameRight, text = "Add Destination", command = self.FindAddDestination) 
		self.FindButtonAddDestination.pack(fill = X, side = TOP)

		self.FindLableBlank = ttk.Label(self.FindFrameRight)
		self.FindLableBlank.pack(side = TOP, fill = X)

		self.FindLableBlank = ttk.Label(self.FindFrameRight)
		self.FindLableBlank.pack(side = TOP, fill = X)

		self.FindCheckSubfolderVar = IntVar() # StringVar()
		self.FindCheckSubfolder = ttk.Checkbutton(self.FindFrameRight, text = "Including subfolder with same name", \
											variable = self.FindCheckSubfolderVar, onvalue = 1, offvalue = 0) 
		self.FindCheckSubfolder.pack(fill = X, side = TOP)
		self.FindCheckSubfolderVar.set(0)

		self.FindButtonFind = ttk.Button(self.FindFrameRight, text = "Find Same File Structure", command = self.Find) #bg = "#e1e1e1"
		self.FindButtonFind.pack(side = TOP, fill = X)

		self.FindLableBlank = ttk.Label(self.FindFrameRight)
		self.FindLableBlank.pack(side = TOP, fill = X)

		self.FindCheckFileVar = IntVar()
		self.FindCheckFile = ttk.Checkbutton(self.FindFrameRight, text = "Including Files", \
											variable = self.FindCheckFileVar, onvalue = 1, offvalue = 0) 
		self.FindCheckFile.pack(fill = X, side = TOP)
		self.FindCheckFileVar.set(1)

		self.FindCheckFolderVar = IntVar()
		self.FindCheckFolder = ttk.Checkbutton(self.FindFrameRight, text = "Including Folders", \
											variable = self.FindCheckFolderVar, onvalue = 1, offvalue = 0) 
		self.FindCheckFolder.pack(fill = X, side = TOP)
		self.FindCheckFolderVar.set(0)

		self.FindCheckSourceVar = IntVar()
		self.FindCheckSource = ttk.Checkbutton(self.FindFrameRight, text = "Including Subfolder in Source", \
											variable = self.FindCheckSourceVar, onvalue = 1, offvalue = 0) 
		self.FindCheckSource.pack(fill = X, side = TOP)
		self.FindCheckSourceVar.set(1)

		self.FindCheckDestinationVar = IntVar()
		self.FindCheckDestination = ttk.Checkbutton(self.FindFrameRight, text = "Including Subfolder in Destination", \
											variable = self.FindCheckDestinationVar, onvalue = 1, offvalue = 0) 
		self.FindCheckDestination.pack(fill = X, side = TOP)
		self.FindCheckDestinationVar.set(1)

		self.FindCheckRenameVar = IntVar()
		self.FindCheckRename = ttk.Checkbutton(self.FindFrameRight, text = 'Taking "Rename" Upbox as Source', \
											variable = self.FindCheckRenameVar, onvalue = 1, offvalue = 0) 
		self.FindCheckRename.pack(fill = X, side = TOP)
		self.FindCheckRenameVar.set(0)

		self.FindButtonFind2 = ttk.Button(self.FindFrameRight, text = "Find All Files in Same Name", command = self.Find2)
		self.FindButtonFind2.pack(side = TOP, fill = X)

		# end right frame