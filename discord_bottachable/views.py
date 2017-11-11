from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template.defaulttags import register
from django.db.models import Q
from discord_bottachable.models import Server, Link

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

# Create your views here.
def index(request):
    return render(request, 'index.html', {'servers': Server.objects.all()})

def server(request, server_id, tags='', keywords=''):
    if request.method == 'POST':
        return redirect(getRedirectUrl(request, server_id, tags, keywords))
    else:
        keywords = str_to_array(keywords, ',')
        s = get_object_or_404(Server, discord_id=server_id)
        all_links = Link.objects.filter(server_id=s)

        tags = str_to_array(tags, ',')

        if len(keywords) > 0:
            all_links = filterByKeywords(all_links, keywords)
        
        if len(tags) > 0:
            all_links = filterByTags(all_links, tags)

        paginator = Paginator(all_links, 10)

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
            'tags': tags,
            'current_tags': ','.join(tags),
            'current_keywords': ','.join(keywords),
            'tag_links': getTagLinks(all_links, server_id, tags, keywords)
        })

def getRedirectUrl(request, server_id, tags, keywords):
    # convert to array
    keywords = str_to_array(request.POST.get('keywords', None), ',')
    # trim every keyword
    for i, keyword in enumerate(keywords):
        keywords[i] = keyword.strip()
    # convert back to string
    keywords = ','.join(keywords)

    url = '/' + server_id + '/'

    if len(keywords) > 0:
        url += 'search/' + keywords + '/'
    if len(tags) > 0:
        url += 'tags/' + ','.join(str_to_array(tags, ','))

    return url

def getTagLinks(all_links, server_id, tags, keywords):
    urls = {}
    for l in all_links:
        url = ''
        urls[l.id] = {}
        for t in l.tags.all():
            url = ''
            if len(keywords) > 0:
                url = 'search/' + ','.join(keywords) + '/'
            if len(tags) > 0:
                if t.name not in tags:
                    url += 'tags/' + ','.join(tags) + ',' + t.name
                else:
                    url += 'tags/' + ','.join(tags)
            elif len(tags) == 0:
                url += 'tags/' + t.name
            urls[l.id][t.id] = url
    return urls

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
