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
if __name__ == '__main__':
	fname, numcpus, voltage = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
	frequency = (300 * (voltage-2.736) / 0.564) + 200
	print frequency
	if numcpus > 4:
		numcpus = 4
	test = open(fname, 'r')
	string = test.read()
	str = string.split()
	#print numcpus
	#print str

	dynparamstart = ["system.cpu0.POWER.DYNAMIC:bpred_block_average", 
	"system.cpu1.POWER.DYNAMIC:bpred_block_average", 
	"system.cpu2.POWER.DYNAMIC:bpred_block_average", 
	"system.cpu3.POWER.DYNAMIC:bpred_block_average"]
	dynparamend = ["system.cpu0.POWER.DYNAMIC:lsq_block_average", 
	"system.cpu1.POWER.DYNAMIC:lsq_block_average", 
	"system.cpu2.POWER.DYNAMIC:lsq_block_average", 
	"system.cpu3.POWER.DYNAMIC:lsq_block_average"]
	staparamstart = ["system.cpu0.POWER.STATIC:bpred_block_average", 
	"system.cpu1.POWER.STATIC:bpred_block_average", 
	"system.cpu2.POWER.STATIC:bpred_block_average", 
	"system.cpu3.POWER.STATIC:bpred_block_average"]
	staparamend = ["system.cpu0.POWER.STATIC:lsq_block_average", 
	"system.cpu1.POWER.STATIC:lsq_block_average", 
	"system.cpu2.POWER.STATIC:lsq_block_average", 
	"system.cpu3.POWER.STATIC:lsq_block_average"]
	dynpower = [0.0,0.0,0.0,0.0]
	stapower = [0.0,0.0,0.0,0.0]		# Initialize an array in length of 4
	dyntotal = 0.0
	statotal = 0.0

	for i in range(numcpus):
		# first value to fetch is the one that comes after this pattern
		dynindex = str.index(dynparamstart[i]) + 1
		dynend = str.index(dynparamend[i]) + 1
		while dynindex < dynend:
			dynpower[i] += float(str[dynindex])
			dynindex =  dynindex + 4
		print "Dynamic Power for Processor", i, " sums upto: ", dynpower[i]
		dyntotal += dynpower[i]

		# Similarly for static power
		staindex = str.index(staparamstart[i]) + 1
		staend = str.index(staparamend[i]) + 1
		while staindex < staend:
			stapower[i] += float(str[staindex])
			staindex += 4	
		print "Static Power for Processor", i, " sums upto: ", stapower[i]
		statotal += stapower[i]
	
	print "Total Dynamic Power: ", dyntotal
	print "Scaled according to", voltage, "V and", frequency, "MHz:", (dyntotal*voltage*voltage*frequency/3.3/3.3/500)
	print "Total Static Power: ", statotal
	print "Scaled according to", voltage, "V:", (statotal*math.exp(3.3-voltage))
	totalpower = (dyntotal*voltage*voltage*frequency/3.3/3.3/500) + (statotal*math.exp(3.3-voltage))
	print "Overall Power Dissipation for", numcpus, "processors running at", voltage, "volts and", \
		frequency, "MHz:", totalpower, "W"
