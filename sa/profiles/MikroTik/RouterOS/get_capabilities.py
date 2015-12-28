# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## MikroTik.RouterOS.get_capabilities_ex
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.sa.profiles.Generic.get_capabilities import Script as BaseScript


class Script(BaseScript):
    name = "MikroTik.RouterOS.get_capabilities"

    def execute_platform(self, caps):
        v = self.cli("/system license print")
        c = {}
        for l in v.splitlines():
            l = l.strip()
            if ":" in l:
                cn, cv = l.split(":", 1)
                c[cn.strip()] = cv.strip()

        caps["MikroTik | RouterOS | License | SoftwareID"] = c["software-id"]
        caps["MikroTik | RouterOS | License | Level"] = int(c["nlevel"])
        upto = c.get("upgradable-to")
        if upto:
            caps["MikroTik | RouterOS | License | Upgradable To"] = upto