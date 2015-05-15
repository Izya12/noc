# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Vendor: Supertel
## OS:     K2X
##----------------------------------------------------------------------
## Copyright (C) 2007-2014 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.sa.profiles import Profile as NOCProfile


class Profile(NOCProfile):
    name = "Supertel.K2X"
    supported_schemes = [NOCProfile.TELNET, NOCProfile.SSH]
    pattern_username = r"^User Name:"
    pattern_password = r"^Password:"
    pattern_more = [
        (r"^More: <space>,  Quit: q, One line: <return>$", " "),
        (r"\[Yes/press any key for no\]", "Y")
        ]
    pattern_unpriveleged_prompt = r"^\S+> "
    pattern_syntax_error = r"^%\s+(Unrecognized command|Incomplete command|\
missing mandatory parameter|bad parameter value|\
Wrong number of parameters or invalid range, size or characters entered)$"
    command_disable_pager = "terminal datadump"
    command_super = "enable"
    command_enter_config = "configure"
    command_leave_config = "end"
    command_save_config = "copy running-config startup-config"
    pattern_prompt = r"^(?P<hostname>\S+)#"

    platforms = {
        "1": "K21",
        "2": "K21-1",
        "3": "K23",
        "4": "K23-1",
    }