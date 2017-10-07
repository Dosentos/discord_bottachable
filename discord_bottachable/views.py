from django.shortcuts import render
from django.http import HttpResponse
from discord_bottachable.models import Link

# Create your views here.
def index(request):
    try:
        links = Link.objects.all()
        print("Loaded successfully")
    except:
        print("Error")
        if not links:
            print("Is empty")
    context = {'links': links}
    return render(request, 'index.html', context)