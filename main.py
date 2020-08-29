#coding=utf-8
#File_tools/main.py

# if you use linux, don't put folder "FIle_tools" into anyplace under "~/home/"
# just create a new folder like "/a" and put in it would be ok

import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog 
from tkinter.font import Font, nametofont

import os
import sys
import stat
import shutil
import json
import copy
import multiprocessing
from multiprocessing import *
from multiprocessing import Pool

import file
import txt
import firewall
import rar

import zz


import lib.baselib
import lib.filelib
import lib.txtlib
import lib.firewalllib
import lib.rarlib

import traceback
import logging

# third party package must also be import in main if using pyinstaller
import chardet
import natsort
from natsort import natsort_keygen, ns
import crcmod

#project_dir=os.path.dirname(__file__)
#sys.path.append(project_dir)  
#sys.path.append(project_dir+'/'+'tkinterdnd2')  
import tkinterdnd2 
from tkinterdnd2 import *
# appending this in command if using pyinstaller 
# --add-data "D:/python/File_tools/tkinterdnd2";"tkinterdnd2/"





class Share():
	def __init__(self):
		super().__init__()

		self.RootWidth = 1000
		self.RootHeight = 615
		if os.name == 'nt':
			self.LogPath = r"C:\temp\File_tools.json"
			self.LogPathBackup = r'C:\Windows\Temp\File_tools_backup.json'
		else:
			self.LogPath = r"/temp/File_tools.json"
			self.LogPathBackup = r'/temp/File_tools_backup.json'

		self.IsFirstTimeOpen = 1
		self.firewall_add_rules_savefile = r'firewall_add_rules_savefile.txt'
		self.EnableLog = 1
		self.CheckPathExist = 1
		self.AdvancedMode = 0

		self.bl = lib.baselib.BaseLib()
		self.fl = lib.filelib.FileLib()
		self.tl = lib.txtlib.TxtLib()
		self.fwl = lib.firewalllib.FirewallLib()
		self.rl = lib.rarlib.RarLib()

		self.natsort_key1 = natsort_keygen(key=lambda y: y.lower())   # l1.sort(key=self.natsort_key1)  # lower means lowerCase -> upperCase
		self.natsort_key2 = natsort_keygen(alg=ns.IGNORECASE)         # l2.sort(key=self.natsort_key2)	



class FileTools(Share, file.File, txt.Txt, firewall.Firewall, rar.Rar, zz.Zz):

	def __init__(self):
		super().__init__()


	def drop_in_text(self, event):
		if event.data:
			files = event.widget.tk.splitlist(event.data)
			for f in files:
				if os.path.exists(f):
					event.widget.insert(INSERT, f)
					event.widget.insert(INSERT, '\n')
		if event.widget == self.RenameTextUpFiles:
			self.RenameCheckRepeatUp()
		return event.action

	def drop_in_entry(self, event):
		if event.data:
			files = event.widget.tk.splitlist(event.data)
			for f in files:
				if os.path.exists(f):
					event.widget.delete(0, 'end')
					event.widget.insert(0, f)	
				break
		return event.action



	def MainDefault(self):
		self.FileToolsDefaultLog()
		self.CreateWidgetsFileTools()
		self.MainRestoreState()

		self.root.geometry(str(self.RootWidth) + 'x' + str(self.RootHeight))



	def FileToolsDefaultLog(self, recur = 0):
		if not os.path.exists(self.LogPath):
			if not os.path.exists( os.path.dirname(self.LogPath) ):
				os.makedirs( os.path.dirname(self.LogPath) )
			f = open(self.LogPath, 'w', encoding='utf-8')
			j = {'file_tools':{} }
			json.dump(j, f, ensure_ascii=False)
			f.close()
		try:
			f = open(self.LogPath, 'r', encoding='utf-8')
			j = json.load(f)
			f.close()
			j2 = copy.deepcopy(j)
			if not 'file_tools' in j:
				j['file_tools'] = {}
			if not 'window' in j['file_tools']:
				j['file_tools']['window'] = {}
			if not 'width' in j['file_tools']['window']:
				j['file_tools']['window']['width'] = self.RootWidth
			if not 'height' in j['file_tools']['window']:
				j['file_tools']['window']['height'] = self.RootHeight
			if not 'menu' in j['file_tools']:
				j['file_tools']['menu'] = {}
			if not 'rename' in j['file_tools']['menu']:
				j['file_tools']['menu']['rename'] = {}
			if not 'check_path' in j['file_tools']['menu']['rename']:
				j['file_tools']['menu']['rename']['check_path'] = 1
			if not 'log' in j['file_tools']['menu']:
				j['file_tools']['menu']['log'] = {}
			if not 'is_first_time_open' in j['file_tools']['menu']['log']:
				j['file_tools']['menu']['log']['is_first_time_open'] = 1
			if not 'enable_log' in j['file_tools']['menu']['log']:
				j['file_tools']['menu']['log']['enable_log'] = 1
			if not 'notebook' in j['file_tools']:
				j['file_tools']['notebook'] = {}
			if not 'notebook01' in j['file_tools']['notebook']:
				j['file_tools']['notebook']['notebook01'] = {}
			if not 'current_index' in j['file_tools']['notebook']['notebook01']:
				j['file_tools']['notebook']['notebook01']['current_index'] = 0
			if not 'file' in j['file_tools']:
				j['file_tools']['file'] = {}
			if not 'txt' in j['file_tools']:
				j['file_tools']['txt'] = {}
			if not 'firewall' in j['file_tools']:
				j['file_tools']['firewall'] = {}
			if not 'rar' in j['file_tools']:
				j['file_tools']['rar'] = {}
			if not 'zz' in j['file_tools']:
				j['file_tools']['zz'] = {}
			if j != j2:
				f = open(self.LogPath, 'w', encoding='utf-8')
				json.dump(j, f, ensure_ascii=False)
				f.close()
		except:
			try:
				if os.path.isfile(self.LogPath):
					os.chmod(self.LogPath, stat.S_IRWXU)
					os.unlink(self.LogPath)
			except:
				messagebox.showerror ("ERROR", 'Some program is using \n"' + self.LogPath + '" \nPlease delete it by hand and restart')
				return
		else:
			if recur == 0:
				self.FileToolsDefaultLog(recur = 1)



	def MainRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		self.RootWidth = j['file_tools']['window']['width']
		self.RootHeight = j['file_tools']['window']['height']
		self.IsFirstTimeOpen = j['file_tools']['menu']['log']['is_first_time_open']
		self.EnableLog = j['file_tools']['menu']['log']['enable_log']
		self.EnableLogVar.set(self.EnableLog)
		self.CheckPathExist = j['file_tools']['menu']['rename']['check_path']
		self.CheckPathExistVar.set(self.CheckPathExist)

		if self.IsFirstTimeOpen == 1:
			tmp = messagebox.askquestion("Warning", "Please read carefully !\n\n" + 
			"This application could cause your files or folders CHAOS or DISAPPEAR\n\n" +
			"Will you take all responsibility by yourself ?")
			if tmp == 'no':
				sys.exit()


	def MainRestoreState2(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		self.NoteBook01.select(j['file_tools']['notebook']['notebook01']['current_index'])

		



	def MainSaveEntry(self):
		self.FileToolsDefaultLog()
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		j['file_tools']['menu']['log']['is_first_time_open'] = self.IsFirstTimeOpen
		j['file_tools']['menu']['log']['enable_log'] = self.EnableLogVar.get()
		j['file_tools']['menu']['rename']['check_path'] = self.CheckPathExistVar.get()
		j['file_tools']['window']['width'] = self.root.winfo_width()
		j['file_tools']['window']['height'] = self.root.winfo_height()
		j['file_tools']['notebook']['notebook01']['current_index'] = self.NoteBook01.index(self.NoteBook01.select())
		f = open(self.LogPath, 'w', encoding='utf-8')
		json.dump(j, f, ensure_ascii=False)
		f.close()



	def toggle_check_path_exist(self):
		self.CheckPathExist = self.CheckPathExistVar.get()
		self.update_rename_state()
		self.SaveAll(exit = 0)



	def toggle_advanced_mode(self):
		self.AdvancedMode = self.AdvancedModeVar.get()
		if self.AdvancedMode == 1:
			tmp = messagebox.askquestion("Warning", "In Advanced Mode:\n\n" + 
			'When using "Replace", instead of filename, you are dealing with the full path\n\n' +
			"Any tiny mistake could cause your file end up NOWHERE or EVERYWHERE !\n\n" + 
			'Plus: Path validity will not be checked')
			if tmp == 'no':
				self.AdvancedModeVar.set(0)
				self.AdvancedMode = self.AdvancedModeVar.get()
		self.update_rename_state()
		self.SaveAll(exit = 0)


	def update_rename_state(self):
		text_results = 'Results'
		if self.CheckPathExist == 0:
			text_results = text_results + '   ( "Check Path Exists" is OFF )' 
		if self.AdvancedMode == 1:
			text_results = text_results + '   ( "Advanced Mode" is On )' 
		self.RenameFrameDownLeft.config(text = text_results )


	def toggle_log(self):
		self.EnableLog = self.EnableLogVar.get()
		self.SaveAll(exit = 0)


	def init_log(self):
		try:
			if os.path.isfile(self.LogPath):
				os.chmod(self.LogPath, stat.S_IRWXU)
				os.unlink(self.LogPath)
		except:
			pass
		self.restart()



	def help(self):
		#print(StockText.TextUpTemp)
		self.help = Toplevel(self.root)
		self.help.geometry('860x240')
		self.help.title("")
		self.LabelHelp = ttk.Label(self.help, text = 
#'\n' +
'log path: ' + self.LogPath + '\n\n' + 
'Advanced Mode: Dealing with full path ( only works with "Replace" ) \n\n' +
'Check Path Exist: When ON, every "Rename" proccess will check whether every line is a real file or folder \n\n' + 
'You can not name file or folder with these words, e.g. "con", "CON", "Con", "con.txt"\n' + str(self.bl.filename_forbidden_windows)[1:-1] + '\n\n'
'Clear Cache: Only works in windows, when you feel something wrong, try this \n\n' +
'If any text got garbled, log will not be handled correctly'

			     , anchor = 'nw')
		self.LabelHelp.place(relx = 0, relwidth = 1, rely = 0, relheight = 1)
		#print(temp)


	def about(self):
		self.about = Toplevel(self.root)
		self.about.geometry('340x100')
		self.about.title("")
		self.LabelAbout = ttk.Label(self.about, text=
#'\n' +
'Github: https://github.com/fehler001/File_tools\n\n' +
'GPL-3.0 Lisence\n\n' + 
"File tools Ver 0.34        Author  tgbxs\n\n"
		, anchor = 'w')
		self.LabelAbout.place(relx = 0, relwidth = 1, rely = 0, relheight = 1)


	def SaveAll(self, exit = 1):
		self.IsFirstTimeOpen = 0
		try:
			if os.path.isfile(self.LogPath):
				shutil.copy2(self.LogPath, self.LogPathBackup)

			self.MainSaveEntry()

			self.RenameSaveEntry()
			self.RefineSaveEntry()
			self.RemoveSaveEntry()
			self.FilterSaveEntry()
			self.FindSaveEntry()
			self.MoveSaveEntry()
			self.DateSaveEntry()
			self.CsumSaveEntry()
			
			self.CleanSaveEntry()
			self.DivideSaveEntry()
			self.StrSaveEntry()
			self.MatchSaveEntry()

			self.ARuleSaveEntry()

			self.BruteSaveEntry()

			try:
				self.Z1SaveEntry()
			except:
				pass

		except:
			if os.path.isfile(self.LogPathBackup):
				shutil.copy2(self.LogPathBackup, self.LogPath)
				os.unlink(self.LogPathBackup)

		if os.path.isfile(self.LogPathBackup):
				os.unlink(self.LogPathBackup)
		
		if exit == 0:
			return
		sys.exit()


	def CreateWidgetsFileTools(self):
		
		self.root = Tk()
		#default_font = nametofont("TkDefaultFont") # must under self.root = Tk() # change default font
		#default_font.configure(family='Microsoft YaHei', size = 20)
		#self.root.option_add(ft, default_font)
		if os.name == 'nt':
			self.ft = Font(family = 'Microsoft YaHei', size = 10)
		else:
			self.ft = Font(family = 'xxxxxxxxxxxxxx', size = 10)
		self.root.title("File Tools")
		
		#self.root.geometry(str(self.RootWidth) + 'x' + str(self.RootHeight))
		
		# start menu
		self.menubar = Menu(self.root)

		self.filemenu = Menu(self.menubar, tearoff = 0)
		#filemenu.add_command ( label = "AddFiles", command = AddFiles )
		#filemenu.add_separator()
		self.filemenu.add_command ( label = "Exit", command = self.SaveAll )
		self.menubar.add_cascade(label = "File", menu = self.filemenu)

		self.logmenu = Menu(self.menubar, tearoff = 0)
		self.EnableLogVar = IntVar()
		self.logmenu.add_checkbutton( label = "Enable Log", \
			variable = self.EnableLogVar, onvalue = 1, offvalue = 0, command = self.toggle_log )
		self.logmenu.add_command ( label = "Initialize Log and Restart", command = self.init_log )
		self.menubar.add_cascade( label = "Log", menu = self.logmenu)

		self.renamemenu = Menu(self.menubar, tearoff = 0)
		self.CheckPathExistVar = IntVar()
		self.renamemenu.add_checkbutton( label = "Check Path Exist", \
			variable = self.CheckPathExistVar, onvalue = 1, offvalue = 0, command = self.toggle_check_path_exist )
		self.AdvancedModeVar = IntVar()
		self.renamemenu.add_checkbutton( label = "Advanced Mode", \
			variable = self.AdvancedModeVar, onvalue = 1, offvalue = 0, command = self.toggle_advanced_mode )
		self.menubar.add_cascade( label = "Rename", menu = self.renamemenu)

		self.cachemenu = Menu(self.menubar, tearoff = 0)
		self.cachemenu.add_command ( label = "Clear Cache", command = self.fl.clear_windows_cache )
		self.menubar.add_cascade(label = "Cache", menu = self.cachemenu)
		
		self.helpmenu = Menu(self.menubar, tearoff = 0)
		self.helpmenu.add_command ( label = "Help", command = self.help )
		self.helpmenu.add_command ( label = "About", command = self.about )
		self.menubar.add_cascade( label = "Help", menu = self.helpmenu)

		self.root.config(menu = self.menubar)
		# end menu
		
		# start Notebook01
		self.NoteBook01 = ttk.Notebook(self.root)
		self.NoteBook01.pack(expand = True, fill = BOTH)
		# end Notebook01
		
		self.root.protocol("WM_DELETE_WINDOW", self.SaveAll)
		
		

	def mainloop(self):

		self.MainDefault()

		self.FileRoot = self.NoteBook01
		self.FileDefault()
		self.TxtRoot = self.NoteBook01
		self.TxtDefault()
		self.FirewallRoot = self.NoteBook01
		self.FirewallDefault()
		self.RarRoot = self.NoteBook01
		self.RarDefault()
		
		self.ZzRoot = self.NoteBook01
		self.ZzDefault()

		self.MainRestoreState2()

		self.root.update_idletasks()
		self.root.deiconify()

		self.root.mainloop()


	def restart(self):
		self.root.destroy() 
		ft = FileTools()
		ft.mainloop()
		
	

if __name__ == "__main__":

	ft = FileTools()
	ft.mainloop()

'''
except (ImportError,Exception, ValueError) as e:
	logging.error(traceback.format_exc())
	print(str(e))
	os.system("pause")
'''

'''
self.root.destroy()        # destroy
self.root.withdraw()       # hide and show again
self.root.update()
self.root.deiconify()      # redraw window
self.Notebook01.tab(self.Notebook01.select(), "text")   # get notebook information
'''
