# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# KBGlobalBookmark
# ---------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from django.db import models
# NOC modules
from noc.kb.models.kbentry import KBEntry


class KBGlobalBookmark(models.Model):
    """
    Global Bookmarks
    @todo: Replace with boolean flag in KBEntry
    """
    class Meta:
        verbose_name = "KB Global Bookmark"
        verbose_name_plural = "KB Global Bookmarks"
        app_label = "kb"
        db_table = "kb_kbglobalbookmark"

    kb_entry = models.ForeignKey(KBEntry, verbose_name="KBEntry", unique=True)

    def __unicode__(self):
        return unicode(self.kb_entry)
