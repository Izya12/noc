# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Django URL dispatcher for module MAIN
##----------------------------------------------------------------------
## Copyright (C) 2007-2009 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from noc.main.views import index,logout,report,report_index,success,failure

urlpatterns = patterns ( None,
        (r"^$",        login_required(index)),
        (r"^logout/$", login_required(logout)),
        (r"^report/(?P<report>[a-z0-9\-_.]+)/$", login_required(report)),
        (r"^report/$", login_required(report_index)),
        (r"success/$", login_required(success)),
        (r"failure/$", login_required(failure)),
)
