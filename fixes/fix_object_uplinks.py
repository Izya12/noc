# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Update ObjectUplink
# ---------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

from noc.core.topology.segment import SegmentTopology
# NOC modules
from noc.inv.models.networksegment import NetworkSegment
from noc.sa.models.objectdata import ObjectData


def fix():
    for ns in NetworkSegment.objects.timeout(False):
        st = SegmentTopology(ns)
        ObjectData.update_uplinks(
            st.get_object_uplinks()
        )
