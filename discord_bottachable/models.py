# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Server(models.Model):
    discord_id = models.CharField(max_length=64)
    log_channel = models.ForeignKey('Channel',null=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return (
            "Discord id: {0}\n"
            "Log channel: {1}\n"
            "Name: {2}\n"
        ).format(
            self.discord_id,
            ("None" if self.log_channel is None else self.log_channel.name),
            self.name
        )


class Channel(models.Model):
    discord_id = models.CharField(max_length=64)
    server_id = models.ForeignKey('Server')
    listen = models.SmallIntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return (
            "Discord id: {0}\n"
            "Server id: {1}\n"
            "Name: {2}\n"
        ).format(self.discord_id, self.server_id.id, self.name)


class User(models.Model):
    discord_id = models.CharField(max_length=64)
    username = models.CharField(max_length=128)

    def __str__(self):
        return (
            "Discord id: {0}\n"
            "Name: {1}\n"
        ).format(self.discord_id, self.username)


class Role(models.Model):
    server_id = models.ForeignKey('Server')
    user_id = models.ForeignKey('User')
    rank = models.PositiveSmallIntegerField()

    def __str__(self):
        return "Rank: {0}\n".format(self.rank)


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return "Name: {0}\n".format(self.name)


class Link(models.Model):
    # Initialize variables for choices
    MEDIA_TYPE_PICTURE = 'picture'
    MEDIA_TYPE_VIDEO = 'video'
    MEDIA_TYPE_NONE = None

    # Add possible values for media_type
    MEDIA_TYPE_CHOICES = (
        (MEDIA_TYPE_PICTURE, 'Picture'),
        (MEDIA_TYPE_VIDEO, 'Video'),
        (MEDIA_TYPE_NONE, 'No media')
    )

    source = models.CharField(max_length=256)
    user_id = models.ForeignKey('User')
    channel_id = models.ForeignKey('Channel')
    server_id = models.ForeignKey('Server')
    description = models.CharField(max_length=2048)
    title = models.CharField(max_length=128)
    media_url = models.CharField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="tags")
    media_type = models.CharField(max_length=64, choices=MEDIA_TYPE_CHOICES)

    def __str__(self):
        return (
            "Url: {0}\n"
            "Author: {1}\n"
            "From channel: #{2}\n"
            "Description: {3}\n"
            "Title: {4}\n"
            "Tags: {5}\n"
        ).format(
            self.source,
            self.user_id.username,
            self.channel_id.name,
            self.description,
            self.title,
            [tag.name for tag in self.tags.all()]
        )
