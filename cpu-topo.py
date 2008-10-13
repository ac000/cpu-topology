#!/usr/bin/python
#
# cpu-topo.py
# Determine a systems CPU topology
#
# Andrew Clayton <andrew@digital-domain.net>
#
# GPLv2
#

import os, sys, re

# Number of physical cpus (distinct physical_id's)
num_pcpus  = 0
num_cores = 0
num_threads = 0
files     = []
# Dictionary to hold cpu topology; cpu number, number of cores
cpu_topo  = {}
# Previous physical_package_id
ppid = -2
# Previous core_id
pcid = -2


def print_summary():
	global num_pcpus, num_cores

	print
	print "Number of CPUs    = ",num_pcpus
	if num_cores == 1:
		print "Number of threads =  2"
	if num_cores > 1:
		print "Number of cores   = ",num_cores


# Check to see if we are UP or SMP
try:
	os.stat("/sys/devices/system/cpu/cpu0/topology")
except:
	print "System appears to be uni-processor"
	sys.exit(0)

# We appear to be SMP, get CPU topology information
for f in os.listdir("/sys/devices/system/cpu"):
	r = re.compile('cpu[0-9]+')
	if r.match(f):
		files.append(f)

files.sort()
for file in files:
	# get number of physical CPU's
	pfp = open("/sys/devices/system/cpu/"+file+"/topology/physical_package_id", 
																			"r")
	pid = pfp.read()
	
	if pid != ppid:
		num_pcpus += 1
		ppid = pid
		cpu_topo[pid] = 0
	
	cfp = open("/sys/devices/system/cpu/"+file+"/topology/core_id", "r")
	cid = cfp.read()

	if cid != pcid:
		num_cores += 1	
		pcid = cid
		try:
			cpu_topo[pid] += 1
		except:
			cpu_topo[pid] = 1


print "CPU Topology",

if num_cores < num_pcpus:
	num_cores = 0
	print "(SMP)\n"
	for k, v in cpu_topo.iteritems():
		print "CPU "+str(k),

	print_summary()
elif num_cores == num_pcpus:
	print "(SMP / Hyperthreaded)\n"
	for k, v in cpu_topo.iteritems():
		print "CPU "+str(k) +"    Threads: 2"

	print_summary()
else:
	if num_pcpus == 1:
		print "(Multicore)\n"
	else:
		print "(SMP / Multicore)\n"
	
	for k, v in cpu_topo.iteritems():
		print "CPU "+str(k) +"    Cores: "+ str(v)
	
	print_summary()
	
