# from django.shortcuts import render
# from django.http import HttpResponse
import requests
import sys
import os
import dotenv

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the highlights index.")


def get_clips():
    """
    Sends a get request to the twitch clips endpoint and returns its json response
    containing an array of clip objects.
    """
    # topGamesRes = requests.get('https://api.twitch.tv/helix/games/top')
    token_res = get_token()
    URL = 'https://api.twitch.tv/helix/clips'
    game_name = 'Call of Duty: Modern Warfare'

    CLIENT_ID = os.getenv('CLIENT_ID')
    headers = {}
    params = {}

    headers['Authorization'] = 'Bearer ' + token_res['access_token']
    headers['Client-ID'] = CLIENT_ID
    game_id = get_game_id(game_name, headers=headers)
    params['game_id'] = game_id['data'][0]['id']
    try:
        clips_res = requests.get(URL, params=params, headers=headers)
        clips_res_json = clips_res.json()
        for clip in clips_res_json['data']:
            print(clip['url'])
        return clips_res_json
    except:
        print('Raised an exception')
        print('get request error: ', sys.exc_info()[0])
        return HttpResponse('Raised an exception upon get clips request')


def get_token():
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    HEADERS = {
        'client_id': CLIENT_ID,
    }
    data = {}
    json = {}
    headers = {}
    URL = 'https://id.twitch.tv/oauth2/token'
    params = {}
    params['client_id'] = CLIENT_ID
    params['client_secret'] = CLIENT_SECRET
    params['grant_type'] = 'client_credentials'
    # scope=<space-separated list of scopes>

    headers['Authorization'] = 'Bearer ' + CLIENT_ID

    query_params = 'client_id=' + CLIENT_ID + '&' + 'client_secret=' + \
        CLIENT_SECRET + '&' + 'grant_type=client_credentials'
    print(query_params)
    response_token = requests.post(URL + '?' + query_params)
    res_token_json = response_token.json()
    print(res_token_json)
    return res_token_json


def get_game_id(game_name, params={}, headers={}):
    URL = 'https://api.twitch.tv/helix/games'
    params['name'] = game_name
    game_id_res = requests.get(URL, params=params, headers=headers)
    game_id_json = game_id_res.json()
    print(game_id_json)
    return game_id_json

# TODO: Move dotenv load to settings
dotenv.load_dotenv()
print(get_clips())
