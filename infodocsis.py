#! /usr/bin/env python3
# Copyright Jason Kack – jkack@telebec.com
# Using MIT License
# Version 0.5j

import os, sys
from IPy import IP
from netaddr import *
from snimpy.manager import Manager as M, load, snmp

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
	load("DOCS-IF31-MIB")
	load("DOCS-PNM-MIB")
	load("DOCS-IF-EXT-MIB")



	modem = str(modem_host)
	host = M(host=modem, community="public", version=2, timeout=1, retries=2)
	logs = host.docsDevEvFirstTime
	cablemac = host.ifPhysAddress[2]
	mac = EUI(cablemac)
	mac.dialect = mac_cisco
	ifIndex = host.ifIndex
	pilots = host.docsIf31CmDsOfdmChannelPowerCenterFrequency
	downstream = []
	upstream = []
	ofdmid = []
	ofdmsnr = host.docsPnmCmDsOfdmRxMerMean
	docsisver = host.docsIfDocsisBaseCapability
	eth = []
	o = 0
	for i in ifIndex:
		ifType = host.ifType[i]
		try:
			if "docsCableDownstream" in str(ifType):
				downstream.append(i)
				o = o + 1
			if "docsOfdmDownstream" in str(ifType):
				ofdmid.append(i)
				o = o + 1
			if "ethernetCsmacd"  in str(ifType):
				eth.append(i)
				o = o + 1
		except:
			pass

	print ("-------------------------------------------------------------------")
	print ("Downstream Information:")
	print ("Down\t" + "Frequency\t" + "Width\t" + "Mod\t\t" + "Power\t" + "SNR\t")
	o = 0
	for i in downstream:
		DownFreq = float(host.docsIfDownChannelFrequency[i]) / 1000000
		ChanWidth = float(host.docsIfDownChannelWidth[i]) / 1000000
		ChanMod = host.docsIfDownChannelModulation[i]
		RXPower = float(host.docsIfDownChannelPower[i])	/ 10
		DownSNR = float(host.docsIfSigQSignalNoise[i]) / 10
		print(str(o) + "\t" + str(DownFreq) + " MHZ\t" + str(ChanWidth) + " MHZ\t" + str(ChanMod) + "\t" + str(RXPower) + "\t" + str(DownSNR))
		o = o + 1

	if (docsisver == 5):
		for i in ofdmid:
			ofdmsnr = host.docsPnmCmDsOfdmRxMerMean[i] / 100
			print ("")
			print ("Ofdm Channel pilots and receive power, SNR:")
			print ("Ofdm channel SNR: " + str(ofdmsnr))
			print ("Ofdm Channel PWR:")
			o = 0
			for i in pilots:
				try:
					pilot = host.docsIf31CmDsOfdmChannelPowerCenterFrequency[i] / 1000000
					ofdmrxpwr = float(host.docsIf31CmDsOfdmChannelPowerRxPower[i]) / 10
					print (str(o) + "\t|\t" + str(pilot) + " MHZ\t|\t" + str(ofdmrxpwr))
					o = o + 1
				except snmp.SNMPException as detail:
					print ("Modem " + modem + " : " + str(detail))

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
	print ("Docsis Version:\t\t" + str(docsisver))
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
	print ("RA:\t\t\t" + str(host.docsIfCmStatusRangingAborteds[2]))
	print ("")
	print ("FEC Count:")
	print ("Downstream\t" + "Good\t\t" + "Corrected\t" + "UnCorrected")
	o = 0

	if docsisver <= 3:
		GFec = host.docsIfSigQUnerroreds[3]
		CFec = host.docsIfSigQCorrecteds[3]
		UFec = host.docsIfSigQUncorrectables[3]
		print ("0" + "\t\t" + str(GFec) + "\t\t" + str(CFec) + "\t\t" + str(UFec))
	if docsisver == 4:
		print ("docsis 3.0")
		for i in downstream:
			GFec = host.docsIfSigQExtUnerroreds[i]
			CFec = host.docsIfSigQExtCorrecteds[i]
			UFec = host.docsIfSigQExtUncorrectables[i]
			print (str(o) + "\t\t" + str(GFec) + "\t\t" + str(CFec) + "\t\t" + str(UFec))
			o = o + 1
	if docsisver == 5:
		print ("docsis 3.1")
		for i in downstream:
			GFec = host.docsIfSigQExtUnerroreds[i]
			CFec = host.docsIfSigQExtCorrecteds[i]
			UFec = host.docsIfSigQExtUncorrectables[i]
			print (str(o) + "\t\t" + str(GFec) + "\t\t" + str(CFec) + "\t\t" + str(UFec))
			o = o + 1
	print ("")
	print ("Ethernet Interfaces:")
	o = 0
	for i in eth:
		print ("Eth" + str(o) + ":")
		print ("Admin status:\t\t" + str(host.ifAdminStatus[i]))
		print ("Oper Status:\t\t" + str(host.ifOperStatus[i]))
		print ("Speed:\t\t\t" + str(host.ifSpeed[i] / 1000000) + " Mbits")
		print ("IN Octets 32bits:\t" + str(host.ifInOctets[i]))
		print ("OUT Octets 32bits:\t" + str(host.ifOutOctets[i]))
		print ("IN Octets 64bits:\t" + str(host.ifHCInOctets[i]))
		print ("OUT Octets 64bits:\t" + str(host.ifHCOutOctets[i]))
		print ("")
		o = o + 1

	print ("")
	print ("Here are the MAC used by the modem:")
	print ("Ethernet Mac:         " + host.ifPhysAddress[1])
	print ("Cable MAC:            " + host.ifPhysAddress[2])
	try:
		print ("USB Mac:              " + host.ifPhysAddress[5])
	except:
		pass
	print ("Here are the macs the modem learned:")
	o = 0
	maclearn = []
	port = []
	status = []
	for i in host.dot1dTpFdbAddress:
		try:
			if 'learned' in str(host.dot1dTpFdbStatus[i]):
				maclearn.append(host.dot1dTpFdbAddress[i])
				port.append(host.dot1dTpFdbPort[i])
				status.append(host.dot1dTpFdbStatus[i])
				print("Mac:" + str(maclearn[o]) + " Port:" + str(port[o]) + " Status:" + str(status[o]))
				o = o + 1
		except snmp.SNMPException as detail:
			print ("Modem " + modem + " : " + str(detail))
	print ("")

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
		except UnicodeDecodeError:
			continue


except snmp.SNMPException as detail:
	print ("Modem " + modem + " : " + str(detail))
