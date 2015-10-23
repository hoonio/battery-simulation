#!/usr/bin/env python

'''Plot relative battery lifes of regulated and deregulated approaches as
functions of initial voltage and footprint based on the following assumptions:
  1) Equal footprints (twice the area allowed for deregulated)
  2) The workload is that requiring all the deregulated cores at minimal voltage.
'''

# Justify vmin with DRAM low.
vmin = 1.8
bat_capacity = 600.0 * 1E-3 * 60.0 * 60.0 * 4 # Ws
conv_eff = 0.85
parallel_eff = 0.85
reg_system_r = 5.0 # Ohm
leakage = 0.00
cutout = 0.85

import math
import shutil
import os
import sys


def frange(a, b, inc):
	return (a + i * inc for i in range(int(math.ceil((b - a) / inc))))


def actual_work(proc):
	return proc ** parallel_eff


def actual_proc(work):
	return math.ceil(work ** (1.0 / parallel_eff))




class Multicore(object):
	time_step = 2.0

	def __init__(self, bat, proc_cnt, tot_r, work_rate):
		# Work rate is for all processors at 1 volt
		self.bat = bat
		self.proc_cnt = proc_cnt
		self.tot_r = tot_r
		self.work_rate = work_rate
		self.leakage_i = leakage * bat.voltage() / tot_r
		self.run_time_s = 0.0
		while self.functioning():
			cap_step = self.power() * self.time_step
			self.bat.deplete_capacity(cap_step)
			self.run_time_s += self.time_step


class RegMC(Multicore):
	def __init__(self, bat, proc_cnt, tot_r, work_rate, conv_eff):
		self.conv_eff = conv_eff
		self.outvolt = work_rate / actual_work(proc_cnt)
		Multicore.__init__(self, bat, proc_cnt, tot_r, work_rate)

	def functioning(self):
		return self.bat.cap > 0.0 and self.bat.voltage() * cutout > self.outvolt

	def power(self):
		leak_p = self.leakage_i * self.outvolt
		dyn_p = self.outvolt ** 2.0 / self.tot_r / conv_eff
#		print leak_p / dyn_p
		return leak_p + dyn_p


class DeregMC(Multicore):
	def __init__(self, bat, proc_cnt, tot_r, work_rate, vmin):
		self.vmin = vmin
		Multicore.__init__(self, bat, proc_cnt, tot_r, work_rate)

	def functioning(self):
		return self.bat.cap > 0.0 and self.bat.voltage() > self.vmin

	def power(self):
		proc = actual_proc(self.work_rate / self.bat.voltage())
#		print proc, self.proc_cnt
		proc_rat = proc / self.proc_cnt
		leak_p = self.leakage_i * self.bat.voltage() * proc_rat
		dyn_p = self.bat.voltage() ** 2.0 / self.tot_r * proc_rat
#		print leak_p / dyn_p
		return leak_p + dyn_p


def fname(bname, bat_type_i, val, suffix):
	return bname + str(bat_type_i) + ('a%.2f' % val) + '.' + suffix

cmp_min = {}
cmp_max = {}

def gen_data(dereg_reg_area_ratio):
	cmp_min[dereg_reg_area_ratio] = 0.0
	cmp_max[dereg_reg_area_ratio] = 0.0
	for bat_type_i in range(len(bat_types)):
		reg_f = open(fname('reg', bat_type_i, dereg_reg_area_ratio, 'data'), 'w')
		dereg_f = open(fname('dereg', bat_type_i, dereg_reg_area_ratio, 'data'), 'w')
		cmp_f = open(fname('cmp', bat_type_i, dereg_reg_area_ratio, 'data'), 'w')	
		for dereg_proc_cnt in range(1, 17):
			reg_proc_cnt = int(dereg_proc_cnt / dereg_reg_area_ratio)
			if reg_proc_cnt == 0:
				continue
			work_rate = actual_work(dereg_proc_cnt) * vmin
			bat_type = bat_types[bat_type_i]
			reg = RegMC(bat_type(bat_capacity), reg_proc_cnt, reg_system_r,
				work_rate, conv_eff)
			if reg.run_time_s != 0:
				dereg = DeregMC(bat_type(bat_capacity), dereg_proc_cnt,
					reg_system_r / dereg_reg_area_ratio, work_rate, vmin)
				reg_f.write('%d %d %f\n' % (reg_proc_cnt, bat_type_i,
					reg.run_time_s / 60.0))
				dereg_f.write('%d %d %f\n' % (dereg_proc_cnt, bat_type_i,
					dereg.run_time_s / 60.0))
				val = 100.0 * (dereg.run_time_s - reg.run_time_s) / reg.run_time_s
				cmp_f.write('%d %f\n' % (dereg_proc_cnt, val))
				cmp_min[dereg_reg_area_ratio] = \
					min(cmp_min[dereg_reg_area_ratio], val)
				cmp_max[dereg_reg_area_ratio] = \
					max(cmp_max[dereg_reg_area_ratio], val)
		reg_f.write('\n\n')
		dereg_f.write('\n\n')
		cmp_f.write('\n\n')


# Plot the discharge curves
for bti in range(len(bat_types)):
	f = file('discharge%d.data' % bti, 'w')
	for x, y in bat_types[bti].table:
		f.write('%e %e\n' % (x * 100.0, y))
	f.close()

f = file('discharge.gp', 'w')
f.write('''set terminal postscript eps enhanced
#set title 'Battery discharge curves'
set xlabel 'Remaining capacity (%)'
set xrange [100:0]
set ylabel 'Voltage (V)'
''')
all_plt = ', \\\n'.join("'discharge%d.data' w l t '%s'" % (i, bat_types[i].name)
	for i in range(len(bat_types)))
f.write('plot ' + all_plt + '\n')
f.close()

os.system('gnuplot < discharge.gp > discharge.eps')

for dereg_reg_area_ratio in frange(1.0, 1.5, 0.05):
	gen_data(dereg_reg_area_ratio)
	gpfile = 'cmp' + ('%.2f' % dereg_reg_area_ratio) + '.gp'
	shutil.copyfile('cmp.gp', gpfile)
	f = file(gpfile, 'a')
	f.write('plot ')
	f.write(', \\\n'.join("'" + fname('cmp', i, dereg_reg_area_ratio, 'data') +
		"' w l t '" + bat_types[i].name + "'"
		for i in range(len(bat_types))))
	f.write('\n')
	f.close()
	os.system('gnuplot < ' + gpfile + ' > ' +
		'cmp' + ('%.2f' % dereg_reg_area_ratio) + '.eps')
