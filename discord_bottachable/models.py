# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=256)

class Attachment(models.Model):
    url = models.CharField(max_length=2048)
    user = models.ForeignKey('User')
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    tag_name = models.CharField(max_length=64)
    attachment_id = models.ForeignKey('Attachment')

class Link(models.Model):
    source = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    thumbnail_url = models.CharField(max_length=256)
    tags = models.CharField(max_length=256)
