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

num_cpus  = 0
num_cores = 0
files     = []
# Dictionary to hold cpu topology; cpu number, number of cores
cpu_topo  = {}
# Previous physical_package_id
ppid = -2
# Previous core_id
pcid = -2


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
	# get number of CPU's
	pfp = open("/sys/devices/system/cpu/"+file+"/topology/physical_package_id", 
																			"r")
	pid = pfp.read()
	
	if pid != ppid:
		num_cpus += 1
		ppid = pid
	
	if pid == ppid:
		num_cores += 1	
		try:
			cpu_topo[pid] += 1
		except:
			cpu_topo[pid] = 1


print "CPU Topology\n"
for k, v in cpu_topo.iteritems():
	print "CPU "+str(k) +"    Cores: "+ str(v)

print
print "Number of CPUs  = ",num_cpus
print "Number of cores = ",num_cores

