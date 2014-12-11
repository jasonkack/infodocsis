infodocsis
==========

Infodocsis is a script I made to poll a cable modem via snmp. This script is intended for MSO or Network administrator managing a cable plant. the script returns a bunch of useful values to help you troubleshoot. 
The default community used is public which can be changed at this line of code:
host = M(host=modem, community="public", version=2, timeout=1, retries=0)
Change the value of community to what you are using for your cable modems.

You need these modules for this script to work:
Snimpy
IPy
netaddr

You also need mibs for this script to work. Else you will need to translate everything which is insane.
Mibs called by this script will have dependencies. You will get SMI errors if you have broken dep
Vincent Bernat author of snimpy explains this very well on this page.
Here are the mibs we need 

DOCS-CABLE-DEVICE-MIB
SNMPv2-MIB
IF-MIB
SNMPv2-SMI
DISMAN-EVENT-MIB
DOCS-IF-MIB
RFC1213-MIB
BRIDGE-MIB
