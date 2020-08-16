#coding=utf-8
#File_tools/lib/filelib.py

import os
from tkinter import messagebox
import random
import shutil
import stat
import pprint
import time
import re

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



	def check_system_file(self, path):
		path = path.replace('\\', '/')
		path = path.replace('//', '/')
		path = path.lower()
		if 'System Volume Information'.lower() in path:
			return -1
		if  '$RECYCLE.BIN'.lower() in path:
			return -1
	

	def check_banned_path(self, path):
		path = path.replace('\\', '/')
		path = path.replace('//', '/')
		path = path.lower()
		if path[-1:] == r'/' and len(path) > 3:
			path = path[ :-1]
		s = 0
		for i in range(9):
			if  path == 'C:/'.lower():
				s = 1
				break
			if  path == 'C:/ProgramData'.lower():
				s = 1
				break
			'''
			if  path == 'C:/ProgramData/Application Data'.lower():
				s = 1
				break
			if  path == 'C:/ProgramData/ASTER Control'.lower():
				s = 1
				break
			if  path == 'C:/ProgramData/Documents'.lower():
				s = 1
				break
			if  path == 'C:/ProgramData/Start Menu'.lower():
				s = 1
				break
			if  path == 'C:/ProgramData/Desktop'.lower():
				s = 1
				break
			if  path == 'C:/ProgramData/Templates'.lower():
				s = 1
				break
			if  path == 'C:/Documents and Settings'.lower():
				s = 1
				break
			'''
		if s == 1:
			messagebox.showerror ("ERROR", '"C:/ProgramData" is not supported')
			return -1
		if not os.path.isdir(path):
			messagebox.showerror ("ERROR", path + '\n\ndoes not exist')
			return -1
		

	def collect_files_and_folders(self, path, is_add_file = 1, is_add_folder = 0, is_recur = 0):
		all = []
		if path[-1:] == r'/' and len(path) > 4:
			path = path[ :-1]
		path = path.replace('\\', '/')
		if is_recur == 1:
			if is_add_folder == 1:
				for root, subfolders, files in os.walk(path):
					if self.check_system_file(root) == -1: 
						continue
					for subfolder in subfolders:
						if self.check_system_file(subfolder) == -1: 
							continue
						folder1 = root.replace('\\', '/') + '/' + subfolder
						all.append(folder1)
			if is_add_file == 1:
				for root, subfolders, files in os.walk(path):
					if self.check_system_file(root) == -1: 
						continue
					for file in files:
						if self.check_system_file(file) == -1: 
							continue
						file1 = root.replace('\\', '/') + '/' + file
						all.append(file1)
			for i in range(len(all)):
				all[i] = all[i].replace('//', '/')
			return all
		if is_add_file == 1 or is_add_folder == 1:
			files = os.listdir(path) 
			for file in files:
				if self.check_system_file(file) == -1: 
						continue
				file1 = path + '/' + file
				if os.path.isfile(file1) and is_add_file == 1:
					all.append(file1)
				if os.path.isdir(file1) and is_add_folder == 1:
					all.append(file1)
		for i in range(len(all)):
			all[i] = all[i].replace('//', '/')
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
	def rename_by_ordinal(self, files, digit = 1, outset = 0, interval = 1):
		all = []
		ordinal = self.bl.generate_ordinal( len(files), digit = digit, outset = outset, interval = interval)

		n = 0
		for file in files:
			pinfo = self.bl.get_path_info(file)
			if pinfo['/'] == 0:           # if not exist
				all.append(file)        
				continue
			new_file = file[ 0 : pinfo['/'] ] + r'/' + ordinal[n] + file[ pinfo['.'] : ]
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
	def replace_string(self, files, original, substitute, match_pos, is_check_path_exist = 1, is_advanced_mode = 0):
		all = []
		if type(files) == str:
			files = [files]
		original = re.escape(original)
		original = original.replace(r'\?', '.')
		original = original.replace(r'\*', '.*')
		
		for file in files:
			pinfo = self.bl.get_path_info(file)

			if is_advanced_mode == 1:
				pinfo['filename'] = pinfo['parent'] + '/' + pinfo['filename']
				pinfo['parent'] = ''

			matchs = re.findall(original, pinfo['filename'])			# , [re.MULTILINE]) search in all lines
			if matchs == []:
				all.append(file)
				continue
			
			if match_pos == 'match all':
				for m in matchs:
					if substitute != r'\n':
						pinfo['filename'] = pinfo['filename'].replace(m, substitute)
					else:
						pinfo['filename'] = pinfo['filename'].replace(m, '\n')
			else:
				pos = None
				if match_pos == 'match first': pos = 0
				if match_pos == 'match second': pos = 1
				if match_pos == 'match third': pos = 2
				if match_pos == 'match fourth': pos = 3
				if match_pos == 'match fifth': pos = 4
				if match_pos == 'match last': pos = -1
				if pos is None:
					if self.bl.check_legit_int(match_pos) == -1:
						return -1
					else:
						pos = int(match_pos)

			if match_pos != 'match all':
				s = []
				for m in matchs:
					for span in re.finditer(m, pinfo['filename']):
						s.append(span.span())
				s = sorted(s)
				p = pos
				if p > len(s) - 1: p = -1
				if p < 0:
					if abs(p) > len(s): p = 0
				f = pinfo['filename']
				if substitute != r'\n':
					pinfo['filename'] = f[ 0 : s[p][0] ] + substitute + f[ s[p][1] : ]
				else:
					pinfo['filename'] = f[ 0 : s[p][0] ] + '\n' + f[ s[p][1] : ]

			if is_check_path_exist == 1:
				if is_advanced_mode == 1:
					all.append(pinfo['filename'])
				else:
					all.append(pinfo['parent'] + '/' + pinfo['filename'])
			else:
				all.append(pinfo['filename'])
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
	def find_enfold(self, path, is_samename = 1):
		all = []
		for root, subfolders, files in os.walk(path):
				for subfolder in subfolders:
					root = root.replace('\\', '/')
					i = root.rfind('/')
					s = root[i + 1 : ]
					list = os.listdir(root)
					l = len(list)
					if l == 1:
						if is_samename == 1:
							if subfolder == s:
								all.append(root + '/' + subfolder)
						else:
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




	def filter(self, path, include = '', excludes = '', max = '', min = '', including_file = 1, including_folder = 0, \
case_insensitive = 0, is_exactly_same = 0, name_max = '', name_min = '', is_extension = 0, is_recur = 1, is_custom_list = 0):
		all = []
		if type(excludes) == str:
			excludes = [excludes]
		if case_insensitive == 1:
			include = include.lower()
			for i in range(len(excludes)):
				excludes[i] = excludes[i].lower()
		re_include = re.escape(include)
		re_include = re_include.replace(r'\?', '.')
		re_include = re_include.replace(r'\*', '.*')

		if is_custom_list == 0:
			plist = self.collect_files_and_folders(path, is_add_file = including_file, is_add_folder = including_folder, is_recur = is_recur)
		else:
			plist = path

		for p in plist:
			exclude_switch = 0
			p = p.replace('\\', '/') 
			pinfo = self.bl.get_path_info(p)

			if case_insensitive == 1:
				pinfo['filename'] = pinfo['filename'].lower()

			if is_exactly_same == 1:
				if pinfo['filename'] != include:
					continue

			matchs = re.findall(re_include, pinfo['filename'])			# , [re.MULTILINE]) search in all lines
			if matchs == []:
				continue

			if excludes != ['']:
				for exclude in excludes:
					re_exclude = re.escape(exclude)
					re_exclude = re_exclude.replace(r'\?', '.')
					re_exclude = re_exclude.replace(r'\*', '.*')
					matchs = re.findall(re_exclude, pinfo['filename'])			# , [re.MULTILINE]) search in all lines
					if matchs != []:
						exclude_switch = 1
						break
				if exclude_switch == 1:
					continue

			if name_max != '' :
				if len(pinfo['filename']) > name_max:
					continue
			if name_min != '':
				if len(pinfo['filename']) < name_min:
					continue

			if max != '' or min != '' :
				if pinfo['isdir'] == 1:
					try:
						fs = self.bl.get_folder_size(p)       # some windows folder can not be accessed
					except:
						continue
				if pinfo['isfile'] == 1:
					fs = os.path.getsize(p)				
			if max != '' :
				if fs > max:
					continue
			if min != '':
				if fs < min:
					continue

			if is_extension == 1:
				if pinfo['isfile'] == 1:
					if include == '' and pinfo['filename'] == pinfo['name']:
						all.append(p)
						continue
					if include == pinfo['ext']:
						all.append(p)
						continue
				continue
			
			all.append(p)

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
	def move_or_copy(self, lines, path, is_creating_new_folder = 0, new_folder_name = '', is_interval = 0, interval = 100, skip = 0, is_move = 0, is_overwrite = 0 ):
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
				if os.path.exists(dst):
					if is_overwrite == 0:
						messagebox.showerror ("Warrning", dst + "\n\nAlready exists")
						return -1
					else:
						continue
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
						if os.path.exists(dir3):
							if is_overwrite == 0:
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
					elif is_overwrite == 1:
						n = n + 1
						try:
							os.unlink(dst)
						except:
							messagebox.showerror ("Error", dst + "\n\nCould not be overwrited")
							return -1
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
	def delete_single(self, path, including_read_only = 1, show_error = 1):
		try:
			if including_read_only == 1:
				os.chmod(path, stat.S_IRWXU)
			if os.path.isfile(path):
				os.remove(path)
				return
			if os.path.isdir(path):
				shutil.rmtree(path)
				return	
		except:
			if show_error == 1:
				messagebox.showerror ("Error", path + "\n\nCan not be deleted")
				return -1



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



	def copy_folder(self, path_from, path_to, is_overwrite = 0):
		#existed = self.find_same_folder_strctrue(src = path_from, dst = path_to, is_subfolder_with_same_name = 0)
		#print(existed)
		#self.delete_list(list = existed, including_read_only = 1, skip_error = 0)
		
		items = self.collect_files_and_folders(path = path_from, is_add_file = 1, is_add_folder = 1, is_recur = 1)
		
		for item in items:
			new_item = item.replace(path_from, path_to)
		
			if os.path.isdir(item):
				if not os.path.exists(new_item):
					if os.listdir(item) == []:
						shutil.copytree(item, new_item)
				continue
		
			parent = new_item[ : new_item.rfind('/')]
			
			if not os.path.exists(parent):
				os.makedirs(parent)
			if os.path.exists(new_item):
				if is_overwrite == 0:
					messagebox.showerror ("Error", new_item + "\n\nAlready exist")
					return -1
				else:
					os.unlink(new_item)
			shutil.copy2(item, new_item)




	def clear_windows_cache(self):
		if os.name != 'nt':
			messagebox.showinfo("error", 'Clear Cache" only supports windows')
			return
		for root, subfolders, files in os.walk(r'C:\Users\Administrator\AppData\Local\Temp'):
			for file in files:
				path = root + '/' + file
				self.delete_single(path, including_read_only = 1, show_error = 0)
		messagebox.showinfo("info", "Windows cache cleared")
				
		


if __name__ == '__main__':
	fl = FileLib()
	a=r'g:\a'
	a=[(10, 15), (43, 1),(15, 2)]
	a=sorted(a)
	pprint.pprint(a)