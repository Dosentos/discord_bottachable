from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template.defaulttags import register
from django.db.models import Q
from discord_bottachable.models import Server, Link, Channel

import logging
from collections import OrderedDict

# Create an instance of logger
logger = logging.getLogger(__name__)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def addSpaces(str):
    return str.replace(',', ', ')

@register.filter
def isActiveLink(channel_name, current_channel):
    if channel_name == current_channel:
        return 'active'
    else:
        return

@register.simple_tag
def urlWithoutSelf(url, tag, tags):
    tags = list(tags)
    if tag in tags: 
        tags.remove(tag)
    return url + 'tags/' + ','.join(tags)

# Create your views here.
def index(request):
    return render(request, 'index.html', {'servers': Server.objects.all()})

def server(request, server_id, channel_name='', tags='', keywords=''):
    if request.method == 'POST':
        return redirect(getRedirectUrl(request, server_id, tags, keywords, channel_name))
    else:
        s = get_object_or_404(Server, discord_id=server_id)
        all_links = Link.objects.filter(server_id=s).order_by('-modified_at')
        
        channels = Channel.objects.filter(server_id=s.id)

        if len(channel_name) > 0:
            all_links = filterByChannel(all_links, channels, channel_name)

        keywords = str_to_array(keywords, ',')

        if len(keywords) > 0:
            all_links = filterByKeywords(all_links, keywords)
        
        tags = str_to_array(tags, ',')

        if len(tags) > 0:
            all_links = filterByTags(all_links, tags)

        paginator = Paginator(all_links, 12)

        page = request.GET.get('page')
        try:
            links = paginator.page(page)
        except PageNotAnInteger:
            links = paginator.page(1)
        except EmptyPage:
            links = paginator.page(paginator.num_pages)

        return render(request, 'server.html', {
            'links': links,
            'server_id': server_id,
            'server_name': s.name,
            'channels': channels,
            'current_channel': channel_name,
            'tags': tags,
            'current_tags': ','.join(tags),
            'current_keywords': ','.join(keywords),
            'tag_links': getTagLinks(all_links, server_id, tags, keywords, channel_name),
            'current_url_without_tags': getCurrentUrlWithoutTags(server_id, channel_name, keywords)
        })

def getRedirectUrl(request, server_id, tags, keywords, channel_name):
    # convert to array
    keywords = str_to_array(request.POST.get('keywords', None), ',')
    # trim every keyword
    for i, keyword in enumerate(keywords):
        keywords[i] = keyword.strip()
    # convert back to string
    keywords = ','.join(keywords)

    url = '/' + server_id + '/'

    if len(channel_name) > 0:
        url += channel_name + '/'
    if len(keywords) > 0:
        url += 'search/' + keywords + '/'
    if len(tags) > 0:
        url += 'tags/' + ','.join(str_to_array(tags, ','))

    return url

def getTagLinks(all_links, server_id, tags, keywords, channel_name):
    urls = {}
    for l in all_links:
        url = ''
        urls[l.id] = {}
        for t in l.tags.all():
            url = ''
            if len(channel_name) > 0:
                url += channel_name + '/'
            if len(keywords) > 0:
                url = 'search/' + ','.join(keywords) + '/'
            if len(tags) > 0:
                if t.name not in tags:
                    url += 'tags/' + ','.join(tags) + ',' + t.name
                else:
                    url += 'tags/' + ','.join(tags) + '#'
            elif len(tags) == 0:
                url += 'tags/' + t.name
            urls[l.id][t.id] = url
    return urls

def filterByChannel(all_links, channels, channel_name):
    channel = channels.filter(name=channel_name)
    if len(channel) > 0:
        all_links = all_links.filter(channel_id=channel[0].id)
    return all_links

def filterByKeywords(all_links, keywords):
    for keyword in keywords: 
        all_links = all_links.filter(
            Q(title__icontains=keyword) | Q(description__icontains=keyword)
        )

    return all_links

def filterByTags(all_links, tags):
    for tag in tags: 
        all_links = all_links.filter(tags__name=tag)

    return all_links

def str_to_array(str, delimeter):
    try:
        # Because splitting an empty string still returns an array containing
        # an empty string
        if len(str) > 0:
            array = str.split(delimeter)
            # Remove duplicates
            array = list(OrderedDict((item, True) for item in array).keys())
        else:
            array = []
    except Exception as e:
        array = []
    return array

def getCurrentUrlWithoutTags(server_id, channel, keywords):
    url = '/' + server_id + '/'
    if len(channel) > 0:
        url += channel + '/'
    if len(keywords) > 0:
        url += 'search/' + ','.join(keywords) + '/'
    return url