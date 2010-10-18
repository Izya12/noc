# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Vendor: EdgeCore
## OS:     ES35xx
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
import noc.sa.profiles
from noc.sa.protocols.sae_pb2 import TELNET,SSH
import re

class Profile(noc.sa.profiles.Profile):
    name="EdgeCore.ES35xx"
    supported_schemes=[TELNET,SSH]
    pattern_unpriveleged_prompt=r"^(?P<hostname>[^\n]+)>"
    pattern_prompt=r"^(?P<hostname>[^\n]+)#"
    pattern_more=r"(?P<sep>-{2,3})More(?=sep)"
    command_more=" "

