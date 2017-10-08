# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=64)


class Link(models.Model):
    url = models.CharField(max_length=2048)
    user_id = models.ForeignKey('User')
    channel_id = models.CharField(max_length = 64)
    server_id = models.CharField(max_length = 64)
    description = models.CharField(max_length = 2048)
    title = models.CharField(max_length = 128)
    media_url = models.CharField(max_length = 2048)
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    tag_name = models.CharField(max_length=64)
    link_id = models.ForeignKey('Link')
