# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DGS3100.get_interface_status test
## Auto-generated by ./noc debug-script at 2012-02-22 12:49:53
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class DLink_DGS3100_get_interface_status_Test(ScriptTestCase):
    script = "DLink.DGS3100.get_interface_status"
    vendor = "DLink"
    platform = '<<<INSERT YOUR PLATFORM HERE>>>'
    version = '<<<INSERT YOUR VERSION HERE>>>'
    input = {}
    result = [{'interface': '1:1', 'status': False},
 {'interface': '1:2', 'status': True},
 {'interface': '1:3', 'status': False},
 {'interface': '1:4', 'status': False},
 {'interface': '1:5', 'status': True},
 {'interface': '1:6', 'status': False},
 {'interface': '1:7', 'status': False},
 {'interface': '1:8', 'status': True},
 {'interface': '1:9', 'status': True},
 {'interface': '1:10', 'status': False},
 {'interface': '1:11', 'status': True},
 {'interface': '1:12', 'status': True},
 {'interface': '1:13', 'status': True},
 {'interface': '1:14', 'status': True},
 {'interface': '1:15', 'status': True},
 {'interface': '1:16', 'status': True},
 {'interface': '1:17', 'status': True},
 {'interface': '1:18', 'status': True},
 {'interface': '1:19', 'status': True},
 {'interface': '1:20', 'status': True},
 {'interface': '1:21', 'status': True},
 {'interface': '1:22', 'status': True},
 {'interface': '1:23', 'status': True},
 {'interface': '1:24', 'status': True}]
    motd = ''
    cli = {
## 'show ports all'
'show ports all': """ show ports all
Port  Port       Settings                Connection              Address   
      State      Speed/Duplex/FlowCtrl   Speed/Duplex/FlowCtrl   Learning  
---   -------    ------------------      ------------------      -------   
1:1   Enabled    Auto/Disabled           Link Down               Enabled   
1:2   Enabled    100M/Full/Auto          100M/Full/Disabled      Enabled   
1:3   Enabled    100M/Full/Disabled      Link Down               Enabled   
1:4   Enabled    100M/Full/Disabled      Link Down               Enabled   
1:5   Enabled    100M/Full/Disabled      100M/Full/Disabled      Enabled   
1:6   Enabled    100M/Full/Disabled      Link Down               Enabled   
1:7   Enabled    100M/Full/Disabled      Link Down               Enabled   
1:8   Enabled    100M/Full/Disabled      100M/Full/Disabled      Enabled   
1:9   Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
1:10  Enabled    1000M/Full/Disabled     Link Down               Enabled   
1:11  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
1:12  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
1:13  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
1:14  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
1:15  Enabled    100M/Full/Disabled      100M/Full/Disabled      Enabled   
1:16  Enabled    100M/Full/Disabled      100M/Full/Disabled      Enabled   
1:17  Enabled    100M/Full/Disabled      100M/Full/Disabled      Enabled   
1:18  Enabled    100M/Full/Disabled      100M/Full/Disabled      Enabled   
1:19  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
                                                                                                                    1:20  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
1:21  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
1:22  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
1:23  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   
1:24  Enabled    1000M/Full/Disabled     1000M/Full/Disabled     Enabled   """, 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
