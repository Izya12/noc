# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Rotek.RTBS.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------


# Python modules
import re
# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces


class Script(BaseScript):
    name = "Rotek.RTBS.get_interfaces"
    cache = True
    interface = IGetInterfaces

    rx_sh_int = re.compile(
        r"^(?P<ifindex>\d+):\s+(?P<ifname>(e|l|t|b|r|g)\S+):\s"
        r"<(?P<flags>.*?)>\s+mtu\s+(?P<mtu>\d+).+?\n"
        r"^\s+link/\S+(?:\s+(?P<mac>[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}))?\s+.+?\n"
        r"(?:^\s+inet\s+(?P<ip>\d+\S+)\s+)?",
        re.MULTILINE | re.DOTALL)

    rx_status = re.compile(r"^(?P<status>UP|DOWN\S+)", re.MULTILINE)

    def execute(self):
        interfaces = []
        ssid = {}
        i = ["ra0", "ra1"]
        for ri in i:
            s = self.cli("show interface %s ssid" % ri)
            v = self.cli("show interface %s vlan-to-ssid" % ri)
            res = s.split(":")[1].strip().replace("\"", "")
            resv = v.split(":")[1].strip().replace("\"", "")
            ssid[ri] = {"ssid": res, "vlan": resv}
            print ssid
        with self.profile.shell(self):
            v = self.cli("ip a", cached=True)
            for match in self.rx_sh_int.finditer(v):
                a_stat = True
                ifname = match.group("ifname")
                if "@" in ifname:
                    ifname = ifname.split("@")[0]
                flags = match.group("flags")
                smatch = self.rx_status.search(flags)
                if smatch:
                    o_status = smatch.group("status").lower() == "up"
                else:
                    o_status = True
                ip = match.group("ip")
                mac = match.group("mac")
                iface = {
                    "type": self.profile.get_interface_type(ifname),
                    "name": ifname,
                    "admin_status": a_stat,
                    "oper_status": o_status,
                    "snmp_ifindex": match.group("ifindex"),
                    "subinterfaces": [{
                        "name": ifname,
                        "mtu": match.group("mtu"),
                        "admin_status": a_stat,
                        "oper_status": o_status,
                        "snmp_ifindex": match.group("ifindex"),

                    }]
                }
                if mac:
                    iface["mac"] = mac
                    iface["subinterfaces"][0]["mac"] = mac
                if ip:
                    iface["subinterfaces"][0]["address"] = ip
                    iface["subinterfaces"][0]["enabled_afi"] = ["IPv4"]
                else:
                    iface["subinterfaces"][0]["enabled_afi"] = ["BRIDGE"]
                interfaces += [iface]
                for ri in ssid.items():
                    if ifname in ri[0]:
                        iface = {
                            "type": "physical",
                            "name": "%s.%s" % (ifname, ri[1]["ssid"]),
                            "admin_status": a_stat,
                            "oper_status": o_status,
                            "mac": mac,
                            "snmp_ifindex": match.group("ifindex"),
                            "subinterfaces": [{
                                "name": "%s.%s" % (ifname, ri[1]["ssid"]),
                                "enabled_afi": ["BRIDGE"],
                                "admin_status": a_stat,
                                "oper_status": o_status,
                                "mac": mac,
                                "snmp_ifindex": match.group("ifindex"),
                                "untagged_vlan": int(ri[1]["vlan"]),

                            }]
                        }
                        interfaces += [iface]
        return [{"interfaces": interfaces}]
