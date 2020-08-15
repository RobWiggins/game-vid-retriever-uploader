# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import sys
import os
import dotenv
import json
from .twitch_retriever import TwitchRetriever
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the highlights index.")


def clips(request):
    """
    Sends a get request to the twitch clips endpoint and returns its json response
    containing an array of clip objects.
    """
    try:
        retriever = TwitchRetriever()
        # topGamesRes = requests.get('https://api.twitch.tv/helix/games/top')
        game_name = 'Call of Duty: Modern Warfare' # TODO: get name from query params
        game_id = retriever.get_game_id(game_name)
        game_clips_json = retriever.get_clips(game_id)
        print(game_clips_json)
        return JsonResponse(game_clips_json)
    except:
        print('Raised an exception')
        print(sys.exc_info()[0])
        return HttpResponse('Raised an exception upon get clips request')
