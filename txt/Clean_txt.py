#coding=utf-8
#File_tools/txt/String_encoding_decoding.py

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



class CreateFrameClean():

	def __init__(self):
		super().__init__()

		self.CleanRoot = None

		self.CleanTxtPath = ''
		self.CleanSavePath = ''



	def CleanDefault(self):

		self.CleanDefaultLog()
		self.CreateWidgetsFrameClean()
		self.CleanRestoreState()
		

	def CleanDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'clean' in j['file_tools']['txt']:
			j['file_tools']['txt']['clean'] = {}
		if not 'path_txt' in j['file_tools']['txt']['clean']:
			j['file_tools']['txt']['clean']['path_txt'] = ''
		if not 'path_save' in j['file_tools']['txt']['clean']:
			j['file_tools']['txt']['clean']['path_save'] = ''
		if not 'combo_mode' in j['file_tools']['txt']['clean']:
			j['file_tools']['txt']['clean']['combo_mode'] = 'mode 1'
		if not 'check_repeat' in j['file_tools']['txt']['clean']:
			j['file_tools']['txt']['clean']['check_repeat'] = 0
		if not 'check_sort' in j['file_tools']['txt']['clean']:
			j['file_tools']['txt']['clean']['check_sort'] = 0
		if not 'check_enter' in j['file_tools']['txt']['clean']:
			j['file_tools']['txt']['clean']['check_enter'] = 0
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()




	def CleanRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.CleanTxtPath = j['file_tools']['txt']['clean']['path_txt']
		self.CleanSavePath = j['file_tools']['txt']['clean']['path_save']
		self.CleanEntryTxtSource.insert(0, self.CleanTxtPath)
		self.CleanEntryTxtDestination.insert(0, self.CleanSavePath )
		self.CleanComboMode.set(j['file_tools']['txt']['clean']['combo_mode'])
		self.CleanCheckRepeatVar.set( j['file_tools']['txt']['clean']['check_repeat'] )
		self.CleanCheckSortVar.set( j['file_tools']['txt']['clean']['check_sort'] )
		self.CleanCheckEnterVar.set( j['file_tools']['txt']['clean']['check_enter'] )
		f.close()


	

	def ReadCleanPath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.CleanTxtPath = j['file_tools']['txt']['clean']['path_txt']
		self.CleanSavePath = j['file_tools']['txt']['clean']['path_save']
		f.close()



	def CleanSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['txt']['clean']['path_txt'] = self.CleanEntryTxtSource.get()
			j['file_tools']['txt']['clean']['path_save'] = self.CleanEntryTxtDestination.get()
			j['file_tools']['txt']['clean']['combo_mode'] = self.CleanComboMode.get()
			j['file_tools']['txt']['clean']['check_repeat'] = self.CleanCheckRepeatVar.get()
			j['file_tools']['txt']['clean']['check_sort'] = self.CleanCheckSortVar.get()
			j['file_tools']['txt']['clean']['check_enter'] = self.CleanCheckEnterVar.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def CleanReset(self):
		self.CleanEntryTxtSource.delete(0, "end")
		self.CleanEntryTxtDestination.delete(0, "end")
		self.CleanTextDown.delete("1.0", "end")
		self.CleanSaveEntry()
	


	def CleanAddSource(self):
		self.ReadCleanPath()
		p = self.CleanTxtPath
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(initialdir = p) 
		else:
			dir = filedialog.askopenfilename(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.CleanEntryTxtSource.delete(0, "end")
			self.CleanEntryTxtSource.insert(0, dir)
			self.CleanTxtPath = dir
			self.CleanSaveEntry()
		except:pass
	

	def CleanAddDirection(self):
		self.ReadCleanPath()
		p = self.CleanSavePath
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.CleanEntryTxtDestination.delete(0, "end")
			self.CleanEntryTxtDestination.insert(0, dir)
			self.CleanSavePath = dir
			self.CleanSaveEntry()
		except:pass



	def CleanTxtPreview(self):
		self.CleanTxt(preview = True)

	def CleanTxt(self, preview = False):
		self.CleanSaveEntry()
		mode = self.CleanComboMode.get()
		src = self.CleanEntryTxtSource.get().replace('\\', '/')
		dst = self.CleanEntryTxtDestination.get().replace('\\', '/')
		is_repeat = self.CleanCheckRepeatVar.get()
		is_sort = self.CleanCheckSortVar.get()
		is_enter = self.CleanCheckEnterVar.get()
		if not os.path.isfile(src):
			messagebox.showerror ("Warrning", "_____TXT SOURCE ERROR_____")
			return

		if preview == True:
			self.CleanTextDown.delete("1.0", "end")
			f = open(src, 'r', encoding = 'utf-8')
			cont = self.tl.get_txt_content(src, split = 'wholetext')
			if cont == -1:
				return
			new_cont = self.tl.clean_txt(cont, mode = mode, is_repeat = is_repeat, is_sort = is_sort, is_enter = is_enter)
			if new_cont == -1:
				return
			for line in new_cont:
				self.CleanTextDown.insert(INSERT, line)
				self.CleanTextDown.insert(INSERT, '\n')
			return

		if not os.path.isdir(dst):
			messagebox.showerror ("Warrning", "_____PATH ERROR_____\n\nPath should be a direction( a folder )")
			return

		pinfo = self.bl.get_path_info(src)
		n = 1
		switch = 1
		while switch:
			new_txt = dst + '/' + pinfo['name']  + '(' + str(n) + ')' + pinfo['ext']
			if os.path.exists(new_txt):
				n = n + 1
			else:
				switch = 0
		
		new_cont = self.tl.clean_txt(src, mode = mode, is_repeat = is_repeat, is_sort = is_sort, is_enter = is_enter)
		if new_cont == -1:
			return
		f = open(new_txt, 'w', encoding = 'utf-8')
		for line in new_cont:
			if line == '':
				f.write('\n')
			else:
				f.write(line + '\n')
		f.close()		
		


	def CreateWidgetsFrameClean(self):

		# start up left Frame
		self.CleanFrameUpLeft = ttk.LabelFrame(self.CleanRoot, text = "")
		self.CleanFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)

		# start Frame1
		self.CleanFrame1 = ttk.Frame(self.CleanFrameUpLeft)
		self.CleanFrame1.pack(side = TOP, fill = X)

		self.CleanScrollbarXTxtSource = ttk.Scrollbar(self.CleanFrame1, orient = HORIZONTAL)
		self.CleanScrollbarXTxtSource.pack( side = BOTTOM, fill = X )

		self.CleanLabelTxtSource = ttk.Label(self.CleanFrame1, text = "Txt Source Path", anchor = W)
		self.CleanLabelTxtSource.pack(side = TOP, fill = X)
		
		self.CleanEntryTxtSource = ttk.Entry(self.CleanFrame1, font = self.ft, xscrollcommand = self.CleanScrollbarXTxtSource.set)
		self.CleanEntryTxtSource.pack(fill = X)

		self.CleanEntryTxtSource.drop_target_register(DND_FILES, DND_TEXT)
		self.CleanEntryTxtSource.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.CleanScrollbarXTxtSource.config( command = self.CleanEntryTxtSource.xview )
		# end Frame1

		# start Frame2
		self.CleanFrame2 = ttk.Frame(self.CleanFrameUpLeft)
		self.CleanFrame2.pack(side = TOP, fill = X)

		self.CleanScrollbarXTxtDestination = ttk.Scrollbar(self.CleanFrame2, orient = HORIZONTAL)
		self.CleanScrollbarXTxtDestination.pack( side = BOTTOM, fill = X )

		self.CleanLabelTxtDestination = ttk.Label(self.CleanFrame2, text = "Txt Save Path", anchor = W)
		self.CleanLabelTxtDestination.pack(side = TOP, fill = X)
		
		self.CleanEntryTxtDestination = ttk.Entry(self.CleanFrame2, font = self.ft, xscrollcommand = self.CleanScrollbarXTxtDestination.set)
		self.CleanEntryTxtDestination.pack(fill = X)

		self.CleanEntryTxtDestination.drop_target_register(DND_FILES, DND_TEXT)
		self.CleanEntryTxtDestination.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.CleanScrollbarXTxtDestination.config( command = self.CleanEntryTxtDestination.xview )
		# end Frame2

		self.CleanLabelDescription = ttk.Label(self.CleanFrameUpLeft, text = '\
Description:\n\n\
mode 1: Keep original format\n\n\
mode 2: Remove all empty lines\n\n\
	\
			', anchor = W)
		self.CleanLabelDescription.pack(side = TOP, fill = X)
		# end up left Frame
		

		# start down left Frame
		self.CleanFrameDownLeft = ttk.LabelFrame(self.CleanRoot, text = "Preview")
		self.CleanFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.CleanScrollbarXDownText = ttk.Scrollbar(self.CleanFrameDownLeft, orient = HORIZONTAL)
		self.CleanScrollbarXDownText.pack( side = BOTTOM, fill = X )
		
		self.CleanScrollbarYDownText = ttk.Scrollbar(self.CleanFrameDownLeft, orient = VERTICAL)
		self.CleanScrollbarYDownText.pack( side = RIGHT, fill = Y )
		
		self.CleanTextDown = Text(self.CleanFrameDownLeft, font = self.ft, xscrollcommand = self.CleanScrollbarXDownText.set, yscrollcommand = self.CleanScrollbarYDownText.set, wrap = 'none')
		self.CleanTextDown.pack(fill = BOTH)
		
		self.CleanScrollbarXDownText.config( command = self.CleanTextDown.xview )
		self.CleanScrollbarYDownText.config( command = self.CleanTextDown.yview )
		# end down left Frame
		
		# start right frame
		self.CleanFrameRight = ttk.LabelFrame(self.CleanRoot, text = "")
		self.CleanFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.CleanButtonReset = ttk.Button(self.CleanFrameRight, text = "Reset", command = self.CleanReset) 
		self.CleanButtonReset.pack(fill = X, side = TOP)

		self.CleanButtonSetSource = ttk.Button(self.CleanFrameRight, text = "Add txt", command = self.CleanAddSource) 
		self.CleanButtonSetSource.pack(fill = X, side = TOP)

		self.CleanButtonSetDestination = ttk.Button(self.CleanFrameRight, text = "Set Save Path", command = self.CleanAddDirection) 
		self.CleanButtonSetDestination.pack(fill = X, side = TOP)

		self.CleanLabelBlank = ttk.Label(self.CleanFrameRight)
		self.CleanLabelBlank.pack(side = TOP, fill = X)

		self.CleanCheckRepeatVar = IntVar()
		self.CleanCheckRepeat = ttk.Checkbutton(self.CleanFrameRight, text = 'Remove repeat lines', \
											variable = self.CleanCheckRepeatVar, onvalue = 1, offvalue = 0) 
		self.CleanCheckRepeat.pack(fill = X, side = TOP)
		self.CleanCheckRepeatVar.set(0)

		self.CleanCheckSortVar = IntVar()
		self.CleanCheckSort = ttk.Checkbutton(self.CleanFrameRight, text = 'Sort lines', \
											variable = self.CleanCheckSortVar, onvalue = 1, offvalue = 0) 
		self.CleanCheckSort.pack(fill = X, side = TOP)
		self.CleanCheckSortVar.set(0)

		self.CleanCheckEnterVar = IntVar()
		self.CleanCheckEnter = ttk.Checkbutton(self.CleanFrameRight, text = 'Insert "enter" every line', \
											variable = self.CleanCheckEnterVar, onvalue = 1, offvalue = 0) 
		self.CleanCheckEnter.pack(fill = X, side = TOP)
		self.CleanCheckEnterVar.set(0)
		
		values = ('mode 1', 'mode 2')

		self.CleanComboModeVar = StringVar()
		self.CleanComboMode = ttk.Combobox(self.CleanFrameRight, textvariable = self.CleanComboModeVar, state = "readonly")
		self.CleanComboMode["values"] = values
		self.CleanComboMode.current(0) 
		self.CleanComboMode.pack(fill = X)

		self.CleanButtonTxt = ttk.Button(self.CleanFrameRight, text = "Clean txt ( preview )", command = self.CleanTxtPreview)
		self.CleanButtonTxt.pack(side = TOP, fill = X)

		self.CleanLabelBlank = ttk.Label(self.CleanFrameRight)
		self.CleanLabelBlank.pack(side = TOP, fill = X)

		self.CleanButtonTxt = ttk.Button(self.CleanFrameRight, text = "Clean txt", command = self.CleanTxt)
		self.CleanButtonTxt.pack(side = TOP, fill = X)

		# end right frame