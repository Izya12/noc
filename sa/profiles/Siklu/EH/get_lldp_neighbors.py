# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Siklu.EH.get_lldp_neighbors
##----------------------------------------------------------------------
## Copyright (C) 2007-2016 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import re
## NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetlldpneighbors import IGetLLDPNeighbors
from noc.sa.interfaces.base import MACAddressParameter
from noc.lib.validators import is_int, is_ipv4


class Script(BaseScript):
    name = "Siklu.EH.get_lldp_neighbors"
    interface = IGetLLDPNeighbors

    rx_ecfg = re.compile(
        r"^(?P<cmd>\S+)\s+(?P<name>\S+)\s+\d+\s+(?P<key>\S+)\s*:(?P<value>.*?)$",
        re.MULTILINE)

    def parse_section(self, section):
        r = {}
        name = None
        for match in self.rx_ecfg.finditer(section):
            name = match.group("name")
            r[match.group("key")] = match.group("value").strip()
        return name, r

    def execute(self):
        r = []
        try:
            v = self.cli("show lldp-remote")
        except self.CLISyntaxError:
            raise self.NotSupportedError()
        for section in v.split("\n\n"):
            if not section:
                continue
            name, cfg = self.parse_section(section)
            neighbor = {
                "remote_chassis_id": cfg["chassis-id"],
                "remote_chassis_id_subtype": {
                    "network-addr": 5
                }[cfg["chassis-id-subtype"]],
                "remote_port": cfg["port-id"],
                "remote_port_subtype": {
                    "mac-addr": 3
                }[cfg["port-id-subtype"]]
            }
            if "port-descr" in cfg:
                neighbor["remote_port_description"] = cfg["port-descr"]
            if "sys-name" in cfg:
                neighbor["remote_system_name"] = cfg["sys-name"]
            if "sys-descr" in cfg:
                neighbor["remote_system_description"] = cfg["sys-descr"]
            found = False
            for i in r:
                if i["local_interface"] == name:
                    i["neighbors"] += [neighbor]
                    found = True
                    break
            if not found:
                r += [{
                    "local_interface": name,
                    "neighbors": [neighbor]
                }]
        return r