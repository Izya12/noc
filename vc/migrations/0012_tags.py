# encoding: utf-8
from noc.core.model.fields import AutoCompleteTagsField
from noc.ip.models import *
from south.db import db


class Migration:
    TAG_MODELS = ["vc_vc"]

    def forwards(self):
        for m in self.TAG_MODELS:
            db.add_column(m, "tags", AutoCompleteTagsField("Tags", null=True, blank=True))

    def backwards(self):
        for m in self.TAG_MODELS:
            db.delete_column(m, "tags")
