infodocsis
==========

Infodocsis is a script I made to poll a cable modem via snmp. This script is intended for MSO or Network administrator managing a cable plant. the script returns a bunch of useful values to help you troubleshoot. <br>
The default community used is public which can be changed at this line of code:<br>
host = M(host=modem, community="public", version=2, timeout=1, retries=2)<br>
Change the value of community to what you are using for your cable modems.<br>

You need these modules for this script to work:<br>
Snimpy<br>
IPy<br>
netaddr<br>

You also need mibs for this script to work. Else you will need to translate everything which is insane.
Mibs called by this script will have dependencies. You will get SMI errors if you have broken dep
Vincent Bernat author of snimpy explains this very well in his doc.
Here are the mibs we need 

DOCS-CABLE-DEVICE-MIB<br>
SNMPv2-MIB<br>
IF-MIB<br>
SNMPv2-SMI<br>
DISMAN-EVENT-MIB<br>
DOCS-IF-MIB<br>
RFC1213-MIB<br>
BRIDGE-MIB<br>
<br>
Just install packages snmp-mibs-downloader on debian like systems to downlaod all these mibs and many more.
I had issues on 2 servers with with RFC1213-MIB that depends on RFC-1212 which was not included in snmp-mibs-downloader.<br>
A quick way was to do wget http://www.simpleweb.org/ietf/mibs/modules/IETF/txt/RFC-1212 from the /usr/share/mibs/ietf
<br>or<br>
/var/lib/mibs/ietf
<br> I now include it in the mibs dir so you can manually add it to your dir.
