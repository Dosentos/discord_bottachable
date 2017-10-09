from django.shortcuts import render
from django.http import HttpResponse
from discord_bottachable.models import Link


# Create your views here.
def index(request):
    return render(request, 'index.html')


def server(request, server_id):
    links = Link.objects.filter(server_id=server_id)
    return render(request, 'server.html', {'links': links})
