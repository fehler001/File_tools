#coding=utf-8
#File_tools/lib/filelib.py
import os
from tkinter import messagebox
import random
import shutil
import stat

import lib.baselib

from natsort import natsort_keygen, ns



'''
import ctypes
import ctypes.wintypes
class LPSHFILEOPSTRUCT(ctypes.Structure):

    _fields_ = [
        ('hwnd', ctypes.wintypes.HWND),
        ('wFunc', ctypes.wintypes.UINT),
        ('pFrom', ctypes.wintypes.PCHAR),
        ('pTo', ctypes.wintypes.PCHAR),
        ('fFlags', ctypes.wintypes.INT),
        ('fAnyOperationsAborted', ctypes.wintypes.BOOL),
        ('hNameMappings', ctypes.wintypes.LPVOID),
        ('lpszProgressTitle', ctypes.wintypes.PCHAR)
    ]


FO_DELETE = 3

FOF_SILENT = 4
FOF_NOCONFIRMATION = 16
FOF_ALLOWUNDO = 64
FOF_NOCONFIRMMKDIR = 512
FOF_NOERRORUI = 1024
FOF_NO_UI = FOF_SILENT | FOF_NOCONFIRMATION | FOF_NOERRORUI | FOF_NOCONFIRMMKDIR


def send_to_trash_windows(p):
    r = ctypes.windll.shell32.SHFileOperation(LPSHFILEOPSTRUCT(
        hwnd=0,
        wFunc=FO_DELETE,
        pFrom=ctypes.create_string_buffer(p.encode()),
        fFlags=FOF_ALLOWUNDO | FOF_NO_UI
    ))
    if r:
        raise Exception(r)
'''



# deal with file name or folder name
# all the path must be full path
class FileLib():

	def __init__(self):
		super().__init__()

		self.natsort_key1 = natsort_keygen(key=lambda y: y.lower())   # l1.sort(key=self.natsort_key1)  # lower means lowerCase -> upperCase
		self.natsort_key2 = natsort_keygen(alg=ns.IGNORECASE)         # l2.sort(key=self.natsort_key2)

		self.bl = lib.baselib.BaseLib()



	def collect_files_and_folders(self, path, is_add_file = 1, is_add_folder = 0):
		all = []
		files = os.listdir(path) 
		if path[-1:] == r'/':
			path = path[ :-1]
		for file in files:
			file1 = path + '/' + file
			if os.path.isfile(file1) and is_add_file == 1:
				all.append(file1)
			if os.path.isdir(file1) and is_add_folder == 1:
				all.append(file1)
		return all



	def get_folder_size(self, path):
		total_size = 0
		for root, subfolders, files in os.walk(path):
			for file in files:
				root_f = root.replace('\\', '/')
				if root_f[-1] == '/':
					root_f = root_f[ :-1]
				f = root_f + '/' + file
				size = os.path.getsize(f)
				total_size = total_size + size
		return total_size


	def generate_ordinal(self, length, digit = 1, outset = 0):
		all = []
		n = 0 + outset
		for i in range(length):
			if n >= 0:
				all.append( '0'*(digit - len(str(n)) ) + str(n) )
			else:
				all.append('-' + '0'*(digit - len(str(n)) + 1) + str(abs(n)) )
			n = n + 1
		return all


	def rename_by_ordinal(self, files, digit = 1, outset = 0):
		all = []
		length = 0
		for file in files:
			if file == '\n' or file == '':
				continue
			else:
				length = length + 1
		ordinal = self.generate_ordinal(length, digit = digit, outset = outset)

		n = 0
		for file in files:
			if file == '\n' or file == '':
				continue
			i = file.rfind(r'/')
			if i == -1:
				all.append(file)
				continue
			i2 = file.rfind(r'.')
			if i2 == -1 or i2 < i:
				i2 = len(file)
			new_file = file[0:i] + r'/' + ordinal[n] + file[i2: ]
			all.append(new_file)
			n = n + 1
		return all


	def insert(self, files, pos, cont, is_ordinal = False, digit = 1, outset = 0):
		all = []
		
		if is_ordinal is True:
			length = 0
			for file in files:
				if file == '\n' or file == '':
					continue
				else:
					length = length + 1
			ordinal = self.generate_ordinal(length, digit = digit, outset = outset)
			n = 0

		for file in files:
			if file == '\n' or file == '':
				continue
			i = file.rfind('/')
			if i == -1:
				all.append(file)
				continue
			i2 = file.rfind('.')
			if i2 < i:
				i3 = len(file) - i   # name length
			else:
				i3 = len(file) - i - ( len(file) - i2 )
			if pos >= 0:
				if pos <= i3:
					new_pos = i + 1 + pos
				else:
					new_pos = i + 1 + i3
			if pos < 0:
				if abs(pos) <= i3:
					new_pos = i + 1 + i3 - abs(pos)
				else:
					new_pos = i + 1
			if is_ordinal is False:
				new_file = file[ 0 : new_pos ] + cont + file[ new_pos : ]
			else:
				new_file = file[ 0 : new_pos ] + ordinal[n] + file[ new_pos : ]
				n = n + 1
			all.append(new_file)
		return all


	def replace_string(self, files, original, substitute):
		all = []
		for file in files:
			if file == '\n' or file == '':
				continue
			i = file.rfind(original)
			if i != -1 and i > file.rfind(r'/'):
				new_file = file[0:i] + substitute + file[i + len(original) : ]
				all.append(new_file)
			else:
				all.append(file)
		return all


	def find_enfold(self, path):
		all = []
		for root, subfolders, files in os.walk(path):
				for subfolder in subfolders:
					root = root.replace('\\', '/')
					i = root.rfind('/')
					s = root[i + 1 : ]
					if subfolder == s:
						L = os.listdir(root)
						l = len(L)
						if l == 1:
							all.append(root + '/' + subfolder)
		return all


	def refine_enfold(self, folders):
		for i in range(len(folders)):
			if len(folders[i]) < 5:
				continue
			r = random.random()
			r = str(r)
			f = folders[i]
			i = f.rfind(r'/')
			i2 = f[:i].rfind(r'/')
			f2 = f + r
			os.rename(f, f2)
			dst = f[ : i2] 
			shutil.move(f2, dst)
			os.rmdir(f[:i])
			os.rename(dst + f[i: ] + r, dst + f[i: ] )


	def find_empty_folder(self, path):
		all = []
		for root, subfolders, files in os.walk(path):
				for subfolder in subfolders:
					root = root.replace('\\', '/')
					i = root.rfind('/')
					if root[-1] == '/':
						root = root[ :-1]
					f = root + r'/' + subfolder
					L = os.listdir(f)
					l = len(L)
					if l == 0:
						all.append(f)
		return all


	def filter(self, path, include = '', exclude = '', max = '', min = '', \
				including_file = 1, including_folder = 0, case_insensitive = 0, is_exactly_same = 0, name_max = '', name_min = ''):
		all = []
		if case_insensitive == 1:
			include = include.lower()
			exclude = exclude.lower()
		for root, subfolders, files in os.walk(path):
			if including_folder == 1:
				for subfolder in subfolders:
					root_f = root.replace('\\', '/')
					if root_f[-1] == '/':
						root_f = root_f[ :-1]
					f = root_f + '/' + subfolder
					if case_insensitive == 1:
						f = f.lower()
					fs = self.get_folder_size(f)
					fns = len(subfolder)
					i_f = f.rfind('/')
					i2_f = f.rfind(include)
					i3_f = f.rfind(exclude)
					if i2_f == -1:
						continue
					if i2_f < i_f:
						continue
					if i3_f > i_f and exclude != '':
						continue
					if max != '' :
						if fs > max:
							continue
					if min != '':
						if fs < min:
							continue
					if name_max != '' :
						if fns > name_max:
							continue
					if name_min != '':
						if fns < name_min:
							continue
					if is_exactly_same == 1:
						if subfolder != include:
							continue
					all.append(f)

		for root, subfolders, files in os.walk(path):
			if including_file == 1:
				for file in files:
					root_ff = root.replace('\\', '/')
					if root_ff[-1] == '/':
						root_ff = root_ff[ :-1]
					ff = root_ff + '/' + file
					if case_insensitive == 1:
						ff = ff.lower()
					size = os.path.getsize(ff)
					i_ff = ff.rfind('/')
					ffns = len( ff[i_ff : ] )
					i2_ff = ff.rfind(include)
					i3_ff = ff.rfind(exclude)
					if i2_ff == -1:
						continue
					if i2_ff < i_ff:
						continue
					if i3_ff > i_ff and exclude != '':
						continue
					if max != '' :
						if size > max:
							continue
					if min != '':
						if size < min:
							continue
					if name_max != '' :
						if ffns > name_max:
							continue
					if name_min != '':
						if ffns < name_min:
							continue
					if is_exactly_same == 1:
						if file != include:
							continue
					all.append(ff)
		return all


	def find_same_folder_strctrue(self, src, dst, is_subfolder_with_same_name = 0):
		all = []
		source_collected = []
		source_collected_replaced = []
		all_file_in_destination = []
		same_file = []
		
		new_dsts = []
		if is_subfolder_with_same_name == 1:
			new_dsts = self.filter(dst, include = src[src.rfind('/') + 1 : ], including_file = 0, including_folder = 1, is_exactly_same = 1)
		new_dsts.append(dst)

		for new_dst in new_dsts:
			for root, subfolders, files in os.walk(new_dst):
				for file in files:
					all_file_in_destination.append( os.path.join(root, file).replace('\\', '/') )
			if not all_file_in_destination:
				return ["Nothing in the destination"]
			for root, subfolders, files in os.walk(src):
				for file in files:
					source_collected.append( os.path.join(root, file).replace('\\', '/') )
			if not source_collected:
				return ["Nothing in the source"]
			for file in source_collected:
				source_collected_replaced.append( file.replace(src, new_dst) )
			for file in source_collected_replaced:
				if file in all_file_in_destination:
					same_file.append(file)
			if same_file:
				for file in same_file:
					all.append(file)
			else:
				return ["Could not find any file in same strcture"]
		return all


	def move_or_copy(self, lines, path, is_creating_new_folder = 0, new_folder_name = '', is_interval = 0, interval = 100, skip = 0, is_move = 0 ):
		if not os.path.isdir(path):
			messagebox.showerror ("Warrning", "_____PATH ERROR_____")
			return -1
		if path[-1] == '/':
			dir = path[ :-1]
		else:
			dir = path
		if is_creating_new_folder == 1:
			if self.bl.check_legit_string(new_folder_name) == -1:
				return -1
		
		old_folders = []
		new_folders = []
		old_files = []
		new_files = []
		for line in lines:
			if os.path.isdir(line):
				dst = dir + '/' + line[line.rfind('/') + 1: ]
				if os.path.isdir(dst):
					if skip == 1:
						continue
					messagebox.showerror ("Warrning", dst + "\n\nAlready exists")
					return -1
				else:
					new_folders.append(dst)
					old_folders.append(line)
		n = 0
		n2 = 0
		n3 = -1
		creating_new_folder_paths = []
		for line in lines:
			if os.path.isfile(line):
				if is_creating_new_folder == 1:
					dir2 = dir + '/' + new_folder_name
					if is_interval == 1:
						if n % interval == 0 and n != 0:
							n2 = n2 + 1
						dir3 = dir2 + str(n2 * interval + 1) + '-' + str( (n2 + 1) * interval) 
					else:
						dir3 = dir2
					if n3 < n2:
						if os.path.isdir(dir3):
							if skip == 0:
								messagebox.showerror ("Warrning", dir3 + "\n\nAlready exists")
								return -1
						else:
							creating_new_folder_paths.append(dir3)
						n3 = n3 + 1
				else:
					dir3 = dir
				dst = dir3 + '/' + line[ line.rfind('/') + 1 : ]
				if os.path.isfile(dst):
					if skip == 1:
						n = n + 1
						continue
					else:
						messagebox.showerror ("Warrning", dst + "\n\nAlready exists")
						return -1
				else:
					new_files.append(dst)
					old_files.append(line)
				n = n + 1
		if is_creating_new_folder == 1:
			for path in creating_new_folder_paths:
				os.mkdir(path)
		if is_move == 0:
			for i in range(len(old_folders)):
				shutil.copytree(old_folders[i], new_folders[i])
			for i in range(len(old_files)):
				shutil.copy2(old_files[i], new_files[i])
		if is_move == 1:
			for i in range(len(old_folders)):
				shutil.move(old_folders[i], new_folders[i])
			for i in range(len(old_files)):
				shutil.move(old_files[i], new_files[i])


	def find_files_with_same_name_by_list(self, src, dst, including_file = 1, including_folder = 1):
		all = []
		files_src = self.filter(src, including_file = including_file, including_folder = including_folder)
		files_dst = self.filter(dst, including_file = including_file, including_folder = including_folder)
		for file in files_dst:
			name_file = file[ file.rfind('/') : ]
			for file2 in files_src:
				name_file2 = file2[ file2.rfind('/') : ]
				if name_file2 == name_file:
					if file not in all:
						all.append(file)
		return all


	def delete_single(self, path, including_read_only = 1):
		if including_read_only == 1:
			os.chmod(path, stat.S_IRWXU)
		if os.path.isfile(path):
			os.remove(path)
			return
		if os.path.isdir(path):
			shutil.rmtree(path)
			return	

	# return string 
	def delete_list(self, list, including_read_only = 1, skip_error = 1):
		list = set(list)
		list = sorted(list, key=self.natsort_key2)
		line = ''
		for line in list:
			if line == '\n' or line == '':
				continue
			if os.path.isfile(line):
				try:
					self.delete_single(line, including_read_only = including_read_only)
				except:
					if skip_error == 1:
						continue
					else:
						messagebox.showerror ("Warrning", line + "\n\nWent Wrong")
						return -1
		for line in list:
			if line == '\n' or line == '':
				continue
			if os.path.isdir(line):
				try:
					self.delete_single(line, including_read_only = including_read_only)
				except:
					if skip_error == 1:
						continue
					else:
						messagebox.showerror ("Warrning", line + "\n\nWent Wrong")
						return -1
