# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import sys
import os
import json
import datetime
from dotenv import load_dotenv
# TODO: Not resolving or finding this import - broken
# import strict_rfc3339

class TwitchRetriever:
    """
    Talks to the twitch API - responsible for retrieving authentication,
    video clips, and other stream gaming statistics.
    """

    def __init__(self):
        self.APP_AUTH_TOKEN_URL = 'https://id.twitch.tv/oauth2/token'
        self.CLIPS_URL = 'https://api.twitch.tv/helix/clips'
        self.GAMES_URL = 'https://api.twitch.tv/helix/games'

    def __get_token(self):
        """
        Returns a twitch application authentication token from the twitch API oauth2 token endpoint.
        """
        load_dotenv()
        CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
        CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
        print(CLIENT_ID, CLIENT_SECRET)
        HEADERS = {
            'client_id': CLIENT_ID,
        }
        data = {}
        json = {}
        headers = {}
        params = {}
        params['client_id'] = CLIENT_ID
        params['client_secret'] = CLIENT_SECRET
        params['grant_type'] = 'client_credentials'

        headers['Authorization'] = 'Bearer ' + CLIENT_ID

        query_params = 'client_id=' + CLIENT_ID + '&' + 'client_secret=' + \
            CLIENT_SECRET + '&' + 'grant_type=client_credentials'
        print(query_params)
        response_token = requests.post(
            self.APP_AUTH_TOKEN_URL + '?' + query_params)
        res_token_json = response_token.json()
        print(res_token_json)
        return res_token_json['access_token']

    def get_game_id(self, game_name):
        """
        Returns the game id for the specified game name from the games endpoint.
        """
        headers = {}
        params = {}
        token = self.__get_token()
        headers['Authorization'] = 'Bearer ' + token

        headers['Client-ID'] = os.getenv('TWITCH_CLIENT_ID')
        params['name'] = game_name
        game_id_res = requests.get(
            self.GAMES_URL, params=params, headers=headers)
        game_id_json = game_id_res.json()
        print(json.dumps(game_id_json) + 'GAME ID JSON')
        return game_id_json['data'][0]['id']

    def get_clips(self, game_id):
        """
        Sends a get request to the twitch clips endpoint and returns its json response
        containing an array of clip objects.
        """
        # topGamesRes = requests.get('https://api.twitch.tv/helix/games/top')
        token = self.__get_token()
        game_name = 'Call of Duty: Modern Warfare'

        CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
        headers = {}
        params = {}
        headers['Authorization'] = 'Bearer ' + token
        headers['Client-ID'] = CLIENT_ID
        # game_id = self.get_game_id(game_name, headers=headers)
        params['game_id'] = game_id
        params['first'] = 50 # MAX 100
        # TODO: The below time conversion is broken - figure out the right way to do it
        # params['started_at'] = strict_rfc3339.timestamp_to_rfc3339_utcoffset((datetime.datetime.now() - datetime.timedelta(9)))
        print(params)
        # try:
        clips_res = requests.get(
            self.CLIPS_URL, params=params, headers=headers)
        clips_res_json = clips_res.json()
        print('THE GET_CLIPS JSON RES' + (json.dumps(clips_res_json)))
        for clip in clips_res_json['data']:
            print(clip['url'])
        return clips_res_json
        # except:
        # print('Raised an exception')
        # print('get request error: ', sys.exc_info()[0])
        # return HttpResponse('Raised an exception upon get clips request')
