#coding=utf-8
#File_tools/rar/Brute_force_crack.py

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
import subprocess
import time
import datetime
from multiprocessing import Pool


import tkinterdnd2 
from tkinterdnd2 import *



class CreateFrameBrute():

	def __init__(self):
		super().__init__()

		self.BruteRoot = None

		self.BruteRarPath = ''
		self.BruteUnrarPath = ''
		self.BruteDictPath = ''
		



	def BruteDefault(self):
		
		self.BruteDefaultLog()
		self.CreateWidgetsFrameBrute()
		self.BruteRestoreState()

		self.brute_stop = 0
		

	def BruteDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'brute' in j['file_tools']['rar']:
			j['file_tools']['rar']['brute'] = {}
		if not 'path_rar' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['path_rar'] = ''
		if not 'path_unrar' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['path_unrar'] = ''
		if not 'path_dict' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['path_dict'] = ''
		if not 'radio_rar' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['radio_rar'] = 'rar'
		if not 'entry_ii' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['entry_ii'] = 1000
		if not 'entry_feedback' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['entry_feedback'] = 1
		if not 'entry_ii0' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['entry_ii0'] = 100
		if not 'entry_outset' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['entry_outset'] = ''
		if not 'entry_core' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['entry_core'] = 1
		if not 'check_custom_dict' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['check_custom_dict'] = 0
		if not 'check_show_info' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['check_show_info'] = 0
		if not 'text_up' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['text_up'] = self.rl.dict
		if not 'text_down' in j['file_tools']['rar']['brute']:
			j['file_tools']['rar']['brute']['text_down'] = ''
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()




	def BruteRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.BruteRarPath = j['file_tools']['rar']['brute']['path_rar']
		self.BruteUnrarPath = j['file_tools']['rar']['brute']['path_unrar']
		self.BruteDictPath = j['file_tools']['rar']['brute']['path_dict']
		self.BruteEntryRarSource.insert(0, self.BruteRarPath)
		self.BruteEntryUnrar.insert(0, self.BruteUnrarPath)
		self.BruteEntryDictPath.insert(0, self.BruteDictPath )
		self.BruteRadioRarVar.set(  j['file_tools']['rar']['brute']['radio_rar'] )
		if self.BruteRadioRarVar.get() == 'rar':
			self.BruteRadioRar.invoke()
		else:
			self.BruteRadio7z.invoke()
		self.BruteEntryii.insert(0, j['file_tools']['rar']['brute']['entry_ii'] )
		self.BruteEntryFeedback.insert(0, j['file_tools']['rar']['brute']['entry_feedback'] )
		self.BruteEntryii0.insert(0, j['file_tools']['rar']['brute']['entry_ii0'] )
		self.BruteEntryOutset.insert(0, j['file_tools']['rar']['brute']['entry_outset'] )
		self.BruteEntryCore.insert(0, j['file_tools']['rar']['brute']['entry_core'] )
		self.BruteCheckCustomDictVar.set( j['file_tools']['rar']['brute']['check_custom_dict'] )
		self.BruteCheckShowInfoVar.set( j['file_tools']['rar']['brute']['check_show_info'] )
		self.BruteTextUp.insert(0, j['file_tools']['rar']['brute']['text_up'] )
		self.BruteTextDown.insert(INSERT, j['file_tools']['rar']['brute']['text_down'] )
		f.close()


	

	def ReadBrutePath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.BruteRarPath = j['file_tools']['rar']['brute']['path_rar']
		self.BruteUnrarPath = j['file_tools']['rar']['brute']['path_unrar']
		self.BruteDictPath = j['file_tools']['rar']['brute']['path_dict']
		f.close()



	def BruteSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j['file_tools']['rar']['brute']['path_rar'] = self.BruteEntryRarSource.get()
			j['file_tools']['rar']['brute']['path_unrar'] = self.BruteEntryUnrar.get()
			j['file_tools']['rar']['brute']['path_dict'] = self.BruteEntryDictPath.get()
			j['file_tools']['rar']['brute']['radio_rar'] = self.BruteRadioRarVar.get()
			j['file_tools']['rar']['brute']['entry_ii'] = self.BruteEntryii.get()
			j['file_tools']['rar']['brute']['entry_feedback'] = self.BruteEntryFeedback.get()
			j['file_tools']['rar']['brute']['entry_ii0'] = self.BruteEntryii0.get()
			j['file_tools']['rar']['brute']['entry_outset'] = self.BruteEntryOutset.get()
			j['file_tools']['rar']['brute']['entry_core'] = self.BruteEntryCore.get()
			j['file_tools']['rar']['brute']['check_custom_dict'] = self.BruteCheckCustomDictVar.get()
			j['file_tools']['rar']['brute']['check_show_info'] = self.BruteCheckShowInfoVar.get()
			j['file_tools']['rar']['brute']['text_up'] = self.BruteTextUp.get()
			td = self.BruteTextDown.get('1.0', 'end')
			if td[-1] == '\n':
				j['file_tools']['rar']['brute']['text_down'] = td[0:-1]
			else:
				j['file_tools']['rar']['brute']['text_down'] = td
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()


	def BruteReset(self):
		self.BruteEntryRarSource.delete(0, "end")
		self.BruteEntryUnrar.delete(0, "end")
		self.BruteEntryDictPath.delete(0, "end")
		self.BruteTextUp.delete(0, "end")
		self.BruteTextDown.delete("1.0", "end")
		self.BruteSaveEntry()
	


	def BruteAddSource(self):
		self.ReadBrutePath()
		p = self.BruteRarPath
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(initialdir = p) 
		else:
			dir = filedialog.askopenfilename(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.BruteEntryRarSource.delete(0, "end")
			self.BruteEntryRarSource.insert(0, dir)
			self.BruteRarPath = dir
			self.BruteSaveEntry()
		except:pass
	


	def BruteAddUnrar(self):
		self.ReadBrutePath()
		p = self.BruteUnrarPath
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(initialdir = p) 
		else:
			dir = filedialog.askopenfilename(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.BruteEntryUnrar.delete(0, "end")
			self.BruteEntryUnrar.insert(0, dir)
			self.BruteUnrarPath = dir
			self.BruteSaveEntry()
		except:pass



	def BruteAddDict(self):
		self.ReadBrutePath()
		p = self.BruteDictPath
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(initialdir = p) 
		else:
			dir = filedialog.askopenfilename(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.BruteEntryDictPath.delete(0, "end")
			self.BruteEntryDictPath.insert(0, dir)
			self.BruteDictPath = dir
			self.BruteSaveEntry()
		except:pass



	def BruteRestoreDefaultDict(self):
		self.BruteTextUp.delete(0, "end")
		self.BruteTextUp.insert(0, self.rl.dict)



	def BruteCrack(self):
		self.BruteSaveEntry()
		rar = self.BruteEntryRarSource.get()
		rar = rar.replace('\\', '/')
		unrar = self.BruteEntryUnrar.get()
		unrar = unrar.replace('\\', '/')
		dict = self.BruteEntryDictPath.get()
		dict = dict.replace('\\', '/')
		is_rar = self.BruteRadioRarVar.get()
		ii = self.BruteEntryii.get()
		if self.bl.check_legit_int(ii) == -1:
			return
		ii = int(ii)
		ii0 = self.BruteEntryii0.get()
		if self.bl.check_legit_int(ii0) == -1:
			return
		ii0 = int(ii0)
		fi = self.BruteEntryFeedback.get()
		if self.bl.check_legit_int(fi) == -1:
			return
		fi = int(fi)
		outset = self.BruteEntryOutset.get()
		core = self.BruteEntryCore.get()
		if self.bl.check_legit_int(core) == -1:
			return
		core = int(core)
		is_custom = self.BruteCheckCustomDictVar.get()
		is_show_info = self.BruteCheckShowInfoVar.get()
		if not os.path.isfile(rar):
			messagebox.showerror ("Warrning", "_____RAR FILE NOT EXIST_____")
			return
		if not os.path.isfile(unrar):
			messagebox.showerror ("Warrning", "_____UnRAR.exe or 7z.exe NOT EXIST_____")
			return
		if is_custom == 1:
			if not os.path.isfile(dict):
				messagebox.showerror ("Warrning", "_____DICT FILE NOT EXIST_____")
				return
		if is_custom == 0 and is_rar == '7z':
			messagebox.showerror ("Warrning", 'Due to there is some unknows bugs in "7z.exe"\n\n\"7z" should only be used in custom dict mode')
			return
		p_info = self.bl.get_path_info(rar)
		if p_info['ext'] != '.rar' and is_rar == 'rar':
			if p_info['ext'] != '.r':
				messagebox.showerror ("Warrning", 'Not a "rar" file')
				return
		if p_info['ext'] != '.7z' and is_rar == '7z':
			messagebox.showerror ("Warrning", 'Not a "7z" file')
			return
		if p_info['ext'] != '.zip' and is_rar == 'zip':
			messagebox.showerror ("Warrning", 'Not a "zip" file')
			return

		dir = rar[ 0 : rar.rfind(r'/') + 1 ] 
		
		if is_custom == 1:
			try:
				f = open(dict, 'r', encoding = 'utf-8')
			except:
				messagebox.showerror ("Warrning", "Need a utf-8 dict file")
				return
			d = f.read()
			f.close()
			d = d[1: ]   # utf-8 file get a '\u' at first
			d = d.split('\n')
		else:		#  is_custom == 0
			d = self.BruteTextUp.get()

		if d == '':
			messagebox.showerror ("Warrning", "_____DICT ERROR_____")
			return

		if outset != '':
			if is_custom == 0:
				for c in outset:
					if c not in d:
						messagebox.showerror ("Warrning", 'Crack Start From: "' + c + '" not exist in dict')
						return
			else:
				if outset not in d:
					messagebox.showerror ("Warrning", 'Crack Start From: "' + outset + '" not exist in dict')
					return
		else:
			outset = d[0]
			self.BruteEntryOutset.insert(0, outset)

		self.BruteTextDown.delete("1.0", "end")
		
		pa = outset
		if is_custom == 1:
			ii = len(d)
		for i in range(ii):
			p = Pool(core)
			p.daemon = True
			for i2 in range(core):
				password = pa
				pa, newpara = self.rl.unrar_brute_get_parameter(rar = rar, 
													dir = dir, unrar = unrar, dict = d, outset = pa, ii0 = ii0, is_custom_dict = is_custom, is_rar = is_rar)
				if is_rar == 'zip':
						continue
				if is_show_info == 0:
					p.apply_async( self.rl.unrar_brute_run, args = (newpara,) )
					pass
				else:
					r, output = self.rl.unrar_brute_run_show_info(newpara)
					if r == 0:
						self.BruteTextDown.insert('1.0', '\n')
						self.BruteTextDown.insert('1.0', 'Extracting...\nPassword: ' + password)
						return
					if output == -1:
						return
					self.BruteTextDown.insert('1.0', '\n')
					self.BruteTextDown.insert('1.0', r)
					self.BruteTextDown.insert('1.0', '\n')
					self.BruteTextDown.insert('1.0', output)
					self.root.update()
			p.close()
			p.join()
			if (i+1) % fi == 0:
				self.BruteTextDown.insert('1.0', '\n')
				self.BruteTextDown.insert('1.0', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + 'big loop' + str(i+1) + ':' + pa)
			self.root.update()
			if self.brute_stop == 1:
				self.brute_stop = 0
				return
		self.BruteTextDown.insert('1.0', '\n')
		self.BruteTextDown.insert('1.0', 'big loop: ' + str(i+1) + '\n' + 'You can fill this in "Crack Start From":' + pa)



	def BruteStop(self):
		self.brute_stop = 1



	def BruteRadioRarToggle(self):
		pass


	def CreateWidgetsFrameBrute(self):

		# start up left Frame
		self.BruteFrameUpLeft = ttk.LabelFrame(self.BruteRoot, text = "Windows Only")
		self.BruteFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.46)

		# start Frame1
		self.BruteFrame1 = ttk.Frame(self.BruteFrameUpLeft)
		self.BruteFrame1.pack(side = TOP, fill = X)

		self.BruteScrollbarXRarSource = ttk.Scrollbar(self.BruteFrame1, orient = HORIZONTAL)
		self.BruteScrollbarXRarSource.pack( side = BOTTOM, fill = X )

		self.BruteLabelRarSource = ttk.Label(self.BruteFrame1, text = "rar or 7z file Path ( the shorter path is, the faster running speed you get )", anchor = W)
		self.BruteLabelRarSource.pack(side = TOP, fill = X)
		
		self.BruteEntryRarSource = ttk.Entry(self.BruteFrame1, font = self.ft, xscrollcommand = self.BruteScrollbarXRarSource.set)
		self.BruteEntryRarSource.pack(fill = X)

		self.BruteEntryRarSource.drop_target_register(DND_FILES, DND_TEXT)
		self.BruteEntryRarSource.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.BruteScrollbarXRarSource.config( command = self.BruteEntryRarSource.xview )
		# end Frame1

		# start Frame3
		self.BruteFrame3 = ttk.Frame(self.BruteFrameUpLeft)
		self.BruteFrame3.pack(side = TOP, fill = X)

		self.BruteScrollbarXUnrar = ttk.Scrollbar(self.BruteFrame3, orient = HORIZONTAL)
		self.BruteScrollbarXUnrar.pack( side = BOTTOM, fill = X )

		self.BruteLabelUnrar = ttk.Label(self.BruteFrame3, text = "UnRAR.exe or 7z.exe Path ( the shorter path is, the bigger insider loop you could set )", anchor = W)
		self.BruteLabelUnrar.pack(side = TOP, fill = X)
							   
		self.BruteEntryUnrar = ttk.Entry(self.BruteFrame3, font = self.ft, xscrollcommand = self.BruteScrollbarXUnrar.set)
		self.BruteEntryUnrar.pack(fill = X)
							   
		self.BruteEntryUnrar.drop_target_register(DND_FILES, DND_TEXT)
		self.BruteEntryUnrar.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.BruteScrollbarXUnrar.config( command = self.BruteEntryUnrar.xview )
		# end Frame3

		# start Frame2
		self.BruteFrame2 = ttk.Frame(self.BruteFrameUpLeft)
		self.BruteFrame2.pack(side = TOP, fill = X)

		self.BruteScrollbarXDictPath = ttk.Scrollbar(self.BruteFrame2, orient = HORIZONTAL)
		self.BruteScrollbarXDictPath.pack( side = BOTTOM, fill = X )

		self.BruteLabelDictPath = ttk.Label(self.BruteFrame2, text = 'dict Path  ( fill in dict like this: line1"123456", line2"password", ...... , every line will only be tried by once )', anchor = W)
		self.BruteLabelDictPath.pack(side = TOP, fill = X)
		
		self.BruteEntryDictPath = ttk.Entry(self.BruteFrame2, font = self.ft, xscrollcommand = self.BruteScrollbarXDictPath.set)
		self.BruteEntryDictPath.pack(fill = X)

		self.BruteEntryDictPath.drop_target_register(DND_FILES, DND_TEXT)
		self.BruteEntryDictPath.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.BruteScrollbarXDictPath.config( command = self.BruteEntryDictPath.xview )
		# end Frame2

		self.BruteLabelDescription = ttk.Label(self.BruteFrameUpLeft, text = '\
If not using custom dict, do not set path with "space" and with the exception of "a-Z0-9"\n\
Set rar or 7z file to "d:/1.r" or "d:/1.7z", "UnRAR.exe" to "d:/u.exe" can increase running speed to max\n\
To get "UnRAR.exe", go to "https://www.rarlab.com/rar_add.htm", download "UnRAR for Windows"\n\
\
			', anchor = W)
		self.BruteLabelDescription.pack(side = TOP, fill = X, pady = 5)
		# end up left Frame
		
		# start down left Frame
		self.BruteFrameDownLeft = ttk.Frame(self.BruteRoot)
		self.BruteFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.47, relheight = 0.52)
		
		# start down left frame 1
		self.BruteFrameDownLeft_1 = ttk.LabelFrame(self.BruteFrameDownLeft, text = r'Default dict ( Being used by brute force crack, could be modified )')
		self.BruteFrameDownLeft_1.place(relx = 0.0, relwidth = 1.0, rely = 0.0, relheight = 0.20)

		self.BruteScrollbarXUpText = ttk.Scrollbar(self.BruteFrameDownLeft_1, orient = HORIZONTAL)
		self.BruteScrollbarXUpText.pack( side = BOTTOM, fill = X )
				
		self.BruteTextUp = ttk.Entry(self.BruteFrameDownLeft_1, font = self.ft, xscrollcommand = self.BruteScrollbarXUpText.set)
		self.BruteTextUp.pack(fill = BOTH)
		
		self.BruteScrollbarXUpText.config( command = self.BruteTextUp.xview )
		# end down left frame 1

		# start down left frame 2
		self.BruteFrameDownLeft_2 = ttk.LabelFrame(self.BruteFrameDownLeft, text = r'Progress ( where big loop proceeded, could be fill in "Crack Start From" and crack next time )')
		self.BruteFrameDownLeft_2.place(relx = 0.0, relwidth = 1.0, rely = 0.25, relheight = 0.75)

		self.BruteScrollbarXDownText = ttk.Scrollbar(self.BruteFrameDownLeft_2, orient = HORIZONTAL)
		self.BruteScrollbarXDownText.pack( side = BOTTOM, fill = X )
		
		self.BruteScrollbarYDownText = ttk.Scrollbar(self.BruteFrameDownLeft_2, orient = VERTICAL)
		self.BruteScrollbarYDownText.pack( side = RIGHT, fill = Y )
		
		self.BruteTextDown = Text(self.BruteFrameDownLeft_2, font = self.ft, xscrollcommand = self.BruteScrollbarXDownText.set, yscrollcommand = self.BruteScrollbarYDownText.set, wrap = 'none')
		self.BruteTextDown.pack(fill = BOTH)
		
		self.BruteScrollbarXDownText.config( command = self.BruteTextDown.xview )
		self.BruteScrollbarYDownText.config( command = self.BruteTextDown.yview )
		# end down left frame 2

		# end down left Frame
		
		# start right frame
		self.BruteFrameRight = ttk.LabelFrame(self.BruteRoot, text = "")
		self.BruteFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.BruteButtonReset = ttk.Button(self.BruteFrameRight, text = "Reset", command = self.BruteReset) 
		self.BruteButtonReset.pack(fill = X, side = TOP)

		self.BruteButtonSetSource = ttk.Button(self.BruteFrameRight, text = "add rar or 7z file", command = self.BruteAddSource) 
		self.BruteButtonSetSource.pack(fill = X, side = TOP)

		self.BruteButtonSetSource = ttk.Button(self.BruteFrameRight, text = "set UnRAR.exe or 7z.exe Path", command = self.BruteAddUnrar) 
		self.BruteButtonSetSource.pack(fill = X, side = TOP)

		self.BruteButtonSetDict = ttk.Button(self.BruteFrameRight, text = "Set dict Path", command = self.BruteAddDict) 
		self.BruteButtonSetDict.pack(fill = X, side = TOP)

		self.BruteRadioRarVar = StringVar()
		self.BruteRadioRar = ttk.Radiobutton(self.BruteFrameRight, text = 'rar  ', variable = self.BruteRadioRarVar, value = 'rar',
									   command = self.BruteRadioRarToggle)
		self.BruteRadioRar.pack(fill = X, side = TOP)
		self.BruteRadioRar.invoke()

		self.BruteRadioZip = ttk.Radiobutton(self.BruteFrameRight, text = "zip  ( doesn't need external tool, but very slow )", variable = self.BruteRadioRarVar, value = 'zip',
									  command = self.BruteRadioRarToggle)
		self.BruteRadioZip.pack(fill = X, side = TOP)

		self.BruteRadio7z = ttk.Radiobutton(self.BruteFrameRight, text = "7z   ( should only be used in custom dict mode )", variable = self.BruteRadioRarVar, value = '7z',
									  command = self.BruteRadioRarToggle)
		self.BruteRadio7z.pack(fill = X, side = TOP)

		self.BruteLabelii = ttk.Label(self.BruteFrameRight, text = "Big Loop", anchor = W)
		self.BruteLabelii.pack(side = TOP, fill = X)
		
		self.BruteEntryii = ttk.Entry(self.BruteFrameRight, font = self.ft)
		self.BruteEntryii.pack(fill = X)

		self.BruteLabelFeedback = ttk.Label(self.BruteFrameRight, text = "Feedback Interval ( number of big loops )", anchor = W)
		self.BruteLabelFeedback.pack(side = TOP, fill = X)
		
		self.BruteEntryFeedback = ttk.Entry(self.BruteFrameRight, font = self.ft)
		self.BruteEntryFeedback.pack(fill = X)


		self.BruteLabelBlank = ttk.Label(self.BruteFrameRight)
		self.BruteLabelBlank.pack(side = TOP, fill = X)

		self.BruteLabelii0 = ttk.Label(self.BruteFrameRight, text = "Inside Loop ( loop inside big loop, set 1 - 250 )", anchor = W)
		self.BruteLabelii0.pack(side = TOP, fill = X)

		self.BruteLabelii0 = ttk.Label(self.BruteFrameRight, text = '( use "Show Info" to see how much you could set )', anchor = W)
		self.BruteLabelii0.pack(side = TOP, fill = X)

		self.BruteEntryii0 = ttk.Entry(self.BruteFrameRight, font = self.ft)
		self.BruteEntryii0.pack(fill = X)	

		self.BruteLabelBlank = ttk.Label(self.BruteFrameRight)
		self.BruteLabelBlank.pack(side = TOP, fill = X)

		self.BruteLabelOutset = ttk.Label(self.BruteFrameRight, text = "Crack Start From ( if ascii, 'a' or '1000a' or other )", anchor = W)
		self.BruteLabelOutset.pack(side = TOP, fill = X)
							   
		self.BruteEntryOutset = ttk.Entry(self.BruteFrameRight, font = self.ft)
		self.BruteEntryOutset.pack(fill = X)

		self.BruteButtonRestoreDefault = ttk.Button(self.BruteFrameRight, text = "Restore Default dict", command = self.BruteRestoreDefaultDict)
		self.BruteButtonRestoreDefault.pack(side = TOP, fill = X)

		self.BruteLabelCore = ttk.Label(self.BruteFrameRight, text = "Number of Cores ( set max could be harm for cpu )", anchor = W)
		self.BruteLabelCore.pack(side = TOP, fill = X)
							   
		self.BruteEntryCore = ttk.Entry(self.BruteFrameRight, font = self.ft)
		self.BruteEntryCore.pack(fill = X)

		self.BruteCheckCustomDictVar = IntVar()
		self.BruteCheckCustomDict = ttk.Checkbutton(self.BruteFrameRight, text = 'Using Custom dict ( set dict path first )', \
											variable = self.BruteCheckCustomDictVar, onvalue = 1, offvalue = 0) 
		self.BruteCheckCustomDict.pack(fill = X, side = TOP)
		self.BruteCheckCustomDictVar.set(0)

		self.BruteCheckShowInfoVar = IntVar()
		self.BruteCheckShowInfo = ttk.Checkbutton(self.BruteFrameRight, text = 'Show Info ( uncheck to greatly increase speed )', \
												variable = self.BruteCheckShowInfoVar, onvalue = 1, offvalue = 0) 
		self.BruteCheckShowInfo.pack(fill = X, side = TOP)
		self.BruteCheckShowInfoVar.set(0)
		
		self.BruteButtonCrack = ttk.Button(self.BruteFrameRight, text = "Start Crack", command = self.BruteCrack)
		self.BruteButtonCrack.pack(side = TOP, fill = X)

		self.BruteLabelBlank = ttk.Label(self.BruteFrameRight)
		self.BruteLabelBlank.pack(side = TOP, fill = X)

		self.BruteButtonStop = ttk.Button(self.BruteFrameRight, text = "Stop ( fiercely click me )", command = self.BruteStop)
		self.BruteButtonStop.pack(side = TOP, fill = X)

		# end right frame