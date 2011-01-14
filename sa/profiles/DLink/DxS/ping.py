# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS.ping
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
from noc.sa.script import Script as NOCScript
from noc.sa.interfaces import IPing
import re

rx_result=re.compile(r"^\s*Packets: Sent =\s*(?P<count>\d+), Received =\s*(?P<success>\d+), Lost =\s*\d+",re.MULTILINE|re.DOTALL|re.IGNORECASE)
class Script(NOCScript):
    name="DLink.DxS.ping"
    implements=[IPing]
    def execute(self,address,count=None,source_address=None,size=None,df=None):
        cmd="ping %s"%address
        if count:
            cmd+=" times %d"%int(count)
        else:
            cmd+=" times 5"
        if source_address:
            cmd+=" source_ip %s"%source_address
        # Don't implemented, may be in future firmware revisions ?
        #if size:
        #    cmd+=" size %d"%int(size)
        #if df:
        #    cmd+=" df-bit"
        match=rx_result.search(self.cli(cmd))
        if not match:
            raise self.NotSupportedError()
        return {
            "success": match.group("success"),
            "count"  : match.group("count"),
        }
