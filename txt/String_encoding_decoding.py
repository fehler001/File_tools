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



class CreateFrameStr():

	def __init__(self):
		super().__init__()

		self.StrRoot = None

		self.StrTxtPath = ''
		self.StrSavePath = ''



	def StrDefault(self):

		self.StrDefaultLog()
		self.CreateWidgetsFrameStr()
		self.StrRestoreState()
		

	def StrDefaultLog(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j2 = copy.deepcopy(j)
		if not 'string' in j['file_tools']['txt']:
			j['file_tools']['txt']['string'] = {}
		if not 'path_txt' in j['file_tools']['txt']['string']:
			j['file_tools']['txt']['string']['path_txt'] = ''
		if not 'path_save' in j['file_tools']['txt']['string']:
			j['file_tools']['txt']['string']['path_save'] = ''
		if not 'combo_from' in j['file_tools']['txt']['string']:
			j['file_tools']['txt']['string']['combo_from'] = 'utf-8'
		if not 'combo_to' in j['file_tools']['txt']['string']:
			j['file_tools']['txt']['string']['combo_to'] = 'utf-8'
		if not 'check_binary' in j['file_tools']['txt']['string']:
			j['file_tools']['txt']['string']['check_binary'] = 1
		if j != j2:
			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()




	def StrRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.StrTxtPath = j['file_tools']['txt']['string']['path_txt']
		self.StrSavePath = j['file_tools']['txt']['string']['path_save']
		self.StrEntryTxtSource.insert(0, self.StrTxtPath)
		self.StrEntryTxtDestination.insert(0, self.StrSavePath )
		self.StrComboFrom.set(j['file_tools']['txt']['string']['combo_from'])
		self.StrComboTo.set(j['file_tools']['txt']['string']['combo_to'])
		self.StrCheckBinaryVar.set( j['file_tools']['txt']['string']['check_binary'] )
		f.close()


	

	def ReadStrPath(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		self.StrTxtPath = j['file_tools']['txt']['string']['path_txt']
		self.StrSavePath = j['file_tools']['txt']['string']['path_save']
		f.close()



	def StrSaveEntry(self):
		if self.EnableLog == 1:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			self.StrTxtPath = self.StrEntryTxtSource.get()
			j['file_tools']['txt']['string']['path_txt'] = self.StrTxtPath
			j['file_tools']['txt']['string']['path_save'] = self.StrEntryTxtDestination.get()
			j['file_tools']['txt']['string']['combo_from'] = self.StrComboFrom.get()
			j['file_tools']['txt']['string']['combo_to'] = self.StrComboTo.get()
			j['file_tools']['txt']['string']['check_binary'] = self.StrCheckBinaryVar.get()

			f = open(self.LogPath, 'w', encoding='utf-8')
			json.dump(j, f, ensure_ascii=False)
			f.close()



	def StrReset(self):
		self.StrEntryTxtSource.delete(0, "end")
		self.StrEntryTxtDestination.delete(0, "end")
		self.StrTextUp.delete("1.0", "end")
		self.StrTextDown.delete("1.0", "end")
		self.StrSaveEntry()
	


	def StrAddSource(self):
		self.ReadStrPath()
		p = self.StrTxtPath
		if os.path.isdir(p):
			dir = filedialog.askopenfilename(initialdir = p) 
		else:
			dir = filedialog.askopenfilename(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.StrEntryTxtSource.delete(0, "end")
			self.StrEntryTxtSource.insert(0, dir)
			self.StrTxtPath = dir
			dir.replace('\\', '/')
			savedir = dir[ :dir.rfind('/')]
			self.StrEntryTxtDestination.insert(0, savedir)
			self.StrSavePath = savedir
			self.StrSaveEntry()
		except:pass
	

	def StrAddDirection(self):
		self.ReadStrPath()
		p = self.StrSavePath
		if os.path.isdir(p):
			dir = filedialog.askdirectory(initialdir = p) 
		else:
			dir = filedialog.askdirectory(initialdir = p[0 : p.rfind(r'/')] ) 
		try: 
			if dir == '':
				return
			self.StrEntryTxtDestination.delete(0, "end")
			self.StrEntryTxtDestination.insert(0, dir)
			self.StrSavePath = dir
			self.StrSaveEntry()
		except:pass



	def StrReadClipboard(self):
		self.StrTextUp.delete("1.0", "end")
		self.StrTextUp.insert(INSERT, self.root.clipboard_get() )



	def StrCopyResult(self):
		self.root.clipboard_append( self.StrTextDown.get("1.0", "end") )
		


	def StrDownToUp(self):
		self.StrTextUp.delete("1.0", "end")
		down = self.StrTextDown.get("1.0", "end")
		self.StrTextUp.insert(INSERT, down)
		self.StrTextDown.delete("1.0", "end")



	def StrGuessTxt(self):
		self.StrSaveEntry()
		self.StrTextDown.delete("1.0", "end")
		src = self.StrTxtPath
		if not os.path.isfile(src):
			messagebox.showerror ("Warrning", "_____TXT SOURCE ERROR_____")
			return
		f = open(src, 'rb')
		str = f.read()
		enc = self.bl.guess_encoding_binary(str)
		self.StrTextDown.insert(INSERT, enc)
		self.StrTextDown.insert(INSERT, '\n\n')
		self.StrTextDown.insert(INSERT, "If encoding doesn't in \"To\", you can just type in it\n")


	def StrEncoding(self):
		self.StrSaveEntry()
		self.StrTextDown.delete("1.0", "end")
		enc_from = self.StrComboFrom.get()
		str_before = self.StrTextUp.get("1.0", "end")
		str_after = str( self.bl.str_encode(str_before, enc = enc_from) )
		if str_after == -1:
			self.StrTextDown.delete("1.0", "end")
			return
		self.StrTextDown.insert(INSERT, str_after)


	def StrDecoding(self):
		self.StrSaveEntry()
		self.StrTextDown.delete("1.0", "end")
		enc_to = self.StrComboTo.get()
		str_before = self.StrTextUp.get("1.0", "end").strip()
		str_after = self.bl.str_decode(str_before, enc = enc_to)
		str_after = str_after.strip()
		if str_after == -1:
			self.StrTextDown.delete("1.0", "end")
			return
		self.StrTextDown.insert(INSERT, str_after)


	def StrTranscoding(self):
		self.StrSaveEntry()
		self.StrTextDown.delete("1.0", "end")
		enc_from = self.StrComboFrom.get()
		enc_to = self.StrComboTo.get()
		str_before = self.StrTextUp.get("1.0", "end")
		str_after = self.bl.str_transcode(str_before, enc_from = enc_from, enc_to = enc_to)
		str_after = str_after.strip()
		if str_after == -1:
			self.StrTextDown.delete("1.0", "end")
			return
		self.StrTextDown.insert(INSERT, str_after)



	def StrTranscodingTxtPreview(self):
		self.StrTranscodingTxt(preview = True)

	def StrTranscodingTxt(self, preview = False):
		self.StrSaveEntry()
		enc_from = self.StrComboFrom.get()
		enc_to = self.StrComboTo.get()
		src = self.StrEntryTxtSource.get()
		src = src.replace('\\', '/')
		dst = self.StrEntryTxtDestination.get()
		dst = dst.replace('\\', '/')
		is_b = self.StrCheckBinaryVar.get()
		if not os.path.isfile(src):
			messagebox.showerror ("Warrning", "_____TXT SOURCE ERROR_____")
			return

		if preview == True:
			self.StrTextDown.delete("1.0", "end")
			if is_b == 1:
				f = open(src, 'rb')
				#cont = f.read(2000)
				cont = f.read()
				f.close()
				new_cont = self.bl.bytes_decode(cont, enc_to)
				self.StrTextDown.insert(INSERT, new_cont)
			else:
				f = open(src, 'r', encoding = enc_from, errors = 'backslashreplace')
				cont = f.read(2000)
				f.close()
				new_cont = self.bl.str_transcode(cont, enc_from, enc_to)
				self.StrTextDown.insert(INSERT, new_cont)
			return

		if not os.path.isdir(dst):
			messagebox.showerror ("Warrning", "_____PATH ERROR_____")
			return
		new_txt = dst + '/' + 'new' + src[ src.rfind('/') + 1 : ]
		if is_b == 1:
			f = open(src, 'rb')
			cont = f.read()
			f.close()
			new_cont = self.bl.bytes_decode(cont, enc = enc_to)
			f = open(new_txt, 'w', encoding = 'utf-8')
			f.write(new_cont)
		else:
			f = open(src, 'r', encoding = enc_from, errors = 'backslashreplace')
			cont = f.read()
			f.close()
			new_cont = self.bl.str_transcode(cont, enc_from = enc_from, enc_to = enc_to)
			f = open(new_txt, 'w', encoding = 'utf-8')
			f.write(new_cont)
		
		


	def StrEntryTxtSourceFocusOut(self, _):
		path = self.StrEntryTxtSource.get()
		if os.path.isfile(path):
			path2 = self.StrEntryTxtDestination.get()
			if path != '' and path2 == '':
				path = path.replace('\\', '/')
				path2 = path[ :path.rfind('/')]
				self.StrEntryTxtDestination.insert(0, path2)




	def CreateWidgetsFrameStr(self):

		# start up left Frame
		self.StrFrameUpLeft = ttk.LabelFrame(self.StrRoot, text = "")
		self.StrFrameUpLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.01, relheight = 0.28)

		# start Frame1
		self.StrFrame1 = ttk.Frame(self.StrFrameUpLeft)
		self.StrFrame1.pack(side = TOP, fill = X)

		self.StrScrollbarXTxtSource = ttk.Scrollbar(self.StrFrame1, orient = HORIZONTAL)
		self.StrScrollbarXTxtSource.pack( side = BOTTOM, fill = X )

		self.StrLabelTxtSource = ttk.Label(self.StrFrame1, text = "Txt Source Path", anchor = W)
		self.StrLabelTxtSource.pack(side = TOP, fill = X)
		
		self.StrEntryTxtSource = ttk.Entry(self.StrFrame1, font = self.ft, xscrollcommand = self.StrScrollbarXTxtSource.set)
		self.StrEntryTxtSource.pack(fill = X)
		self.StrEntryTxtSource.bind("<FocusOut>", self.StrEntryTxtSourceFocusOut)

		self.StrEntryTxtSource.drop_target_register(DND_FILES, DND_TEXT)
		self.StrEntryTxtSource.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.StrScrollbarXTxtSource.config( command = self.StrEntryTxtSource.xview )
		# end Frame1

		# start Frame2
		self.StrFrame2 = ttk.Frame(self.StrFrameUpLeft)
		self.StrFrame2.pack(side = TOP, fill = X)

		self.StrScrollbarXTxtDestination = ttk.Scrollbar(self.StrFrame2, orient = HORIZONTAL)
		self.StrScrollbarXTxtDestination.pack( side = BOTTOM, fill = X )

		self.StrLabelTxtDestination = ttk.Label(self.StrFrame2, text = "Txt Save Path", anchor = W)
		self.StrLabelTxtDestination.pack(side = TOP, fill = X)
		
		self.StrEntryTxtDestination = ttk.Entry(self.StrFrame2, font = self.ft, xscrollcommand = self.StrScrollbarXTxtDestination.set)
		self.StrEntryTxtDestination.pack(fill = X)

		self.StrEntryTxtDestination.drop_target_register(DND_FILES, DND_TEXT)
		self.StrEntryTxtDestination.dnd_bind('<<Drop>>', self.drop_in_entry)

		self.StrScrollbarXTxtDestination.config( command = self.StrEntryTxtDestination.xview )
		# end Frame2
		# end up left Frame
		
		# start down left Frame
		self.StrFrameDownLeft = ttk.Frame(self.StrRoot)
		self.StrFrameDownLeft.place(relx = 0.01, relwidth = 0.69, rely = 0.29, relheight = 0.70)
		
		# start down left frame 1
		self.StrFrameDownLeft_1 = ttk.LabelFrame(self.StrFrameDownLeft, text = r'Paste text here')
		self.StrFrameDownLeft_1.place(relx = 0.0, relwidth = 1.0, rely = 0.0, relheight = 0.5)

		self.StrScrollbarXUpText = ttk.Scrollbar(self.StrFrameDownLeft_1, orient = HORIZONTAL)
		self.StrScrollbarXUpText.pack( side = BOTTOM, fill = X )
		
		self.StrScrollbarYUpText = ttk.Scrollbar(self.StrFrameDownLeft_1, orient = VERTICAL)
		self.StrScrollbarYUpText.pack( side = RIGHT, fill = Y )
		
		self.StrTextUp = Text(self.StrFrameDownLeft_1, font = self.ft, xscrollcommand = self.StrScrollbarXUpText.set, yscrollcommand = self.StrScrollbarYUpText.set, wrap = 'none')
		self.StrTextUp.pack(fill = BOTH)
		
		self.StrScrollbarXUpText.config( command = self.StrTextUp.xview )
		self.StrScrollbarYUpText.config( command = self.StrTextUp.yview )
		# end down left frame 1

		# start down left frame 2
		self.StrFrameDownLeft_2 = ttk.LabelFrame(self.StrFrameDownLeft, text = r'Result')
		self.StrFrameDownLeft_2.place(relx = 0.0, relwidth = 1.0, rely = 0.5, relheight = 0.5)

		self.StrScrollbarXDownText = ttk.Scrollbar(self.StrFrameDownLeft_2, orient = HORIZONTAL)
		self.StrScrollbarXDownText.pack( side = BOTTOM, fill = X )
		
		self.StrScrollbarYDownText = ttk.Scrollbar(self.StrFrameDownLeft_2, orient = VERTICAL)
		self.StrScrollbarYDownText.pack( side = RIGHT, fill = Y )
		
		self.StrTextDown = Text(self.StrFrameDownLeft_2, font = self.ft, xscrollcommand = self.StrScrollbarXDownText.set, yscrollcommand = self.StrScrollbarYDownText.set, wrap = 'none')
		self.StrTextDown.pack(fill = BOTH)
		
		self.StrScrollbarXDownText.config( command = self.StrTextDown.xview )
		self.StrScrollbarYDownText.config( command = self.StrTextDown.yview )
		# end down left frame 2

		# end down left Frame
		
		# start right frame
		self.StrFrameRight = ttk.LabelFrame(self.StrRoot, text = "")
		self.StrFrameRight.place(relx = 0.7, relwidth = 0.29, rely = 0.01, relheight = 0.98)
		
		self.StrButtonReset = ttk.Button(self.StrFrameRight, text = "Reset", command = self.StrReset) 
		self.StrButtonReset.pack(fill = X, side = TOP)

		self.StrButtonSetSource = ttk.Button(self.StrFrameRight, text = "Add txt", command = self.StrAddSource) 
		self.StrButtonSetSource.pack(fill = X, side = TOP)

		self.StrButtonSetDestination = ttk.Button(self.StrFrameRight, text = "Set Save Path", command = self.StrAddDirection) 
		self.StrButtonSetDestination.pack(fill = X, side = TOP)

		self.StrLabelBlank = ttk.Label(self.StrFrameRight)
		self.StrLabelBlank.pack(side = TOP, fill = X)

		self.StrButtonGuessTxt = ttk.Button(self.StrFrameRight, text = "Guess Encoding", command = self.StrGuessTxt)
		self.StrButtonGuessTxt.pack(side = TOP, fill = X)

		self.StrLabelBlank = ttk.Label(self.StrFrameRight)
		self.StrLabelBlank.pack(side = TOP, fill = X)

		self.StrCheckBinaryVar = IntVar()
		self.StrCheckBinary = ttk.Checkbutton(self.StrFrameRight, text = 'Binary Mode ( results only affected by "To" )', \
											variable = self.StrCheckBinaryVar, onvalue = 1, offvalue = 0) 
		self.StrCheckBinary.pack(fill = X, side = TOP)
		self.StrCheckBinaryVar.set(0)
		
		self.StrButtonTranscodingTxt = ttk.Button(self.StrFrameRight, text = "Get Preview", command = self.StrTranscodingTxtPreview)
		self.StrButtonTranscodingTxt.pack(side = TOP, fill = X)

		self.StrLabelBlank = ttk.Label(self.StrFrameRight)
		self.StrLabelBlank.pack(side = TOP, fill = X)

		self.StrButtonTranscodingTxt = ttk.Button(self.StrFrameRight, text = "Transcode txt", command = self.StrTranscodingTxt)
		self.StrButtonTranscodingTxt.pack(side = TOP, fill = X)

		self.StrLabelBlank = ttk.Label(self.StrFrameRight, text = "From")
		self.StrLabelBlank.pack(side = TOP, fill = X)

		values = ('utf-8', 'utf-16', 'utf-32', 'raw_unicode_escape', 'unicode_escape', 'ascii', 
			'gb2312', 'big5', 'gbk', 'gb18030', 'shift-jis', 'shift_jis_2004', 'shift_jisx0213', 
			'', "transcode not supported below here", 'base64', 'html')
		enc = values + ('quote', 'hex', 'binary', 'ascii-hex', 'ord')
		dec = values + ('unquote', 'int', 'ascii-unhex', 'chr')

		self.StrComboFromVar = StringVar()
		self.StrComboFrom = ttk.Combobox(self.StrFrameRight, textvariable = self.StrComboFromVar)
		self.StrComboFrom["values"] = enc
		self.StrComboFrom.current(0) 
		self.StrComboFrom.pack(fill = X)
		#comboxlist.bind("<<ComboboxSelected>>", fun)   # when one item selected, fun()

		self.StrLabelBlank = ttk.Label(self.StrFrameRight, text = "To")
		self.StrLabelBlank.pack(side = TOP, fill = X)

		self.StrComboToVar = StringVar()
		self.StrComboTo = ttk.Combobox(self.StrFrameRight, textvariable = self.StrComboToVar)
		self.StrComboTo["values"] = dec
		self.StrComboTo.current(0) 
		self.StrComboTo.pack(fill = X)

		self.StrButtonTranscoding = ttk.Button(self.StrFrameRight, text = "Transcode", command = self.StrTranscoding)
		self.StrButtonTranscoding.pack(side = TOP, fill = X)

		self.StrButtonEncoding = ttk.Button(self.StrFrameRight, text = 'Encode ( only affected by "From" )', command = self.StrEncoding)
		self.StrButtonEncoding.pack(side = TOP, fill = X)

		self.StrButtonDecoding = ttk.Button(self.StrFrameRight, text = 'Decode ( only affected by "To" )', command = self.StrDecoding)
		self.StrButtonDecoding.pack(side = TOP, fill = X)

		self.StrLabelBlank = ttk.Label(self.StrFrameRight)
		self.StrLabelBlank.pack(side = TOP, fill = X)

		self.StrLabelBlank = ttk.Label(self.StrFrameRight)
		self.StrLabelBlank.pack(side = TOP, fill = X)

		self.StrButtonDownToUp = ttk.Button(self.StrFrameRight, text = "Read Clipboard to Up", command = self.StrReadClipboard)
		self.StrButtonDownToUp.pack(side = TOP, fill = X)

		self.StrLabelBlank = ttk.Label(self.StrFrameRight)
		self.StrLabelBlank.pack(side = TOP, fill = X)

		self.StrButtonDownToUp = ttk.Button(self.StrFrameRight, text = "Read Down to Up", command = self.StrDownToUp)
		self.StrButtonDownToUp.pack(side = TOP, fill = X)

		self.StrLabelBlank = ttk.Label(self.StrFrameRight)
		self.StrLabelBlank.pack(side = TOP, fill = X)

		self.StrButtonDownToUp = ttk.Button(self.StrFrameRight, text = "Copy Result", command = self.StrCopyResult)
		self.StrButtonDownToUp.pack(side = TOP, fill = X)
		# end right frame