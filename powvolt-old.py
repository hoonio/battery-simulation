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
	'MPGdec': [(3.3, 1), (3.112, 2), (2.83, 3), (2.736, 4)], \
	'MPGenc': [(3.3, 1), (3.112, 2), (2.736, 3)], \
	'SpeechRec': [(3.3, 1), (3.112, 2), (2.736, 3)], \
	'ADPCMdec': [(3.3, 1), (3.112, 2), (2.83, 3)], \
	'ADPCMenc': [(3.3, 1), (3.112, 2), (2.736, 3)], \
	'epic': [(3.3, 1), (3.112, 2), (2.924, 3)], \
	'unepic': [(3.3, 1), (3.112, 2), (2.736, 3)], \
	'g721dec': [(3.3, 1), (3.112, 2), (2.83, 3)], \
	'g721enc': [(3.3, 1), (3.112, 2), (2.736, 3)] \
}

_power_cons = [(3.3, 3.3899), (3.206, 2.9031), (3.112, 2.4551), (3.018, 2.04677), 
		(2.924, 1.67705), (2.83, 1.3415), (2.736, 1.0408)]

def benchmark_proc(bench, voltage):
	v_to_proc_cnt = _bench_proc[bench]
	for v, numcpus in v_to_proc_cnt:
		if v < voltage:
			return numcpus
	return 1

def single_proc_p(voltage):
	v_to_power_cnt = _power_cons
	for v, power in v_to_power_cnt:
		if v > voltage:
			return power

def power_voltage(bench, voltage):
	numcpus = benchmark_proc(bench, voltage)		# Find out number of CPUs used at specific voltage level
#	single_proc_p(voltage)
	return (float(numcpus) * single_proc_p(voltage))