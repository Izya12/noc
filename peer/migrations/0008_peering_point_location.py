# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (C) 2007-2009 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
from noc.peer.models import *
from south.db import db


class Migration:
    def forwards(self):
        db.add_column("peer_peeringpoint", "location",
                      models.CharField("Location", max_length=64, blank=True, null=True))

    def backwards(self):
        db.delete_column("peer_peeringpoint", "location")
