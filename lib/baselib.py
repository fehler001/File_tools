#coding=utf-8
#File_tools/lib/baselib.py

import os
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font, nametofont
import random
import shutil
import stat
import codecs
import base64
import html
from encodings.aliases import aliases
import pprint
import time
import datetime
import binascii
import hashlib

# third party
import chardet
import crcmod


class BaseLib():

	def __init__(self):
		super().__init__()

		self.date_unit = ['year', 'month', 'day', 'hour', 'minute', 'second']
		self.date_format = '%Y.%m.%d.%H.%M.%S'
		#self.year_mktime = 365*24*3600 + 5*3600 + 48*60 + 46
		self.year_mktime = 365.25*24*3600
		self.ascii = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'




	def increase_one_by_dict(self, string, dict):   # e.g.  dict = '123456789'
		str = string
		l = len(str)
	
		if str[-1] == dict[-1]:       #  if  '99'  [-1] is '9'        
			str = str[ : -1] + dict[0]    #  '99'  ->  '91'  
			for i in range( l ):     #  l = 2
				if abs(-i-2) > l:     #  if i = 1,  abs(-i-2) = 3 > 2
					str = dict[0] + str      #  after '99' -> '91' -> '11',   '11'  ->  '111'
					break
				else:
					if str[-i-2] == dict[-1]:   # if i = 0,  after '99' -> '91',  [-i-2] is '9' == dict[-1]
						str = str[ : -i-2] + dict[ 0 ] + str[ -i-1 : ]     #  '91' -> '11'
					else:									# if i = 0,  '79',   after '79' -> '71',  [-i-2] is '7' != dict[-1]
						str = str[ : -i-2] + dict[ dict.index(str[-i-2]) + 1 ] + str[ -i-1 : ]     #  '71' -> '81'
						break					
		else:    #  if  '95'  [-1] is '5' != dict[-1]
			str = str[ : -1] + dict[ dict.index(str[-1]) + 1 ]      #   '95'  ->  '96'

		return str



	def get_crc(self, input, mode = 'crc-32'):
		if type(input) == int:
			input = str(int(input))
		if type(input) == str:
			b_data = self.str_encode(input)   # b_data = binascii.unhexlify('aaaa')  ascii to bytes  => b'\xaa\xaa'
		if type(input) == bytes:
			b_data = input
		crc_data = crcmod.predefined.Crc(mode)
		crc_data.update(b_data)
		rst = hex(crc_data.crcValue)
		return rst



	def get_md5(self, input):
		if type(input) == int:
			input = str(int(input))
		if type(input) == str:
			b_data = self.str_encode(input)
		if type(input) == bytes:
			b_data = input

		key = hashlib.md5()  # could fill a bytes to custom a key, like: b'1234567'
		key.update(b_data)
		rst = key.hexdigest()
		return rst


	def get_sha1(self, input):
		if type(input) == int:
			input = str(int(input))
		if type(input) == str:
			b_data = self.str_encode(input)
		if type(input) == bytes:
			b_data = input

		key = hashlib.sha1()
		key.update(b_data)
		rst = key.hexdigest()
		return rst


	def get_sha256(self, input):
		if type(input) == int:
			input = str(int(input))
		if type(input) == str:
			b_data = self.str_encode(input)
		if type(input) == bytes:
			b_data = input

		key = hashlib.sha256()
		key.update(b_data)
		rst = key.hexdigest()
		return rst


	def get_sha384(self, input):
		if type(input) == int:
			input = str(int(input))
		if type(input) == str:
			b_data = self.str_encode(input)
		if type(input) == bytes:
			b_data = input

		key = hashlib.sha384()
		key.update(b_data)
		rst = key.hexdigest()
		return rst


	def get_sha512(self, input):
		if type(input) == int:
			input = str(int(input))
		if type(input) == str:
			b_data = self.str_encode(input)
		if type(input) == bytes:
			b_data = input

		key = hashlib.sha512()
		key.update(b_data)
		rst = key.hexdigest()
		return rst



	def get_checksum(self, input, mode):
		if mode == 'MD5':
			return self.get_md5(input)
		if mode == 'SHA1':
			return self.get_sha1(input)
		if mode == 'SHA256':
			return self.get_sha256(input)
		if mode == 'SHA384':
			return self.get_sha384(input)
		if mode == 'SHA512':
			return self.get_sha512(input)
		if mode == 'MD5':
			return self.get_md5(input)
		if mode == 'CRC-8':
			return self.get_crc(input, 'crc-8')
		if mode == 'CRC-16':
			return self.get_crc(input, 'crc-16')
		if mode == 'CRC-32':
			return self.get_crc(input, 'crc-32')
		if mode == 'CRC-64':
			return self.get_crc(input, 'crc-64')



	def check_legit_int(self, cont):
		try:
			int(cont)
		except:
			messagebox.showerror ("NUMERIC ERROR", 'Please fill a number. (like "1", "3")')
			return -1


	def check_legit_string(self, cont):
		illegal = ['/', '\\', ':', '*', '"', '<', '>', '|', '?']
		for c in cont:
			if c in illegal:
				messagebox.showerror ("STRING ERROR", "['/', '\\', ':', '*', '\"', '<', '>', '|', '?'] are not allowed")
				return -1


	def check_has_repeat(self, list):
		l2 = []
		for item in list:
			if item in l2:
				messagebox.showerror ("REPEAT ERROR", "Got same name file !\n\n" + '"' + item + '"')
				return -1
			l2.append(item)



	def clean_list(self, list, is_repeat = 0, is_sort = 0):
		all = []
		if is_repeat == 1:
			list = set(list)
		if is_sort == 1:
			list = sorted(list, key = self.natsort_key2)
		for item in list:
			if item == '' or item == '\n':
				continue
			all.append(item)
		return all




	def str_encode(self, string, enc = 'utf-8'):
		str = string.strip()
		if enc == 'hex':
			return hex(int(str))
		if enc == 'binary':
			return bin(int(str))
		if enc == 'ascii-hex':
			b = bytes(str, 'ascii')
			return  binascii.hexlify(b)   # binascii.hexlify(b'A') = hex(ord('A'))
		if enc == 'html':
			return html.escape(str)
		if enc == 'base64':
			rst_b = base64.b64encode(str.encode("utf-8"))
			rst = str(rst_b, "utf-8")
			#rst_b = base64.urlsafe_b64encode(string.encode("utf-8"))   # safe encode in base64
			#rst = str(rst_b, "utf-8")
			return rst
		rst = codecs.encode(str, encoding = enc, errors = 'backslashreplace')
		return rst


	def bytes_decode(self, binary, enc = 'utf-8'):
		rst = codecs.decode(binary, encoding = enc, errors = 'backslashreplace')
		return rst


	def str_decode(self, string, enc = 'utf-8'):
		if string[0:2] == "b'" and string[-1] == "'":
			str = string[2:-1]
		else:
			str = string
		if enc == 'int':
			return int(str)
		if enc == 'ascii-unhex':
			return  binascii.unhexlify(str)     # binascii.unhexlify(41) = chr(int(0x41))
		if enc == 'html':
			return html.unescape(str)
		if enc == 'base64':
			rst = ''
			strs = str.split('\n')
			for str in strs:
				b = base64.b64decode(str)
				rst = rst + codecs.decode(b, encoding = 'utf-8', errors = 'backslashreplace')
			return rst
		else:
			b = eval('b' + "'" + str + "'")		
		rst = codecs.decode(b, encoding = enc, errors = 'backslashreplace')
		return rst


	def str_transcode(self, string, enc_from = 'utf-8', enc_to = 'utf-8'):
		b = self.str_encode(string, enc = enc_from)
		rst = self.bytes_decode(b, enc = enc_to)
		return rst



	def guess_encoding_binary(self, binary):
		return chardet.detect(binary)




	def date_unit_to_mktime(self, unit):
		u = unit.lower()
		if u not in self.date_unit:
			messagebox.showerror ("ERROR", '"Unit" error !')
			return -1
		if u == 'year': return self.year_mktime
		if u == 'month': return self.year_mktime/12
		if u == 'day': return 3600*24
		if u == 'hour': return 3600
		if u == 'minute': return 60
		if u == 'second': return 1



	def get_path_date(self, path):
		try:
			now = time.localtime()
			ctime = os.path.getctime(path)
			mtime = os.path.getmtime(path)
			atime = os.path.getatime(path)
			ctime += 3600 * (now.tm_isdst - time.localtime(ctime).tm_isdst)
			mtime += 3600 * (now.tm_isdst - time.localtime(mtime).tm_isdst)
			atime += 3600 * (now.tm_isdst - time.localtime(atime).tm_isdst)

			sctime = time.strftime(self.date_format, time.localtime(ctime))
			smtime = time.strftime(self.date_format, time.localtime(mtime))
			satime = time.strftime(self.date_format, time.localtime(atime))
			return {'ctime':ctime, 'mtime':mtime, 'atime':atime, 'sctime':sctime, 'smtime':smtime, 'satime':satime}
		except:
			return {'ctime':'', 'mtime':'', 'atime':'', 'sctime':'', 'smtime':'', 'satime':''}



	def modify_date(self, path, atime, mtime):
		os.chmod(path, stat.S_IRWXU)
		os.utime(path, (atime, time))  # (accessed time, modified time)



	# path must use '/'
	# 'c:/a.txt'  i1 = index '/', i2 = index '.', filename = 'a.txt', name = 'a', ext = '.txt'
	def get_path_info(self, path, is_size = 0):
		if os.path.isfile(path):
			if is_size == 1:
				size = os.path.getsize(path)
			else:
				size = ''
			i = path.rfind(r'/')
			i2 = path.rfind('.')
			parent = path[ :i]
			filename = path[i+1: ]
			if i2 != -1 and i2 > i:
				name = path[i+1 : i2]
				ext = path[i2: ]
				return {'/':i, '.':i2, 'parent':parent, 'filename':filename, 'name':name, 'ext':ext, 'isfile':1, 'isdir':0, 'is_exist':1, 'size':size}
			if i2 == -1 or i2 < i:
				name = path[i+1: ]
				return {'/':i, '.':len(path), 'filename':filename, 'parent':parent, 'name':name, 'ext':'', 'isfile':1, 'isdir':0, 'is_exist':1, 'size':size}
		if os.path.isdir(path):
			if is_size == 1:
				size = self.get_folder_size(path)
			else:
				size = ''
			i = path.rfind(r'/')
			parent = path[ :i]
			filename = path[i+1: ]
			return {'/':i, '.':len(path), 'filename':filename, 'parent':parent, 'name':filename, 'ext':'', 'isfile':0, 'isdir':1, 'is_exist':1, 'size':size}
		return {'/':0, '.':len(path), 'filename':path, 'parent':'', 'name':path, 'ext':'', 'isfile':0, 'isdir':0, 'is_exist':0, 'size':''}



	def check_path_exist(self, list, isfile = 0):
		if type(list) == str:
			list = [list]
		for path in list:
			if path == '' or path == '\n':
				continue
			pinfo = self.get_path_info(path)
			if pinfo['is_exist'] == 0:
				messagebox.showerror ("ERROR", '"' + path + '"' + '\n\ndoes not exist !')
				return -1
			if isfile == 1:
				if pinfo['isfile'] == 0:
					messagebox.showerror ("ERROR", '"' + path + '"' + '\n\nis not a file !')
					return -1



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



	# length = 5, digit = 3, outset = 1  =>  [001,002,003,004,005]
	def generate_ordinal(self, length, digit = 1, outset = 0, interval = 1):
		all = []
		n = 0 + outset
		for i in range(length):
			if n >= 0:
				all.append( '0'*(digit - len(str(n)) ) + str(n) )
			else:
				all.append('-' + '0'*(digit - len(str(n)) + 1) + str(abs(n)) )
			n = n + interval
		return all



	# return ['2001-01-01_0.0.0', '2001-01-01_0.1.0', ...... ]
	def generate_date_ordinal(self, length, outset = '2001.01.01.12.0.0', output_format = '%Y-%m-%d_%H.%M.%S', 
						   interval = 60, unit = 'second', is_str = 1, is_mktime = 0):
		all = []
		
		if unit == 'year' or unit == 'month':
			for i in range(length):
				dt = outset.split('.')
				if unit == 'year':
					dt[0] = str( int(dt[0]) + interval*i )
				if unit == 'month':
					if (int(dt[1]) + interval*i) > 12:
						if (int(dt[1]) + interval*i) % 12 == 0:
							dt[0] = str( int(dt[0]) + (int(dt[1]) + interval*i) / 12 - 1 ).split('.')[0]
							dt[1] = '01'
						else:
							dt[0] = str( int(dt[0]) + (int(dt[1]) + interval*i) / 12 ).split('.')[0]
							dt[1] = str( (int(dt[1]) + interval*i) % 12 )
					else:
						dt[1] = str( int(dt[1]) + interval*i )
				t3 = dt[0] + '.' + dt[1] + '.' + dt[2] + '.' + dt[3] + '.' + dt[4] + '.' + dt[5]
				try:
					t2 = time.strptime(t3, self.date_format)
				except:
					messagebox.showerror ("ERROR", '"' + t3 + '"' +  
							   '\n\nExceed system date range !')
					return -1
				if is_mktime == 1:
					t1 = time.mktime(t2)
					all.append(t1)
				if is_str == 1:
					all.append( time.strftime(output_format, t2) )

		else:
			t2 = time.strptime(outset, self.date_format)
			t1 = time.mktime(t2)
			us = interval * self.date_unit_to_mktime(unit) # 'second' - 'day' unit to second
			for i in range(length):
				if is_mktime == 1:
					tmp2 = t1 + us*i
				if is_str == 1:
					try:
						tmp1 = time.localtime( t1 + us*i )    # localtime is like this # (tm_year=2017, tm_mon=2, tm_mday=4, ...
					except:
						messagebox.showerror ("ERROR", '"' + tmp2 + '" + ' + str(interval) +  '" * ' + unit + '"' + 
							   '\n\nExceed system date range !')
						return -1
					tmp2 = time.strftime(output_format, tmp1)
				all.append(tmp2)
		return all



	def check_date_range(self, dates, max = '', min = '', format = ''):

		if format == '':
			f = self.date_format
		else:
			f = format

		if max == '':
			t3 = '2099.12.31.12.0.0'
		try:
			t2 = time.strptime(t3, self.date_format)
			max = time.mktime(t2)
		except:
			pass
		max_dt2 = time.localtime(max)
		max_dt3 = time.strftime(f, max_dt2)

		if min == '':
			t3 = '1980.01.01.12.0.0'
		try:
			t2 = time.strptime(t3, self.date_format)
			min = time.mktime(t2)
		except:
			pass
		min_dt2 = time.localtime(min)
		min_dt3 = time.strftime(f, min_dt2)

		for date in dates:
			try:
				t2 = time.strptime(date, f)
				mk = time.mktime(t2)
			except:
				mk = date
			if mk > max or mk < min:
				dt2 = time.localtime(mk)
				dt1 = time.strftime(self.date_format, dt2)
				messagebox.showerror ("ERROR", '"' + str(dt1) + '"' + '  exceed system date range !' + 
					'\n\nPlease set between\n\n' + '"' + str(min_dt3) + '"' + ' - ' + '"' + str(max_dt3) + '"')
				return -1



if __name__ == '__main__':
	bl = BaseLib()
	f=open(r'G:\TDDOWNLOAD\Devil May Cry 5 [FitGirl Repack]\fg-selective-english.bin', mode='rb')
	a=f.read()
	#a='1234'
	#b=bl.get_sha512(a)
	print(b)



#date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
#mktime = time.mktime(date.timetuple())