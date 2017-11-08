# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

from noc.core.model.fields import TagsField
# Django modules
# Third-party modules
from south.db import db


class Migration:
    def forwards(self):
        db.add_column(
            "sa_managedobjectprofile",
            "tags",
            TagsField("Tags", null=True, blank=True)
        )

    def backwards(self):
        pass
