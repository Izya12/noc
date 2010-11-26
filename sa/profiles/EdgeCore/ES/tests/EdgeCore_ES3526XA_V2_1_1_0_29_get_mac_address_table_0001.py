# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES.get_mac_address_table test
## Auto-generated by manage.py debug-script at 2010-11-26 17:48:33
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class EdgeCore_ES_get_mac_address_table_Test(ScriptTestCase):
    script="EdgeCore.ES.get_mac_address_table"
    vendor="EdgeCore"
    platform='ES3526XA-V2'
    version='1.1.0.29'
    input={}
    result=[{'interfaces': ['Eth 1/25'],
      'mac': '00:12:CF:7E:0F:36',
      'type': 'D',
      'vlan_id': 1},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:16:C7:62:8F:00',
      'type': 'D',
      'vlan_id': 120},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:24:01:18:7E:F8',
      'type': 'D',
      'vlan_id': 120},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:26:88:70:90:00',
      'type': 'D',
      'vlan_id': 120},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:16:C7:62:8F:00',
      'type': 'D',
      'vlan_id': 733},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:1E:F7:02:D4:A1',
      'type': 'D',
      'vlan_id': 733},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:11:5C:0B:C8:80',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:11:5C:DA:0D:00',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:11:92:83:A0:00',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:12:CF:41:36:20',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:12:CF:4C:D2:60',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:12:CF:4C:D6:40',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:14:1C:8E:97:C9',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:16:C7:62:8F:00',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:1C:0E:58:D4:DC',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:25:45:84:46:CC',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:26:88:70:90:00',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:E0:D8:13:9D:82',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:E0:D8:13:9D:D4',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:E0:D8:13:9E:7B',
      'type': 'D',
      'vlan_id': 900},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:12:43:39:CA:80',
      'type': 'D',
      'vlan_id': 2539},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:16:C7:62:8F:00',
      'type': 'D',
      'vlan_id': 2539},
     {'interfaces': ['Eth 1/25'],
      'mac': '00:1B:2A:35:B5:1A',
      'type': 'D',
      'vlan_id': 2539}]
    motd=''
    cli={
## 'show mac-address-table'
'show mac-address-table': """show mac-address-table
 Interface MAC Address       VLAN Type
 --------- ----------------- ---- -----------------
  Eth 1/ 1 00-11-6B-1B-69-AD  120 Learned
  Eth 1/ 2 00-13-46-56-C5-86  733 Learned
  Eth 1/25 00-12-CF-7E-0F-36    1 Learned
  Eth 1/25 00-16-C7-62-8F-00  120 Learned
  Eth 1/25 00-24-01-18-7E-F8  120 Learned
  Eth 1/25 00-26-88-70-90-00  120 Learned
  Eth 1/25 00-16-C7-62-8F-00  733 Learned
  Eth 1/25 00-1E-F7-02-D4-A1  733 Learned
  Eth 1/25 00-11-5C-0B-C8-80  900 Learned
  Eth 1/25 00-11-5C-DA-0D-00  900 Learned
  Eth 1/25 00-11-92-83-A0-00  900 Learned
  Eth 1/25 00-12-CF-41-36-20  900 Learned
  Eth 1/25 00-12-CF-4C-D2-60  900 Learned
  Eth 1/25 00-12-CF-4C-D6-40  900 Learned
  Eth 1/25 00-14-1C-8E-97-C9  900 Learned
  Eth 1/25 00-16-C7-62-8F-00  900 Learned
  Eth 1/25 00-1C-0E-58-D4-DC  900 Learned
  Eth 1/25 00-25-45-84-46-CC  900 Learned
  Eth 1/25 00-26-88-70-90-00  900 Learned
  Eth 1/25 00-E0-D8-13-9D-82  900 Learned
  Eth 1/25 00-E0-D8-13-9D-D4  900 Learned
  Eth 1/25 00-E0-D8-13-9E-7B  900 Learned
  Eth 1/25 00-12-43-39-CA-80 2539 Learned
  Eth 1/25 00-16-C7-62-8F-00 2539 Learned
  Eth 1/25 00-1B-2A-35-B5-1A 2539 Learned""",
}
    snmp_get={}
    snmp_getnext={}
