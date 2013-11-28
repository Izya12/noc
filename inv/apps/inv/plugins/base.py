# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## inv.inv plugins
##----------------------------------------------------------------------
## Copyright (C) 2007-2013 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.inv.models.object import Object

class InvPlugin(object):
    name = None
    js = None

    def __init__(self, app):
        self.app = app
        self.init_plugin()

    def set_app(self, app):
        pass

    def add_view(self, name, func, url, method=["GET"], access="read"):
        self.app.add_view(
            name, func, url=url, method=method, access=access)

    def init_plugin(self):
        self.add_view(
            "api_plugin_%s_data" % self.name,
            self.api_get_data,
            url="^(?P<id>[0-9a-f]{24})/plugin/%s/" % self.name
        )

    def api_get_data(self, request, id):
        o = self.app.get_object_or_404(Object, id=id)
        return self.get_data(request, o)

    def get_data(self, request, object):
        return None

