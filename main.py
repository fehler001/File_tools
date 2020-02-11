#coding=utf-8
#File_tools/main.py

import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog 
import os
import sys
import stat
import shutil
import json
import copy

import file
import txt
import firewall

import lib.baselib
import lib.filelib
import lib.txtlib
import lib.firewalllib

from natsort import natsort_keygen, ns




class Share():
	def __init__(self):
		super().__init__()

		self.RootWidth = 1000
		self.RootHeight = 600
		self.LogPath = r"C:\temp\File_tools.json"
		self.firewall_add_rules_savefile = r'firewall_add_rules_savefile.txt'
		self.EnableLog = 1

		self.bl = lib.baselib.BaseLib()
		self.fl = lib.filelib.FileLib()
		self.tl = lib.txtlib.TxtLib()
		self.fwl = lib.firewalllib.FirewallLib()

		self.natsort_key1 = natsort_keygen(key=lambda y: y.lower())   # l1.sort(key=self.natsort_key1)  # lower means lowerCase -> upperCase
		self.natsort_key2 = natsort_keygen(alg=ns.IGNORECASE)         # l2.sort(key=self.natsort_key2)




class FileTools(Share, file.File, txt.Txt, firewall.Firewall):

	def __init__(self):
		super().__init__()




	def MainDefault(self):
		self.FileToolsDefaultLog()
		self.CreateWidgetsFileTools()
		self.MainRestoreState()

		self.root.geometry(str(self.RootWidth) + 'x' + str(self.RootHeight))



	def FileToolsDefaultLog(self, recur = 0):
		if not os.path.exists(self.LogPath):
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
				j['file_tools']['window']['width'] = 1000
			if not 'height' in j['file_tools']['window']:
				j['file_tools']['window']['height'] = 600
			if not 'menu' in j['file_tools']:
				j['file_tools']['menu'] = {}
			if not 'log' in j['file_tools']['menu']:
				j['file_tools']['menu']['log'] = {}
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
			if j != j2:
				f = open(self.LogPath, 'w', encoding='utf-8')
				json.dump(j, f, ensure_ascii=False)
				f.close()
		except:
			if os.path.isfile(self.LogPath):
				os.chmod(self.LogPath, stat.S_IRWXU)
				os.unlink(self.LogPath)
		else:
			if recur == 0:
				self.FileToolsDefaultLog(recur = 1)



	def MainRestoreState(self):
		f = open(self.LogPath, 'r', encoding='utf-8')
		j = json.load(f)
		f.close()
		self.RootWidth = j['file_tools']['window']['width']
		self.RootHeight = j['file_tools']['window']['height']
		self.EnableLog = j['file_tools']['menu']['log']['enable_log']
		self.EnableLogVar.set(self.EnableLog)

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
		j['file_tools']['menu']['log']['enable_log'] = self.EnableLogVar.get()
		j['file_tools']['window']['width'] = self.root.winfo_width()
		j['file_tools']['window']['height'] = self.root.winfo_height()
		j['file_tools']['notebook']['notebook01']['current_index'] = self.NoteBook01.index(self.NoteBook01.select())
		f = open(self.LogPath, 'w', encoding='utf-8')
		json.dump(j, f, ensure_ascii=False)
		f.close()


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
		self.help.geometry('300x200')
		self.help.title("")
		self.LabelHelp = ttk.Label(self.help, text = r'Log path: "C:\temp\File_tools.json"', anchor = CENTER)
		self.LabelHelp.place(relx = 0, relwidth = 1, rely = 0, relheight = 1)
		#print(temp)


	def about(self):
		self.about = Toplevel(self.root)
		self.about.geometry('300x200')
		self.about.title("")
		self.LabelAbout = ttk.Label(self.about, text="File tools Ver 0.22\n\n    Author tgbxs", anchor = CENTER)
		self.LabelAbout.place(relx = 0, relwidth = 1, rely = 0, relheight = 1)


	def SaveAll(self, exit = 1):
		try:
			self.MainSaveEntry()

			self.RenameSaveEntry()
			self.RefineSaveEntry()
			self.RemoveSaveEntry()
			self.FilterSaveEntry()
			self.FindSaveEntry()
			self.MoveSaveEntry()
			
			self.DivideSaveEntry()
			self.StrSaveEntry()

			self.ARuleSaveEntry()
			if exit == 0:
				return
		finally:
			sys.exit()


	def CreateWidgetsFileTools(self):
		
		self.root = Tk()
		
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
		
		self.MainRestoreState2()
		self.root.mainloop()


	def restart(self):
		self.root.destroy() 
		ft = FileTools()
		ft.mainloop()
		
	

if __name__ == "__main__":

	ft = FileTools()
	ft.mainloop()
	


'''
self.root.destroy()        # destroy
self.root.withdraw()       # hide and show again
self.root.update()
self.root.deiconify()      # redraw window
self.Notebook01.tab(self.Notebook01.select(), "text")   # get notebook information
'''
