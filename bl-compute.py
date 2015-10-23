#!/usr/bin/env python
"""
Battery Life Simulation for each benchmarks
	for use in Power Deregulation research
"""
__author__ = """Seunghoon Kim (ski819)"""
__date__ = "$Date: 2006-06-09 (Fri, 8 Jun 2006) $"
__revision__ = "Rev.2 Part of CS495-20 Project"
#    Written by 
#    Seunghoon Kim <seunghoon@northwestern.edu>
#	 Northwestern University
#
#	 Usage: ./bl-compute.py
#	

import powvolt
import battery

print "-------------------Battery Simulation--------------------\n"
benchmark = ['MPGdec', 'MPGenc', 'SpeechRec', 'ADPCMdec', 'ADPCMenc', 'epic', 'unepic', 'g721dec', 'g721enc']
voltage = [3.3, 3.206, 3.112, 3.018, 2.924, 2.83, 2.736]

for i in range(2):
	time_step = 1.0
	time = 0.0
	bat = battery.Li_MnO2_Battery()

	while bat.cap > 0.0:
		time += time_step
		power = powvolt.dereg(benchmark[i], bat.voltage())
	#	print (bat.cap / bat.cap_init)
	#	print bat.voltage()
	#	print power
		if power == 0.0:
			print "\nEstimated battery lifetime for", benchmark[i], ":", (time-1.0), "seconds"
			bat.cap = 0.0
		else:
			bat.deplete_capacity(power * time_step)

	print "----For regulated processor setup------------------------"
	for j in range(7):
		time_step = 1.0
		time = 0.0
		bat = battery.Li_MnO2_Battery()
		power = powvolt.reg(benchmark[i], j)
		while bat.cap > 0.0:
			time += time_step
			if bat.voltage() < (2.31):			# buck boost effect
				print "Operating at ", voltage[j], "volts :", (time-1.0), "seconds"
				bat.cap = 0.0
			else:
				bat.deplete_capacity((power/0.85) * time_step)	# conversion inefficiency effect
	print "---------------------------------------------------------"