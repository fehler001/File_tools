#coding=utf-8
#File_tools/lib/filelib.py

import os
from tkinter import messagebox
import random
import shutil
import stat
import pprint
import time

try:
	import lib.baselib
except:
	import baselib

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

		try:
			self.bl = lib.baselib.BaseLib()
		except:
			self.bl = baselib.BaseLib()




	def collect_files_and_folders(self, path, is_add_file = 1, is_add_folder = 0, is_recur = 0):
		all = []
		if path[-1:] == r'/':
			path = path[ :-1]
		if is_recur == 1:
			if is_add_folder == 1:
				for root, subfolders, files in os.walk(path):
					for subfolder in subfolders:
						folder1 = root.replace('\\', '/') + '/' + subfolder
						all.append(folder1)
			if is_add_file == 1:
				for root, subfolders, files in os.walk(path):
					for file in files:
						file1 = root.replace('\\', '/') + '/' + file
						all.append(file1)
			return all
		if is_add_file == 1 or is_add_folder == 1:
			files = os.listdir(path) 
			for file in files:
				file1 = path + '/' + file
				if os.path.isfile(file1) and is_add_file == 1:
					all.append(file1)
				if os.path.isdir(file1) and is_add_folder == 1:
					all.append(file1)
		return all




	# 'c:/1.0-_asd.txt'  =>  'c:/asd.txt'
	def delete_front_ordinal(self, path, is_under = 0):
		d = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.']
		if is_under == 1:
			d.append('_')
		try:
			pinfo = self.bl.get_path_info(path)
			if pinfo['is_exist'] == 0:
				return path
			for i in range( len(pinfo['filename']) ):
				if pinfo['filename'][0] in d:
					pinfo['filename'] = pinfo['filename'][1: ]
					continue
				break
			rst = pinfo['parent'] + '/' + pinfo['filename']
			return rst
		except:
			return path




	# digit = 3, outset = 1, 'c:/foo/bar.txt', 'c:/foo/barbar.txt'  =>  'c:/foo/001.txt', 'c:/foo/002.txt'
	def rename_by_ordinal(self, files, digit = 1, outset = 0):
		all = []
		ordinal = self.bl.generate_ordinal( len(files), digit = digit, outset = outset)

		n = 0
		for file in files:
			file = file.replace('\\', '/')
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




	# 'c:/foo/bar.txt', 'c:/foo/barbar.txt'  
	# is_ordinal = True, digit = 3, outset = 1   =>   'c:/foo/001bar.txt', 'c:/foo/002barbar.txt' 
	# is_ordinal = False, pos = 0, cont = 'zz'   =>   'c:/foo/zzbar.txt', 'c:/foo/zzbarbar.txt' 
	def insert(self, files, pos = 0, cont = '', ordinal = None):
		all = []

		n = 0
		for file in files:
			file = file.replace('\\', '/')
			pinfo = self.bl.get_path_info(file)
			if pinfo['is_exist'] == 0:
				all.append('( Not exist ) ' + file)
				continue
			if pos >= 0:
				if pos <= len(pinfo['name']):
					new_pos = pinfo['/'] + 1 + pos
				else:
					new_pos = pinfo['/'] + 1 + pinfo['.']
			if pos < 0:
				if abs(pos) <= len(pinfo['name']):
					new_pos = pinfo['.'] - abs(pos) + 1
				else:
					new_pos = pinfo['/'] + 1
			
			if ordinal is None:
				new_file = file[ 0 : new_pos ] + cont + file[ new_pos : ]
			else:
				new_file = file[ 0 : new_pos ] + ordinal[n] + file[ new_pos : ]
				n = n + 1
			all.append(new_file)
		return all



	# original = 'ar', substitute = 'zz', 'c:/foo/bar.txt'   =>   'c:/foo/bzz.txt'  
	def replace_string(self, files, original, substitute):
		all = []
		for file in files:
			if file == '\n' or file == '':
				continue
			file = file.replace('\\', '/')
			i = file.rfind(original)
			if i != -1 and i > file.rfind(r'/'):
				new_file = file[0:i] + substitute + file[i + len(original) : ]
				all.append(new_file)
			else:
				all.append(file)
		return all



	# p1 = 0, p2 = -1, 'c:/foo/bar.txt'
	# get -> 'c:/foo/b.txt'  
	# delete -> 'c:/foo/ar.txt'
	def get_or_delete_middle_filename(self, file, p1 = 0, p2 = -1, get_middle = 1):
		file = file.replace('\\', '/')
		pinfo = self.bl.get_path_info(file)
		if pinfo['is_exist'] == 0:
			return file
		i = pinfo['/']
		i2 = pinfo['.']
		l = len(file)
		if p1 >= 0 and p1 >= len(pinfo['name']):
			return -1
		if p1 < 0 and abs(p1) - 1 >= len(pinfo['name']):
			return -1
		if p2 >= 0 and p2 >= len(pinfo['name']):
			return -1
		if p2 < 0 and abs(p2) - 1 >= len(pinfo['name']):
			return -1
		if p1 < 0:
			ap1 = l - len(pinfo['ext']) - abs(p1) + 1    # "-1 + 1" means end 
		else:
			ap1 = i + 1 + p1
		if p2 < 0:
			ap2 = l - len(pinfo['ext']) - abs(p2) + 1
		else:
			ap2 = i + 1 + p2

		if get_middle == 1:
			new_file = file[ :i+1] + file[ap1 : ap2] + pinfo['ext']
		else:
			new_file = file[ :ap1]  + file[ap2: ]

		return new_file



	# see 'Refine Enfold' description
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



	# see 'Refine Enfold' description
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




	def filter(self, path, include = '', exclude = '', max = '', min = '', including_file = 1, including_folder = 0, \
case_insensitive = 0, is_exactly_same = 0, name_max = '', name_min = '', is_extension = 0, is_recur = 1):
		all = []
		if case_insensitive == 1:
			include = include.lower()
			exclude = exclude.lower()
		if including_folder == 1 and is_extension == 0:
			for root, subfolders, files in os.walk(path):
				for subfolder in subfolders:
					if is_recur == 0:
						if root != path:
							break
					root_f = root.replace('\\', '/')       # root_f = root path of subfolder
					if root_f[-1] == '/':
						root_f = root_f[ :-1]
					f = root_f + '/' + subfolder           # f = full path of subfolder
					if case_insensitive == 1:
						f = f.lower()
					fs = self.bl.check_path_exist(f)
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

		if including_file == 1:
			for root, subfolders, files in os.walk(path):
				for file in files:
					if is_recur == 0:
						if root != path:
							break
					root_ff = root.replace('\\', '/')          # root_ff = root path of file
					if root_ff[-1] == '/':
						root_ff = root_ff[ :-1]
					ff = root_ff + '/' + file                  # ff = full path of file
					if case_insensitive == 1:
						ff = ff.lower()
					size = os.path.getsize(ff)
					i_ff = ff.rfind('/')
					ffns = len( ff[i_ff : ] )
					i2_ff = ff.rfind(include)
					i3_ff = ff.rfind(exclude)
					i4_ff = ff.rfind(r'.')
					if is_extension == 1:
						if i4_ff == -1 or i4_ff < i_ff or i4_ff != i2_ff:
							continue
						if include != ff[ i4_ff : ]:
							continue
						if case_insensitive == 1:
							if include.lower() != ff[ i4_ff : ]:
								continue
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


	# see 'Find' description
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



	# see 'Move' description  
	# to achieve 'c:/bar/a.txt' -> 'd:/bar/a.txt',  'd:/' is an enpty folder
	# shutil.copytree('c:/bar', 'd:/bar')  or  shutil.copy2('c:/bar/a.txt', 'd:/bar/a.txt')
	def move_or_copy(self, lines, path, is_creating_new_folder = 0, new_folder_name = '', is_interval = 0, interval = 100, skip = 0, is_move = 0 ):
		if not os.path.isdir(path):
			messagebox.showerror ("Warrning", "_____PATH ERROR_____")
			return -1
		if path[-1] == '/':    
			dir = path[ :-1]
		else:
			dir = path           # things will be move here, like 'd:/'
		if is_creating_new_folder == 1:
			if self.bl.check_legit_string(new_folder_name) == -1:       # new_folder_name,  like 'newfolder'
				return -1
		
		old_folders = [] # things need to move,  like 'c:/bar'
		new_folders = [] # new full dst of things (including filename),  like 'd:/bar'
		old_files = []   # like  'c:/bar/a.txt'
		new_files = []   # like  'd:/bar/a.txt'
		for line in lines:
			if os.path.isdir(line):
				dst = dir + '/' + line[line.rfind('/') + 1: ]    # like 'd:/bar'
				if os.path.isdir(dst):
					if skip == 1:
						continue
					messagebox.showerror ("Warrning", dst + "\n\nAlready exists")
					return -1
				else:
					new_folders.append(dst)   # like 'd:/bar'
					old_folders.append(line)  # like 'c:/bar'
		n = 0      # numbers of files
		n2 = 0     # count of interval went through
		n3 = -1    # compare with n2, if n2 increased, create folder like  'd:/bar/newfolder011-020', then n3 = n2
		creating_new_folder_paths = []       # like  'd:/bar/newfolder'  or  'd:/bar/newfolder001-010'
		for line in lines:                     # line 'c:/bar/a.txt'
			if os.path.isfile(line):
				if is_creating_new_folder == 1:
					dir2 = dir + '/' + new_folder_name    #  ->  'd:/bar/newfolder'
					if is_interval == 1:
						if n % interval == 0 and n != 0:
							n2 = n2 + 1
						dir3 = dir2 + str(n2 * interval + 1) + '-' + str( (n2 + 1) * interval)  # like  'd:/bar/newfolder001-010'
					else:
						dir3 = dir2
					if n3 < n2:
						if os.path.isdir(dir3):
							if skip == 0:
								messagebox.showerror ("Warrning", dir3 + "\n\nAlready exists")
								return -1
						else:
							creating_new_folder_paths.append(dir3)    #  like   'd:/bar/newfolder001-010'
						n3 = n3 + 1
				else:
					dir3 = dir
				dst = dir3 + '/' + line[ line.rfind('/') + 1 : ]     #  like  'd:/bar/newfolder001-010/a.txt'
				if os.path.isfile(dst):
					if skip == 1:
						n = n + 1
						continue
					else:
						messagebox.showerror ("Warrning", dst + "\n\nAlready exists")
						return -1
				else:
					new_files.append(dst)    # like  'd:/bar/newfolder001-010/a.txt'
					old_files.append(line)   # like  'c:/bar/a.txt'
				n = n + 1
		if is_creating_new_folder == 1:
			for path in creating_new_folder_paths:      # like  'd:/bar/newfolder001-010'
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



	# is_list = 0 means src = one dir   ->   collect all names in src, find all same file in dst
	# is_list = 1 means src = one list (files or dirs included) -> collect all names in each item, find all same file in dst
	def find_files_with_same_name_by_list(self, src, dst, including_file = 1, including_folder = 1, \
		is_recur_src = 1, is_recur_dst = 1, is_list = 0):
		all = []
		files_src = []
		if is_list == 0:
			files_src = self.filter(src, including_file = including_file, including_folder = including_folder, is_recur = is_recur_src)
		else:
			src = self.bl.clean_list(src)
			for item in src:
				try:
					if os.path.isfile(item):
						files_src.append(item)
					if os.path.isdir(item):
						files_src.extend( self.filter(item, including_file = including_file, including_folder = including_folder, is_recur = is_recur_src))
				except:
					pass
		files_dst = self.filter(dst, including_file = including_file, including_folder = including_folder, is_recur = is_recur_dst)
		for file in files_dst:
			name_file = file[ file.rfind('/') : ]
			for file2 in files_src:
				name_file2 = file2[ file2.rfind('/') : ]
				if name_file2 == name_file:
					files_src.remove(file2)   # delete element once paired
					if file not in all:
						all.append(file)
		return all


	# delete one file or one folder(not empty)
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



if __name__ == '__main__':
	fl = FileLib()
	a=r'g:\a'
	o=fl.get_path_date(a)
	print(o)
	print(o['ctime'])
	b=fl.generate_date_ordinal( 10, outset = o['sctime'], interval = 65451468)
	pprint.pprint(b)