#!/usr/bin/env python
"""
Power Data Extraction and Calculation Script for M5 Statistics

"""
__author__ = """Seunghoon Kim (ski819)"""
__date__ = "$Date: 2006-06-08 (Thurs, 8 Jun 2006) $"
__revision__ = "Rev.2 Part of CS495-20 Project"
#    Copyright (C) 2006 by 
#    Seunghoon Kim <seunghoon@northwestern.edu>
#
#	 Usage: ./powercalc.py (filename) (# of processors[max:4]) (Vdd[in V])
#	

import re, sys, math

#for line in fileinput.input():
	numbench = 9
	datapattern = re.compile(r'''(0m[0-9].*s)''')

if __name__ == '__main__':
#	readfile = sys.argv[1]
#	test = open(readfile, 'r')
#	string = test.read()
#	str = string.split()
	for line in fileinput.input():
		print re.compile(pattern, re.M), line.rstrip())

#	for i in range(numbench):
		# first value to fetch is the one that comes after this pattern
#		benchindex = str.index("------------------------------------")
#		print benchname[i], str[benchindex-5], str[benchindex-3], str[benchindex-1]
