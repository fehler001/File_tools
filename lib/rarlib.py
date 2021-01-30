import sys
import os
from tkinter import messagebox
import random
import shutil
import stat
import subprocess
import time
import re
from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import cpu_count
import io
import zipfile

# third party
import pyzipper


try:
	import lib.baselib
except:
	import baselib

from natsort import natsort_keygen, ns


class RarLib():

	def __init__(self):
		super().__init__()

		try:
			self.bl = lib.baselib.BaseLib()
		except:
			self.bl = baselib.BaseLib()

		self.dict = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=~`[]{}|\\:;'\"<>,.?/ "

		

	# based on windows cmd
	def unrar_escape_cmd(self, parameter):
		e = "^&<>|\" "        # \ python will handle by self,  %  ! [ ] * ? . not need in unrar and don't escape it  
																				#	@ # $ ' ` , ; = ( ) { } not need but could be escape with '^'
		e2 = "^&<>|"   # escape with ^
		#e2 = e2 + "'`,;=()"

		s = 0
		for c in parameter:
			if c in e:
				s = 1
				break
		if s == 0:
			return parameter

		l = len(parameter)
		p = 'a' + parameter + 'a'
		i2 = 0
		for i in range(1, l + 1):
			if p[i+i2] in e2:
				p = p[ :i+i2] + '^' + p[i+i2] + p[i+i2+1: ]
				i2 = i2 + 1
				continue
			
			if p[i+i2] == '"':
				p = p[ :i+i2] + '""' + p[i+i2+1: ]
				i2 = i2 + 1
				continue

			if p[i+i2] == ' ':
				p = p[ :i+i2] + '" "' + p[i+i2+1: ]
				i2 = i2 + 2
				continue

		return p[1:-1]



	def unrar_brute_get_parameter(self, rar, dir = 'd:\\', unrar = 'd:\\u.exe', dict = None, prefix = '', suffix = '', outset = 'a', 
																		ii0 = 1, is_custom_dict = 0, is_rar = 'rar'):
		self.startupinfo = subprocess.STARTUPINFO()
		self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

		dir = dir.replace('/', '\\')  # cmd only support \
		rar = rar.replace('/', '\\')
		unrar = unrar.replace('/', '\\')
		pa = outset
		newpara = ''

		if is_custom_dict == 1:
			pw = self.unrar_escape_cmd(pa)
			if is_rar == 'rar':
				newpara =  '"'+unrar+'"'+ ' e ' +  '-p'+prefix+pw+suffix + ' ' + '"'+rar+'"' + ' ' + '"'+dir+'"'
			elif is_rar == '7z':
				newpara =  '"'+unrar+'"'+ ' x ' + '-o'+'"'+dir+'"' + ' ' + '"'+rar+'"'+ ' ' + '-p'+prefix+pw+suffix + ' ' + '-aos' 
			elif is_rar == 'zip':
				with pyzipper.AESZipFile(rar, 'r') as zip_file:
						try:
							zip_file.pwd = self.bl.str_encode(prefix+pa+suffix, enc = 'utf-8')
							zip_file.extractall(path = dir)
							newpara = 0
						except:
							pass
				newpara = ''

			if pa != dict[-1]:
				pa = dict[ dict.index(pa) + 1 ]	
			return pa, newpara
		
		else:
			for i0 in range(ii0):
				pw = self.unrar_escape_cmd(pa)
				if is_rar == 'rar':
					para =  unrar + ' e ' +  '-p'+prefix+pw+suffix + ' ' + rar + ' ' + dir
				elif is_rar == '7z':
					para =  '"'+unrar+'"'+ ' x ' + '-o'+dir + ' ' + rar + ' ' + '-p'+prefix+pw+suffix
				elif is_rar == 'zip':
					with pyzipper.AESZipFile(rar, 'r') as zip_file:
						try:
							zip_file.pwd = self.bl.str_encode(prefix+pa+suffix, enc = 'utf-8')
							zip_file.extractall(path = dir)
							newpara = 0
						except:
							pass
					para = ''
				newpara = newpara + '&' + para
				pa = self.bl.increase_one_by_dict(pa, dict)			

			return pa, newpara[1: ]



	def unrar_brute_run(self, newpara):
		subprocess.run(newpara, shell = True, universal_newlines=True, startupinfo = self.startupinfo, stderr = subprocess.PIPE, close_fds = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
		
	def unrar_brute_run_show_info(self, newpara):
		try:
			s = subprocess.run(newpara, shell = True, stderr = subprocess.PIPE, stdout = subprocess.PIPE, universal_newlines = True)
		except:
			messagebox.showerror ("ERROR", '"Inside Loop" might be too big')
			return -1
		o = s.stdout
		e = s.stderr
		r = s.returncode
		output = o + e
		return  r, output

		


if __name__ == '__main__':

	rl = RarLib()
	subprocess.run( ['powershell', 'd:\p.ps1'] )
	#os.startfile(r'd:\p.ps1')

# python zip
#rar = r'C:\Users\Administrator\Desktop\New folder\RJ280013.zip'
#dir = r'C:\Users\Administrator\Desktop\New folder'
#pw = 'nikaidou'
#pw = str(pw)
#pw = eval('b' + "'" + pw + "'")
#zf=zipfile.ZipFile(rar)
#zf.extractall(path = dir, pwd = pw)



# 7z
'''
# -aoa This switch overwrites all destination files. Use it when the new versions are preferred.
# -aos Skip over existing files without overwriting. Use this for files where the earliest version is most important.
# -aou Avoid name collisions. New files extracted will have a number appending to their names. You will have to deal with them later.
# -aot Rename existing files. This will not rename the new files, just the old ones already there.
'''