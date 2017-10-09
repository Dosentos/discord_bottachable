from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from discord_bottachable.models import Server, Link


# Create your views here.
def index(request):
    return render(request, 'index.html', {'servers': Server.objects.all()})


def server(request, server_id):
    s = get_object_or_404(Server, discord_id=server_id)
    links = Link.objects.filter(server_id=s)
    return render(request, 'server.html', {
        'links': links,
        'server_name': s.name
    })
