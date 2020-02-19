#coding=utf-8
#File_tools/file/__init__.py

import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog 
import os
import sys
import json

import file.Rename
import file.Date
import file.Refine_enfold
import file.Remove_empty_folder
import file.Filter
import file.Find
import file.Move_copy_delete
import file.Checksum




class File( file.Rename.CreateFrameRename,
			file.Date.CreateFrameDate,
			file.Refine_enfold.CreateFrameRefine,
			file.Remove_empty_folder.CreateFrameRemove,
			file.Filter.CreateFrameFilter,
			file.Find.CreateFrameFind,
			file.Move_copy_delete.CreateFrameMove,
			file.Checksum.CreateFrameCsum
			):

	def __init__(self):
		super().__init__()

		self.FileRoot =  None



	def FileDefault(self):
		
		self.CreateWidgetsFrameFile()

		self.RenameRoot = self.FrameRename
		self.RenameDefault()
		self.DateRoot = self.FrameDate
		self.DateDefault()
		self.RefineRoot = self.FrameRefine
		self.RefineDefault()
		self.RemoveRoot = self.FrameRemove
		self.RemoveDefault()
		self.FilterRoot = self.FrameFilter
		self.FilterDefault()
		self.FindRoot = self.FrameFind
		self.FindDefault()
		self.MoveRoot = self.FrameMove
		self.MoveDefault()
		self.CsumRoot = self.FrameCsum
		self.CsumDefault()




	def CreateWidgetsFrameFile(self):
		
		# start Notebook01
		self.FrameRename = Frame(self.FileRoot)
		self.FrameRename.pack(fill = BOTH)
		self.FileRoot.add(self.FrameRename, text='Rename ')

		self.FrameDate = Frame(self.FileRoot)
		self.FrameDate.pack(fill = BOTH)
		self.FileRoot.add(self.FrameDate, text='Date ')
		
		self.FrameRefine = Frame(self.FileRoot)
		self.FrameRefine.pack(fill = BOTH)
		self.FileRoot.add(self.FrameRefine, text='Refine Enfold')
		
		self.FrameRemove = Frame(self.FileRoot)
		self.FrameRemove.pack(fill = BOTH)
		self.FileRoot.add(self.FrameRemove, text='Remove Empty')
		
		self.FrameFilter = Frame(self.FileRoot)
		self.FrameFilter.pack(fill = BOTH)
		self.FileRoot.add(self.FrameFilter, text='Filter ')
		
		self.FrameFind = Frame(self.FileRoot)
		self.FrameFind.pack(fill = BOTH)
		self.FileRoot.add(self.FrameFind, text='Find ')
		
		self.FrameMove = Frame(self.FileRoot)
		self.FrameMove.pack(fill = BOTH)
		self.FileRoot.add(self.FrameMove, text='Move ')

		self.FrameCsum = Frame(self.FileRoot)
		self.FrameCsum.pack(fill = BOTH)
		self.FileRoot.add(self.FrameCsum, text='Checksum')
		# end Notebook01



