# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Zyxel.ZyNOS.add_vlan
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.iaddvlan import IAddVlan


class Script(BaseScript):
    name = "Zyxel.ZyNOS.add_vlan"
    interface = IAddVlan

    def execute(self, vlan_id, name, tagged_ports):
        with self.configure():
            self.cli("vlan %d" % vlan_id)
            self.cli("name %s" % name)
            if tagged_ports:
                for port in tagged_ports:
                    self.cli("fixed %s" % port)
            self.cli("exit")
        self.save_config()
        return True
