# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Server(models.Model):
    discord_id = models.CharField(max_length=64)
    name = models.CharField(max_length=128)


class User(models.Model):
    discord_id = models.CharField(max_length=64)


class Tag(models.Model):
    name = models.CharField(max_length=64)


class Link(models.Model):
    source = models.CharField(max_length=256)
    user_id = models.ForeignKey('User')
    channel_id = models.CharField(max_length=64)
    server_id = models.ForeignKey('Server')
    description = models.CharField(max_length=2048)
    title = models.CharField(max_length=128)
    media_url = models.CharField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
