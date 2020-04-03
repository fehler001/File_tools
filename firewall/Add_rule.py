#coding=utf-8
#File_tools/firewall/Add_rule.py

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



class CreateFrameARule():

	def __init__(self):
		super().__init__()

		self.ARuleRoot = None
		self.ARulePath = ''
		


	def ARuleDefault(self):

		self.ARuleDefaultLog()
		self.CreateWidgetsFrameARule()
		self.ARuleRestoreState()



	def ARuleDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'addrule' in j['file_tools']['firewall']:
			j['file_tools']['firewall']['addrule'] = {}
		if not 'path_addrule' in j['file_tools']['firewall']['addrule']:
			j['file_tools']['firewall']['addrule']['path_addrule'] = ''
		if not 'extension' in j['file_tools']['firewall']['addrule']:
			j['file_tools']['firewall']['addrule']['extension'] = '.exe'
		if not 'check_inbound' in j['file_tools']['firewall']['addrule']:
			j['file_tools']['firewall']['addrule']['check_inbound'] = 0
		if not 'check_outbound' in j['file_tools']['firewall']['addrule']:
			j['file_tools']['firewall']['addrule']['check_outbound'] = 1
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def ARuleRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.ARulePath = j['file_tools']['firewall']['addrule']['path_addrule']
		self.ARuleEntryPath.insert(0, self.ARulePath)
		self.ARuleEntryExtension.insert(0, j['file_tools']['firewall']['addrule']['extension'])
		self.ARuleCheckInVar.set( j['file_tools']['firewall']['addrule']['check_inbound'] )
		self.ARuleCheckOutVar.set( j['file_tools']['firewall']['addrule']['check_outbound'] )
		f.close()

	

	def ReadARulePath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.ARulePath = j['file_tools']['firewall']['addrule']['path_addrule']
		f.close()
	

	def ARuleSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['firewall']['addrule']['path_addrule'] = self.ARuleEntryPath.get()
			j['file_tools']['firewall']['addrule']['extension'] = self.ARuleEntryExtension.get()
			j['file_tools']['firewall']['addrule']['check_inbound'] = self.ARuleCheckInVar.get()
			j['file_tools']['firewall']['addrule']['check_outbound'] = self.ARuleCheckOutVar.get()
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def ARuleReset(self):
		self.ARuleEntryPath.delete(0, "end")
		self.ARuleTextDownFiles.delete("1.0", "end")
		self.ARuleSaveEntry()


	def ARuleCheckRepeat(self):
		files = self.ARuleTextDownFiles.get("1.0", "end")  #"end-1c" till second last charactor
		self.ARuleTextDownFiles.delete("1.0", "end")
		files = files.split('\n')
		files = set(files)
		files = sorted(files, key=self.natsort_key2)
		for file in files:
			if file == '\n' or file == '':
				continue
			self.ARuleTextDownFiles.insert(INSERT, file)
			self.ARuleTextDownFiles.insert(INSERT, '\n')
	

	def ARuleAddDirection(self):
		self.ReadARulePath()
		p = self.ARulePath
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.ARuleTextDownFiles.delete("1.0", "end")
			self.ARuleEntryPath.delete(0, "end")
			self.ARuleEntryPath.insert(0, dir)
			self.ARulePath = dir
			self.ARuleSaveEntry()
		except:pass



	def ARuleAddTxt(self):
		self.ReadARulePath()
		p = self.ARulePath
		typ = [('txt file','*.txt'), ('all', '*')] 
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(filetypes = typ, initialdir = p) 
		else:
			dir = filedialog.askopenfilename(filetypes = typ, initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.ARuleTextDownFiles.delete("1.0", "end")
			self.ARuleEntryPath.delete(0, "end")
			self.ARuleEntryPath.insert(0, dir)
			self.ARulePath = dir[0 : dir.rfind(r'/')]
			self.ARuleSaveEntry()
		except:pass



	def ARuleSearchFiles(self):
		self.ARuleSaveEntry()
		self.ARuleTextDownFiles.delete("1.0", "end")
		path = self.ARuleEntryPath.get()
		ext = self.ARuleEntryExtension.get()
		if self.bl.check_legit_string(ext) == -1:
			return
		n = 0
		if os.path.isdir(path):
			files = self.fl.filter(path, include = ext, \
					including_file = 1, including_folder = 0, case_insensitive = 1, is_extension = 1)
			for file in files:
				self.ARuleTextDownFiles.insert(INSERT, file)
				self.ARuleTextDownFiles.insert(INSERT, '\n')
				n = n + 1
		if os.path.isfile(path):
			dirs = self.tl.get_txt_content(path, '#')
			if dirs == -1:
				return
			for dir in dirs:
				if not os.path.isdir(dir):
					continue
				files = self.fl.filter(dir, include = ext, \
						including_file = 1, including_folder = 0, case_insensitive = 1, is_extension = 1)
				
				for file in files:
					self.ARuleTextDownFiles.insert(INSERT, file)
					self.ARuleTextDownFiles.insert(INSERT, '\n')
					n = n + 1
		self.ARuleFrameDownLeft.config( text = str(n) + '  \
Pending to add in firewall rules, repeat checking will be handled  ( NOTE: DO NOT ADD SYSTEM FILE )')
		self.ARuleCheckRepeat()
		if len(self.ARuleTextDownFiles.get("1.0", "end") ) < 4:
			self.ARuleTextDownFiles.insert(INSERT, "Nothing detected")
			self.ARuleTextDownFiles.insert(INSERT, '\n')



	def AddRule(self):
		self.ARuleSaveEntry()
		is_inbound = self.ARuleCheckInVar.get()
		is_outbound = self.ARuleCheckOutVar.get()
		if is_inbound == 0 and is_outbound == 0:
			messagebox.showerror ("ERROR", '"Add Inbound" and "Add Outbound" are both unchecked')
			return
		files = self.ARuleTextDownFiles.get("1.0", "end")
		if len(files) < 4:
			messagebox.showerror ("Warrning", "_____EMPTY BOX_____")
			return
		tmp = messagebox.askquestion("Adding Files into Firewall rules !", "Are you sure?")
		if tmp == 'no':
			return
		files = files.split('\n')
		if self.fwl.add_rules(files, is_in = is_inbound, is_out = is_outbound) == -1:
			return




	def CreateWidgetsFrameARule(self):

		# start up left Frame
		self.ARuleFrameUpLeft = ttk.LabelFrame(self.ARuleRoot, text = "")
		self.ARuleFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.48)

		self.ARuleLabelPath = ttk.Label(self.ARuleFrameUpLeft, text = "Path to search", anchor = W)
		self.ARuleLabelPath.pack(side = TOP, fill = X)
		
		self.ARuleScrollbarXPath = ttk.Scrollbar(self.ARuleFrameUpLeft, orient = HORIZONTAL)
		self.ARuleScrollbarXPath.pack( side = BOTTOM, fill = X )
		
		self.ARuleEntryPath = ttk.Entry(self.ARuleFrameUpLeft, font = self.ft, xscrollcommand = self.ARuleScrollbarXPath.set)
		self.ARuleEntryPath.pack(fill = X)

		self.ARuleEntryPath.drop_target_register(DND_FILES, DND_TEXT)
		self.ARuleEntryPath.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.ARuleButtonOpen = ttk.Button(self.ARuleFrameUpLeft, text = "  Open  ", \
													command = lambda: os.startfile( self.ARuleEntryPath.get() )  ) 
		self.ARuleButtonOpen.pack(anchor = W, side = TOP)

		self.ARuleLabelBlank = ttk.Label(self.ARuleFrameUpLeft)
		self.ARuleLabelBlank.pack(side = TOP, fill = X)

		self.ARuleLabelDescription = ttk.Label(self.ARuleFrameUpLeft, text = 'Description:   (This function only supports windows powershell)\n\n\
1. Walk through the root direction recursively and find all the "exe" files, then put them into windows firewall rules\n\
   (if you use global proxy, windows firewall will not work, BE CAREFUL, because you know... )\n\n\
2. If import a "txt" file, fill like this in "txt":\n' + 
   r'# adobe' + '\n' +
   r'C:\Program Files\Adobe' + '\n' +
   r"C:\Users\Administrator\AppData\Local\Adobe        # don't change this" + '\n' \
			, anchor = W)
		self.ARuleLabelDescription.pack(side = TOP, fill = X)
		
		self.ARuleScrollbarXPath.config( command = self.ARuleEntryPath.xview )
		# end up left Frame
		
		# start down left Frame
		self.ARuleFrameDownLeft = ttk.LabelFrame(self.ARuleRoot, text = r'Pending to add in firewall rules, repeat checking will be handled  ( NOTE: DO NOT ADD SYSTEM FILE )')
		self.ARuleFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.51, relheight = 0.48)
		
		self.ARuleScrollbarXDownFolders = ttk.Scrollbar(self.ARuleFrameDownLeft, orient = HORIZONTAL)
		self.ARuleScrollbarXDownFolders.pack( side = BOTTOM, fill = X )
		
		self.ARuleScrollbarYDownFolders = ttk.Scrollbar(self.ARuleFrameDownLeft, orient = VERTICAL)
		self.ARuleScrollbarYDownFolders.pack( side = RIGHT, fill = Y )
		
		self.ARuleTextDownFiles = Text(self.ARuleFrameDownLeft, font = self.ft, \
xscrollcommand = self.ARuleScrollbarXDownFolders.set, yscrollcommand = self.ARuleScrollbarYDownFolders.set, wrap = 'none')
		self.ARuleTextDownFiles.pack(fill = BOTH)
		
		self.ARuleScrollbarXDownFolders.config( command = self.ARuleTextDownFiles.xview )
		self.ARuleScrollbarYDownFolders.config( command = self.ARuleTextDownFiles.yview )
		# end down left Frame
		
		# start right frame
		self.ARuleFrameRight = ttk.LabelFrame(self.ARuleRoot, text = "")
		self.ARuleFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.ARuleButtonReset = ttk.Button(self.ARuleFrameRight, text = "Reset", command = self.ARuleReset) 
		self.ARuleButtonReset.pack(fill = X, side = TOP)

		self.ARuleLabelBlank = ttk.Label(self.ARuleFrameRight)
		self.ARuleLabelBlank.pack(side = TOP, fill = X)
		
		self.ARuleButtonAddDirection = ttk.Button(self.ARuleFrameRight, text = "Add txt", command = self.ARuleAddTxt) 
		self.ARuleButtonAddDirection.pack(fill = X, side = TOP)
		
		self.ARuleLabelBlank = ttk.Label(self.ARuleFrameRight)
		self.ARuleLabelBlank.pack(side = TOP, fill = X)
		
		self.ARuleButtonAddDirection = ttk.Button(self.ARuleFrameRight, text = "Add Direction", command = self.ARuleAddDirection) 
		self.ARuleButtonAddDirection.pack(fill = X, side = TOP)
		
		self.ARuleLabelBlank = ttk.Label(self.ARuleFrameRight)
		self.ARuleLabelBlank.pack(side = TOP, fill = X)

		self.ARuleLabelBlank = ttk.Label(self.ARuleFrameRight, text = 'Extension ( fill like: .exe )')
		self.ARuleLabelBlank.pack(side = TOP, fill = X)
				
		self.ARuleEntryExtension = ttk.Entry(self.ARuleFrameRight, font = self.ft)
		self.ARuleEntryExtension.pack(fill = X, side = TOP)

		self.ARuleButtonSearch = ttk.Button(self.ARuleFrameRight, text = "Search Files", command = self.ARuleSearchFiles) #bg = "#e1e1e1"
		self.ARuleButtonSearch.pack(side = TOP, fill = X)

		self.ARuleLabelBlank = ttk.Label(self.ARuleFrameRight)
		self.ARuleLabelBlank.pack(side = TOP, fill = X)
		
		self.ARuleCheckInVar = IntVar()
		self.ARuleCheckIn = ttk.Checkbutton(self.ARuleFrameRight, text = "Add to Inbound Rules", \
											variable = self.ARuleCheckInVar, onvalue = 1, offvalue = 0) 
		self.ARuleCheckIn.pack(fill = X, side = TOP)
		self.ARuleCheckInVar.set(0)

		self.ARuleCheckOutVar = IntVar()
		self.ARuleCheckOut = ttk.Checkbutton(self.ARuleFrameRight, text = "Add to Outbound Rules", \
											variable = self.ARuleCheckOutVar, onvalue = 1, offvalue = 0) 
		self.ARuleCheckOut.pack(fill = X, side = TOP)
		self.ARuleCheckOutVar.set(1)

		self.ARuleButtonAddRule = ttk.Button(self.ARuleFrameRight, text = "Add Rules", command = self.AddRule)
		self.ARuleButtonAddRule.pack(side = TOP, fill = X)		

		self.ARuleLabelBlank = ttk.Label(self.ARuleFrameRight)
		self.ARuleLabelBlank.pack(side = TOP, fill = X)

		self.ARuleButtonAddRule = ttk.Button(self.ARuleFrameRight, text = "Go to Firewall Advanced", command = self.fwl.open_window_firewall_advanced)
		self.ARuleButtonAddRule.pack(side = TOP, fill = X)	
		# end right frame



