# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS.get_version test
## Auto-generated by manage.py debug-script at 2011-01-06 14:56:54
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class DLink_DxS_get_version_Test(ScriptTestCase):
    script="DLink.DxS.get_version"
    vendor="DLink"
    platform='DGS-3312SR'
    version='3.60-S22'
    input={}
    result={'platform': 'DGS-3312SR', 'vendor': 'DLink', 'version': '3.60-S22'}
    motd='******\n\n'
    cli={
## 'show switch'
'show switch': """show switch
Command: show switch

Device Type       : DGS-3312SR Gigabit-Ethernet Switch
Module 1 Type     : DEM-340MG 4-port mini-GBIC (SFP) module
Module 2 Type     : DEM-340MG 4-port mini-GBIC (SFP) module
Unit ID           : 1
MAC Address       : 00-0D-88-69-14-80
IP Address        : 10.111.0.143 (Manual)
VLAN Name         : default
Subnet Mask       : 255.255.255.0
Default Gateway   : 0.0.0.0
Boot PROM Version : Build 2.00.003
Firmware Version  : Build 3.60-S22
Hardware Version  : 0A2
Device S/N        : 
System Name       : 
System Location   : 
System Contact    : 
Spanning Tree     : Disabled
GVRP              : Disabled
IGMP Snooping     : Disabled
TELNET            : Enabled (TCP 23)
WEB               : Enabled (TCP 80)
RMON              : Disabled
RIP               : Disabled
DVMRP             : Disabled
PIM-DM            : Disabled
OSPF              : Disabled
""",
## 'disable clipaging'
'disable clipaging': """disable clipaging
Command: disable clipaging

Success.                                                          
""",
}
    snmp_get={}
    snmp_getnext={}
