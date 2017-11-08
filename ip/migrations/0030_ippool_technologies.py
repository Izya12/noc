# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# VRF.project, Prefix.project, IP.project
# ---------------------------------------------------------------------
# Copyright (C) 2007-2013 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

from noc.core.model.fields import TextArrayField
# Django modules
# Third-party modules
from south.db import db


class Migration:
    def forwards(self):
        db.add_column(
            "ip_ippool",
            "technologies",
            TextArrayField("Technologies", default=["IPoE"])
        )

    def backwards(self):
        db.drop_column("ip_ippool", "technologies")
