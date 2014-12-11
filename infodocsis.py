#! /usr/bin/env python
# Copyright Jason Kack - jasonkack@gmail.com
# Using MIT License
# Version 0.1a

import os
import sys
from IPy import IP
from netaddr import *
from snimpy.manager import Manager as M
from snimpy.manager import load
from snimpy.manager import snmp
global modem_host

try:
	modem_host = IP(sys.argv[1])
except:
	sys.exit("Invalid argument. Just provide an ip. Thats it")

try:
	# Loading mibs we will need
	load("DOCS-CABLE-DEVICE-MIB")
	load("SNMPv2-MIB")
	load("IF-MIB")
	load("SNMPv2-SMI")
	load("DISMAN-EVENT-MIB")
	load("DOCS-IF-MIB")
	load("RFC1213-MIB")
	load("BRIDGE-MIB")
		
	modem = str(modem_host)
	host = M(host=modem, community="public", version=2, timeout=1, retries=0)
	logs = host.docsDevEvFirstTime
	cablemac = host.ifPhysAddress[2]
	mac = EUI(cablemac)
	mac.dialect = mac_cisco
	
	ifIndex = host.ifIndex
	global downstream 
	downstream = []
	global upstream
	upstream = []
	
	o = 0
	for i in ifIndex:
		ifType = host.ifType[i]
		if "docsCableDownstream" in str(ifType):
			downstream.append(i)
			o = o + 1
	o = 0
	print ("-------------------------------------------------------------------")
	print ("Downstream Information:")
	print ("Down\t" + "Frequency\t" + "Width\t" + "Mod\t\t" + "Power\t" + "SNR\t") 
	for i in downstream:
		DownFreq = float(host.docsIfDownChannelFrequency[i]) / 1000000
		ChanWidth = float(host.docsIfDownChannelWidth[i]) / 1000000
		ChanMod = host.docsIfDownChannelModulation[i]
		RXPower = float(host.docsIfDownChannelPower[i])	/ 10
		DownSNR = float(host.docsIfSigQSignalNoise[i]) / 10
		print(str(o) + "\t" + str(DownFreq) + " MHZ\t" + str(ChanWidth) + " MHZ\t" + str(ChanMod) + "\t" + str(RXPower) + "\t" + str(DownSNR))
		o = o + 1
	print ("-------------------------------------------------------------------")
	print ("Upstream information:")
	o = 0
	for i in ifIndex:
		ifType = host.ifType[i]
		if "docsCableUpstream" in str(ifType):
			upstream.append(i)
			o = o + 1
	print ("Up\t" + "Frequency\t" + "Width\t\t" + "ChanID\t" + "Power\t")
	o = 0
	for i in upstream:
		UpFreq = float(host.docsIfUpChannelFrequency[i]) / 1000000
		UpWidth = float(host.docsIfUpChannelWidth[i]) / 1000000
		UpID = host.docsIfUpChannelId[i]
		UpPower = float(host.docsIfCmStatusTxPower[2]) / 10
		print(str(o) + "\t" + str(UpFreq) + " MHZ \t" + str(UpWidth) + " MHZ \t" + str(UpID) + "\t" + str(UpPower)) 
		o = o + 1
	print ("-------------------------------------------------------------------")
	print ("")
	
	print ("Sysinfo:\t\t" + host.sysDescr)
	print ("Firmware Version:\t" + str(host.docsDevSwCurrentVers))
	print ("DHCP Server:\t\t" + str(host.docsDevServerDhcp))
	print ("Time Server:\t\t" + str(host.docsDevServerTime))
	print ("Tftp Server:\t\t" + str(host.docsDevServerTftp))
	print ("Resets:\t\t\t" + str(host.docsIfCmStatusResets[2]))
	print ("Lost Sync:\t\t" + str(host.docsIfCmStatusLostSyncs[2]))
	print ("")
	print ("Timeout Timers:")
	print ("T1:\t\t\t" + str(host.docsIfCmStatusT1Timeouts[2]))
	print ("T2:\t\t\t" + str(host.docsIfCmStatusT2Timeouts[2]))
	print ("T3:\t\t\t" + str(host.docsIfCmStatusT3Timeouts[2]))
	print ("T4:\t\t\t" + str(host.docsIfCmStatusT4Timeouts[2]))
	print ("")
	print ("FEC Count:")
	print ("Downstream\t" + "Good\t\t" + "Corrected\t" + "UnCorrected")
	o = 0
	if "DOCSIS 3.0" not in host.sysDescr:
		GFec = host.docsIfSigQUnerroreds[3]
		CFec = host.docsIfSigQCorrecteds[3]
		UFec = host.docsIfSigQUncorrectables[3]
		print ("0" + "\t\t" + str(GFec) + "\t" + str(CFec) + "\t\t" + str(UFec))
	else:
		for i in downstream:
			GFec = host.docsIfSigQExtUnerroreds[i]
			CFec = host.docsIfSigQExtCorrecteds[i]
			UFec = host.docsIfSigQExtUncorrectables[i]
			print (str(o) + "\t\t" + str(GFec) + "\t" + str(CFec) + "\t\t" + str(UFec))
			o = o + 1
	print ("")
	print ("Ethernet Interface:")
	print ("Admin status:\t\t" + str(host.ifAdminStatus[1]))
	print ("Oper Status:\t\t" + str(host.ifOperStatus[1]))
	print ("Speed:\t\t\t" + str(host.ifSpeed[1] / 1000000) + " Mbits")
	print ("IN Octets 32bits:\t" + str(host.ifInOctets[1]))
	print ("OUT Octets 32bits:\t" + str(host.ifOutOctets[1]))
	print ("IN Octets 64bits:\t" + str(host.ifHCInOctets[1]))
	print ("OUT Octets 64bits:\t" + str(host.ifHCOutOctets[1]))
	print ("")
	print ("Cable Int Traffic")
	print ("IN Octets 32bits:\t" + str(host.ifInOctets[3]))
	print ("OUT Octets 32bits:\t" + str(host.ifOutOctets[4]))
	print ("IN Octets 64bits:\t" + str(host.ifHCInOctets[3]))
	print ("OUT Octets 64bits:\t" + str(host.ifHCOutOctets[4]))
	print ("")
	print ("Here are the MAC used by the modem:")
	print ("Ethernet Mac:         " + host.ifPhysAddress[1])
	print ("Cable MAC:            " + host.ifPhysAddress[2])
	try:
		print ("USB Mac:              " + host.ifPhysAddress[5])
	except:
		pass
	print ("match the order of the macs with the learned MACs. Thats the ones the modem got from ethernet port. Port index 1 is ethernet")
	o = 0
	maclearn = []
	port = []
	status = []
	for i in host.dot1dTpFdbAddress:
		try:
			maclearn.append(host.dot1dTpFdbAddress[i])
			port.append(host.dot1dTpFdbPort[i])
			status.append(host.dot1dTpFdbStatus[i])
			print("Mac:" + str(maclearn[o]) + " Port:" + str(port[o]) + " Status:" + str(status[o]))
			o = o + 1
		except snmp.SNMPException as detail:
			print ("Modem " + modem + " : " + str(detail))
	# Print logs
	try:
		print ("\nLogs for modem " + str(mac))
	except snmp.SNMPException as detail:
		print ("Modem " + modem + " : " + str(detail))
	print ("Firsttime\t\t" + "LastTime\t\t" + "Counts\t" + "Level\t\t" + "EventID\t\t" + "Log Entry")
	
	for i in logs:
		try:
			FirstTime = host.docsDevEvFirstTime[i]
			LastTime = host.docsDevEvLastTime[i]
			Counts = host.docsDevEvCounts[i]
			Level = host.docsDevEvLevel[i]
			EvId = host.docsDevEvId[i]
			Logs = host.docsDevEvText[i]
			print (str(FirstTime) + "\t" + str(LastTime) + "\t" + str(Counts) + "\t" + str(Level) + "\t" + str(EvId) + "\t" + str(Logs))
		except snmp.SNMPException as detail:
			print ("Modem " + modem + " : " + str(detail))
	

except snmp.SNMPException as detail:
	print ("Modem " + modem + " : " + str(detail))
