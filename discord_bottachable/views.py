from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from discord_bottachable.models import Server, Link

import logging

# Create an instance of logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'index.html', {'servers': Server.objects.all()})


def server(request, server_id):
    s = get_object_or_404(Server, discord_id=server_id)
    all_links = Link.objects.filter(server_id=s)
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
        'server_name': s.name
    })
