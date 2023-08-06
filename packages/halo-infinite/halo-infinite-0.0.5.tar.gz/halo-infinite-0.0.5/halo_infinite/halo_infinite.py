from .csr import CSR
from .match import MatchListResult,Match
from .player import PlayerMatchStats
import requests
from requests.exceptions import RequestException
from furl import furl

class HaloInfinite:
    def __init__(self, gamertag, token, season, api_version):
        self.gamertag = gamertag
        self.season = season
        self.client = Client(api_version, token)
        self.csrs = None
        self.csrs_changed = False
        self.recent_matches = []
        self.new_matches = False

    def update_csr(self):
        try:
            response = self.client.request_csr(self.gamertag, self.season)
        except RequestException as e:
            raise e
        csr = CSR(response)
        self.csrs_changed = any([self.csrs[k] != csr.playlists[k] for k in ['crossplay', 'controller', 'mnk']])
        if self.csrs_changed:
            self.csrs = {
                'crossplay': csr.playlists['crossplay'],
                'controller': csr.playlists['controller'],
                'mnk': csr.playlists['mnk']
            }
            return True
        return False

    def update_recent_matches(self):
        try:
            response = self.client.request_match_list(self.gamertag, count=10, offset=1)
        except RequestException as e:
            raise e
        match_list_result = MatchListResult(response)
        match_list = [Match(m, self.gamertag) for m in match_list_result.matches]
        self.new_matches = not any([m in self.recent_matches for m in match_list])
        if self.new_matches:
            self.recent_matches = match_list
            return True
        return False

class Client:
    # single_match_url = f'https://halo.api.stdlib.com/infinite@{API_VERSION}/stats/matches/retrieve/?id={match_id}'
    # match_list_url = f'https://halo.api.stdlib.com/infinite@{API_VERSION}/stats/matches/list/?gamertag={gamer_tag}&limit.count={count}&limit.offset={offset}&mode=matchmade'

    def __init__(self, api_version, api_token):
        self.headers = {
            f'Authorization': 'Bearer ' + api_token
        }
        self.BASE_URL = f'https://halo.api.stdlib.com/infinite@{api_version}/stats/'

    def request_csr(self, gamertag, season):
        url = furl(self.BASE_URL)
        url /= 'csrs/'
        url.args['gamertag'] = gamertag
        url.args['season'] = season
        with requests.session() as s:
            s.headers.update(self.headers)
            response = s.get(url.url)
        if response.status_code != 200:
            raise requests.exceptions.RequestException
        return response.json()

    def request_match_list(self, gamertag, count, offset):
        url = furl(self.BASE_URL)
        url /= 'matches/list/'
        url.args['gamertag'] = gamertag
        url.args['limit.count'] = count
        url.args['limit.offset'] = offset
        url.args['mode'] = 'matchmade'
        with requests.session() as s:
            s.headers.update(self.headers)
            response = s.get(url.url)
        if response.status_code != 200:
            raise requests.exceptions.RequestException
        return response.json()


