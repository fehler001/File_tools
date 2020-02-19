#coding=utf-8
#File_tools/lib/firewalllib.py


import sys
import os
from tkinter import messagebox
import random
import shutil
import stat
import subprocess
	
from natsort import natsort_keygen, ns
try:
	import lib.baselib, lib.filelib
except:
	import baselib, filelib


# this lib only support windows
class FirewallLib():

	def __init__(self):
		super().__init__()

		try:
			self.bl = lib.baselib.BaseLib()
			self.fl = lib.filelib.FileLib()
		except:
			self.bl = baselib.BaseLib()
			self.fl = filelib.FileLib()

		self.firewall_rule_log_in = r'c:\temp\you_can_delete_me_in.txt'
		self.firewall_rule_log_out = r'c:\temp\you_can_delete_me_out.txt'
		self.test = r'c:\temp\1.txt'


	
	def create_log_current_rules_in(self):
		self.delete_log()
		subprocess.run(["powershell.exe", 
				  r'netsh advfirewall firewall show rule name=all dir=in type=dynamic | Out-File -Append ' + self.firewall_rule_log_in])



	def create_log_current_rules_out(self):
		self.delete_log()
		subprocess.run(["powershell.exe", 
				  r'netsh advfirewall firewall show rule name=all dir=out type=dynamic | Out-File -Append ' + self.firewall_rule_log_out])




	def read_log_file_out(self):
		if os.path.isfile(self.firewall_rule_log_out):
			current_rules_out = []
			f = open(self.firewall_rule_log_out, 'r', encoding = 'utf-16')  # powershell use utf-16 to output
			lines = f.readlines()
			f.close()
			for line in lines:
				if 'Rule Name:' in line:
					line = line[15:].strip()   # .strip() will strip double end all space and enter
					current_rules_out.append( line.replace('\\', '/') )       # '\' could get match error
			return current_rules_out



	def read_log_file_in(self):
		if os.path.isfile(self.firewall_rule_log_in):
			current_rules_in = []
			f = open(self.firewall_rule_log_in, 'r', encoding = 'utf-16')  # powershell use utf-16 to output
			lines = f.readlines()
			f.close()
			for line in lines:
				if 'Rule Name:' in line:
					line = line[15:].strip()   # .strip() will strip double end all space and enter
					current_rules_in.append( line.replace('\\', '/') )        # '\' could get match error
			return current_rules_in
	

	
	def delete_log(self):
		try:
			os.chmod(self.firewall_rule_log_in, stat.S_IRWXU)
			os.remove(self.firewall_rule_log_in)
		except:
			pass
		try:
			os.chmod(self.firewall_rule_log_out, stat.S_IRWXU)
			os.remove(self.firewall_rule_log_out)
		except:
			pass
	
	

	def add_one_rule_out(self, rule_name):
		name = rule_name.replace('/', '\\')    # powershell doesn't support '/'
		subprocess.run(["powershell.exe", 
				  'netsh advfirewall firewall add rule name="%s" dir=out program="%s" action=block' %(name, name)])
	


	def add_one_rule_in(self, rule_name):
		name = rule_name.replace('/', '\\')
		subprocess.run(["powershell.exe", 
				  'netsh advfirewall firewall add rule name="%s" dir=in program="%s" action=block' %(name, name)])

	
	# bypass list[] to here
	def add_rules(self, files, is_in = 0, is_out = 1):
		fs = []
		n_in = 0
		n_out = 0
		for file in files:
			if file == '' or file == '\n':
				continue
			file = file.strip()
			if self.bl.get_path_info(file)['isfile'] == 0:
				messagebox.showerror ("ERROR", '"' + file + '"' + '\n\nIs not a file ! ')
				return -1
			fs.append(file)
		if is_out == 1:
			self.create_log_current_rules_out()
			log_out = self.read_log_file_out()
			for f in fs:
				if f not in log_out:
					self.add_one_rule_out(f)
					n_out = n_out + 1
		if is_in == 1:
			self.create_log_current_rules_in()
			log_in = self.read_log_file_in()
			for f in fs:
				if f not in log_in:
					self.add_one_rule_in(files)
					n_in = n_in + 1
		self.delete_log()
		messagebox.showinfo("Complete", \
			str(n_out) + ' files added to firewall outbound rule !\n\n' + \
			str(n_in) + ' files added to firewall inbound rule !\n\n' + \
			'You can go check at \n' + \
			'"system setting - network - firewall - advanced"')



	def open_window_firewall_advanced(self):
		subprocess.run(["powershell.exe", 
				  "c:\windows\system32\WF.msc"])




if __name__ == '__main__':
	fwl = FirewallLib()
	fwl.add_rules(['c:/program files (x86)/adobe/adobe captivate quiz results analyzer 9/adobe captivate quiz results analyzer 9.exe'])
	#subprocess.run(["powershell.exe", "c:/program files (x86)/adobe/adobe captivate quiz results analyzer 9/adobe captivate quiz results analyzer 9.exe"])
	#fwl.open_window_firewall_advanced()

	#cmd
	#os.system(r'netsh advfirewall firewall show rule name=all dir=out type=dynamic>>' + self.log1)
	#os.system('netsh advfirewall firewall add rule name="%s" dir=out program="%s" action=block' %(dir1, dir1))

