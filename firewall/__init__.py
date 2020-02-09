#coding=utf-8
#File_tools/firewall/__init__.py


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


import firewall.Add_rule


class Firewall(firewall.Add_rule.CreateFrameARule):

	def __init__(self):
		super().__init__()
		
		self.FirewallRoot = None


	def FirewallDefault(self):

		self.CreateWidgetsFrameFirewall()

		self.ARuleRoot = self.FrameARule
		self.ARuleDefault()



	def CreateWidgetsFrameFirewall(self):

		self.FrameARule = Frame(self.FirewallRoot)
		self.FrameARule.pack(fill = BOTH)
		self.FirewallRoot.add(self.FrameARule, text='firewall Add Rules')