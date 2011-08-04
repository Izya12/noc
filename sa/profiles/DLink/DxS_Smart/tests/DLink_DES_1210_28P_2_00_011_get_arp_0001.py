# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS_Smart.get_arp test
## Auto-generated by ./noc debug-script at 2011-08-04 14:21:01
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class DLink_DxS_Smart_get_arp_Test(ScriptTestCase):
    script = "DLink.DxS_Smart.get_arp"
    vendor = "DLink"
    platform = 'DES-1210-28P'
    version = '2.00.011'
    input = {}
    result = [{'interface': 'vlanMgmt', 'ip': '10.90.90.92', 'mac': '00:E0:81:40:8D:56'}]
    motd = ' \n\n'
    cli = {
## 'debug info'
'debug info': """ debug info
% sgementation fault log file :

File doesn't exist !!! 
% ARP table : 

Address          Hardware Address   Type  Interface  Mapping  
-------          ----------------   ----  ---------  -------  
10.90.90.92      00:e0:81:40:8d:56  ARPA  vlanMgmt   Dynamic   

% MAC table : 

Vlan    Mac Address         Type     Ports
----    -----------         ----     -----
1       00:05:74:97:49:00   Learnt   Gi0/3    
1       00:0c:6e:44:68:7c   Learnt   Gi0/3    
1       00:0d:61:ae:b0:71   Learnt   Gi0/3    
1       00:0f:3d:88:bd:2a   Learnt   Gi0/3    
1       00:15:2b:d6:ab:d1   Learnt   Gi0/3    
1       00:15:f2:74:bc:c3   Learnt   Gi0/3    
1       00:16:76:09:e4:f2   Learnt   Gi0/3    
1       00:16:d4:61:b9:ca   Learnt   Gi0/3    
1       00:16:ec:08:29:8b   Learnt   Gi0/3    
1       00:19:55:e0:c9:42   Learnt   Gi0/3    
               1       00:1a:4d:4f:59:03   Learnt   Gi0/3    
1       00:1d:60:78:ba:82   Learnt   Gi0/3    
1       00:1e:49:10:5f:41   Learnt   Gi0/3    
1       00:1e:49:88:61:00   Learnt   Gi0/3    
1       00:1f:c6:bb:9d:b0   Learnt   Gi0/3    
1       00:1f:c6:c8:de:7b   Learnt   Gi0/3    
1       00:22:15:00:79:7b   Learnt   Gi0/3    
1       00:24:50:54:b7:01   Learnt   Gi0/3    
1       00:26:cb:50:9d:40   Learnt   Gi0/3    
1       00:56:00:0a:02:ff   Learnt   Gi0/3    
1       00:e0:81:40:71:85   Learnt   Gi0/3    
1       00:e0:81:40:8d:56   Learnt   Gi0/3    
1       00:e0:81:b3:2a:2a   Learnt   Gi0/3    
1       e0:cb:4e:43:dc:91   Learnt   Gi0/3    

Total Mac Addresses displayed: 24

                       """, 
}
    snmp_get = {}
    snmp_getnext = {}
