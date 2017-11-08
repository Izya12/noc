# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Brocade.ADX.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

"""
"""
# Python modules
import re

from noc.core.ip import IPv4
# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces


class Script(BaseScript):
    name = 'Brocade.ADX.get_interfaces'
    interface = IGetInterfaces

    """
    rx_sh_int = re.compile(
        r"^(?P<interface>\d+?)\s+(?P<admin_status>Up|Down)\s+"
        r"(?P<oper_status>Forward|None)?.+"
        r"(?P<mac>\S{4}\.\S{4}\.\S{4})(?:\s(?P<descr>\S+))?$",
        re.MULTILINE | re.IGNORECASE)
    """
    rx_sh_int = re.compile(
        r"^(?P<interface>\S+?)\s+(?P<admin_status>Up|Down)\s+"
        r"(?P<oper_status>Forward|None)?.+"
        r"(?P<mac>\S{4}\.\S{4}\.\S{4})(?:\s(?P<descr>\S+))?")
    rx_int_alias = re.compile(
        r"^(Description|Vlan alias name is)\s*(?P<alias>.*?)$",
        re.MULTILINE | re.IGNORECASE)
    rx_int_mac = re.compile(
        r"address\s+is\s+(?P<mac>\S+)", re.MULTILINE | re.IGNORECASE)
    rx_int_ipv4 = re.compile(
        r"Internet address is (?P<address>[0-9\.\/]+)",
        re.MULTILINE | re.IGNORECASE)
    rx_vlan_list = re.compile(
        r"vlan (?P<vlan>\d+) name (?P<vlanname>\S+) by port"
        r"\s+(?P<tagged>\S+) ethe (?P<from>[0-9\.\/]+)\sto\s"
        r"(?P<to>[0-9\.\/]+)?"
        r"\s+router-interface (?P<ve>ve\s\d+)", re.MULTILINE | re.IGNORECASE)

    def execute(self):
        interfaces = []
        shrunvlan = self.cli('sh running-config vlan | excl tag-type')
        tagged = {}
        untagged = {}
        r = []
        for v in shrunvlan.split('!'):
            # self.debug('\nPROCESSING:' + v + '\n')
            match = self.rx_vlan_list.findall(v)
            if match:
                tag = 1
                for m in match:
                    if not m[0]:
                        tag = 0
                        continue
                    elif m[0].isdigit():
                        vlan = int(m[0])
                        first = m[3]
                        last = m[4]
                    for n in range(int(first), int(last) + 1):
                        if m[2] == 'tagged':
                            if n in tagged:
                                tagged[n].append(vlan)
                            else:
                                tagged[n] = [vlan]
                        else:
                            untagged[n] = vlan
                    if (m[5]):
                        ve = m[5].replace(' ', '')
                        self.debug('\nFOUND VE: ' + m[5] + '\n')
                        untagged[ve] = vlan
                    else:
                        self.debug('\nVE NOT FOUND ' + m[0] + '\n')
                        continue
        v = ''
        # XXX
        shint = self.cli('sh int br | excl Port')
        for v in shint.split("\n"):
            try:
                match = self.re_search(self.rx_sh_int, v)
            except:
                continue
            # self.debug('\nPROCESSING LINE: ' + v + '\n')
            port = match.group("interface")
            admin_status = match.group("admin_status")
            admin_status = admin_status.lower().replace('forward', 'up')
            oper_status = match.group("oper_status")
            if oper_status:
                oper_status = oper_status.lower().replace('none', 'down')
            else:
                oper_status = 'down'
            mac = match.group("mac")
            descr = match.group("descr")
            # XXX
            if port.isdigit():
                ift = 'physical'
                self.debug('FOUND PHYSICAL\n')
            elif port.find('e') > 0:
                ift = 'SVI'
                self.debug('FOUND VIRTUAL\n')
            elif port.find('b') > 0:
                ift = 'loopback'
                self.debug('FOUND LOOPBACK\n')
            elif port.find('g') > 0:
                ift = 'management'
                self.debug('FOUND MANAGEMENT\n')
            elif port.find('n') > 0:
                ift = 'tunnel'
            else:
                self.debug('NOT FOUND: %s\n' % port)
                continue
            i = {
                'name': port,
                'type': ift,
                'admin_status': admin_status == 'up',
                'oper_status': oper_status == 'up',
                'enabled_protocols': [],
                'subinterfaces': [{
                    'name': port,
                    'admin_status': admin_status == 'up',
                    'oper_status': oper_status == 'up'
                }]
            }
            if ift == 'SVI':
                if untagged[port]:
                    i['subinterfaces'][0].update(
                        {'vlan_ids': [untagged[port]]}
                    )
                ipa = self.cli('show run int %s | inc ip addr' % port)
                ipal = ipa.splitlines()
                ip_address = []
                for l in ipal:
                    l = l.strip()
                    self.debug('ip.split len:' + str(len(l.split())))
                    if len(l.split()) > 3:
                        ip_address += ['%s/%s' % (
                            l.split()[2], IPv4.netmask_to_len(l.split()[3])
                        )]
                    else:
                        ip_address.append(l.split()[2])
                #
                i['subinterfaces'][0].update({'enabled_afi': ['IPv4']})
                i['subinterfaces'][0].update({'ipv4_addresses': ip_address})
                if descr:
                    i['subinterfaces'][0].update({'description': descr})
            if ift == 'physical':
                i['subinterfaces'][0].update({'is_bridge': True})
                if port in tagged:
                    i['subinterfaces'][0].update(
                        {'tagged_vlans': tagged[port]}
                    )
                if port in untagged:
                    i['subinterfaces'][0].update(
                        {'untagged_vlan': untagged[port]}
                    )
                    """
                    l2protos = []
                    l3protos = []
                    if port in stp:
                        l2protos += ['STP']
                    if port in gvrp:
                        l2protos += ['GVRP']
                    i.update({'enabled_protocols': l2protos})
                    if port in rip:
                        l3protos += ['RIP']
                    if port in ospf:
                        l3protos += ['OSPF']
                    if port in pim:
                        l3protos += ['PIM']
                    if port in dvmrp:
                        l3protos += ['DVMRP']
                    if port in igmp:
                        l3protos += ['IGMP']
                    i['subinterfaces'][0].update(
                        {'enabled_protocols': l3protos}
                    )
                    """
            interfaces += [i]
        return [{'interfaces': interfaces}]
