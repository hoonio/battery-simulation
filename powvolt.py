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
#	 To be used with bl-compute.py
#	

_bench_proc = { \
	'MPGdec': [(3.3, 3.3899), (3.206, 3.2257), (3.112, 4.0918), (3.018, 3.7903), \
				(2.924, 3.603), (2.83, 4.248), (2.736, 5.088)], \
	'MPGenc': [(3.3, 3.3899), (3.206, 3.209), (3.112, 3.3596), (3.018, 3.2138), \
				(2.924, 3.0452), (2.83, 2.9301), (2.736, 2.912), (2.52, 2.912)], \
	'SpeechRec': [(3.3, 3.3899), (3.206, 3.209), (3.112, 3.3596), (3.018, 3.2138), \
				(2.924, 3.0452), (2.83, 3.9301), (2.736, 3.3232)], \
	'ADPCMdec': [(3.3, 3.3899), (3.206, 3.209), (3.112, 3.3596), (3.018, 3.2138), \
				(2.924, 3.0452), (2.83, 3.9301), (2.736, 3.3232)], \
	'ADPCMenc': [(3.3, 3.3899), (3.206, 3.209), (3.112, 3.3596), (3.018, 3.2138), \
				(2.924, 3.0452), (2.83, 3.9301), (2.736, 3.3232)], \
	'epic': [(3.3, 3.3899), (3.206, 3.209), (3.112, 3.3596), (3.018, 3.2138), \
				(2.924, 3.0452), (2.83, 3.9301), (2.736, 3.3232)], \
	'unepic': [(3.3, 3.3899), (3.206, 3.209), (3.112, 3.3596), (3.018, 3.2138), \
				(2.924, 3.0452), (2.83, 3.9301), (2.736, 3.3232)], \
	'g721dec': [(3.3, 3.3899), (3.206, 3.209), (3.112, 3.3596), (3.018, 3.2138), \
				(2.924, 3.0452), (2.83, 3.9301), (2.736, 3.3232)], \
	'g721enc': [(3.3, 3.3899), (3.206, 3.209), (3.112, 3.3596), (3.018, 3.2138), \
				(2.924, 3.0452), (2.83, 3.9301), (2.736, 3.3232)], \
}

#_power_cons = [(3.3, 3.3899), (3.206, 3.209), (3.112, 3.3596), (3.018, 3.2138), 
#		(2.924, 3.0452), (2.83, 3.9301), (2.736, 3.3232)]

def benchmark_proc(bench, voltage):
	v_to_proc_cnt = _bench_proc[bench]
	for v, numcpus in v_to_proc_cnt:
		if v < voltage:
			return numcpus
	return 1

def reg(bench, num):
	reg_power = _bench_proc[bench]
	return (reg_power[num][1])

def dereg(bench, voltage):
	v_to_power_cnt = _bench_proc[bench]
	for v, power in v_to_power_cnt:
		if voltage > v:
			return power
	return 0.0

#def power_voltage(bench, voltage):
	#numcpus = benchmark_proc(bench, voltage)		# Find out number of CPUs used at specific voltage level
	#single_proc_p(voltage)
#	return (proc_power(bench, voltage))