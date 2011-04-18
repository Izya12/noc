# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS.get_version test
## Auto-generated by manage.py debug-script at 2010-11-19 15:19:57
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class DLink_DxS_get_version_Test(ScriptTestCase):
   script="DLink.DxS.get_version"
   vendor="DLink"
   platform='DGS-3627G'
   version='2.82.B13'
   input={}
   result={'attributes': {'Boot PROM': '1.10-B09',
                 'HW version': 'A1',
                 'Serial Number': 'P1JN1A7000427'},
'platform': 'DGS-3627G', 'vendor': 'DLink', 'version': '2.82.B13'}
   motd='******\n\n'
   cli={
## 'show switch'
'show switch': """show switch
Command: show switch

Device Type       : DGS-3627G Gigabit Ethernet Switch
MAC Address       : 00-22-B0-25-CC-00
IP Address        : 192.168.0.1 (Manual)
VLAN Name         : default
Subnet Mask       : 255.255.255.0
Default Gateway\t  : 0.0.0.0
Boot PROM Version : Build 1.10-B09
Firmware Version  : Build 2.82.B13
Hardware Version  : A1
Serial Number     : P1JN1A7000427
System Name       :
System Location   : Makulan
System Contact    :
Spanning Tree     : Disabled
GVRP              : Disabled
IGMP Snooping     : Disabled
MLD Snooping      : Disabled
RIP               : Disabled
DVMRP             : Disabled
PIM               : Disabled
OSPF              : Disabled
OSPFv3            : Disabled
BGP               : Enabled
RIPng             : Disabled
TELNET            : Enabled (TCP 23)
WEB               : Disabled
SNMP              : Disabled
RMON              : Disabled
SSL status        : Disabled
SSH status        : Disabled
802.1x            : Disabled
Jumbo Frame       : On
Clipaging         : Disabled
MAC Notification  : Disabled
Port Mirror       : Disabled
SNTP              : Enabled
DHCP Relay        : Enabled
DNSR Status       : Disabled
VRRP              : Disabled
HOL Prevention State : Enabled
Syslog Global State  : Disabled
Single IP Management : Disabled
Password Encryption Status : Enabled
DNS Resolver        : Disabled
""",
## 'disable clipaging'
'disable clipaging': """disable clipaging
Command: disable clipaging

Success.
""",
}
   snmp_get={}
   snmp_getnext={}
