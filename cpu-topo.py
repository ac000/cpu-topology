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

# Dictionary to hold physical cpus and number of cores
cpus  = {}

files = []
# Core id
cid   = 0;
# Number of physical CPUs
physical_cpus = 0
# Number of logical CPUs, cores/threads or otherwise
logical_cpus  = 0

def print_summary(type):
	global physical_cpus, logical_cpus

	print "\nNumber of CPUs    =  ",physical_cpus
	if type == "SMP":
		sys.exit()
	if type == "HYP":
		print "Number of threads =  ",logical_cpus
		sys.exit()
	if type == "SMPMUL":
		print "Number of cores   =  ",logical_cpus
		sys.exit()


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

logical_cpus = len(files)

files.sort()
for file in files:
	# Get the number of physical CPU's
	pfp = open("/sys/devices/system/cpu/"+file+"/topology/physical_package_id", 
																			"r")
	# Physical Package ID
	pid = pfp.read()
	try:
		cpus[pid] += 1
	except:
		cpus[pid] = 1


	cfp = open("/sys/devices/system/cpu/"+file+"/topology/core_id", "r")

	# Core ID
	pcid = cfp.read()
	if pcid > cid:
		cid = pcid


physical_cpus = len(cpus)
#print physical_cpus, logical_cpus, cid
print "CPU Topology",

if physical_cpus == logical_cpus:
	print "(SMP)\n"
	for k, v in cpus.iteritems():
		print "CPU "+str(k),

	print_summary("SMP")
elif int(cid) < physical_cpus:
	print "(Hyperthreaded)\n"
	for k, v in cpus.iteritems():
		print "CPU "+str(k) +"    Threads: 2"

	print_summary("HYP")
else:
	if physical_cpus == 1:
		print "(Multicore)\n"
	else:
		print "(SMP / Multicore)\n"
	
	for k, v in cpus.iteritems():
		print "CPU "+str(k) +"    Cores: "+ str(v)
	
	print_summary("SMPMUL")
	
