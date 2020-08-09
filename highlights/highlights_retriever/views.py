from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the highlights index.")


def get_clips(request):
    # topGamesRes = requests.get('https://api.twitch.tv/helix/games/top')
    # gamesRes = requests.get('https://api.twitch.tv/helix/games')
    clipsRes = requests.get('https://api.twitch.tv/helix/clips?name=Call%20of%20Duty%3A%20Modern%20Warfare')
    print(clipsRes.json())