from .csr import CSR
import requests
from furl import furl

class HaloInfinite:
    def __init__(self, name, gamertag, token, season, api_version):
        self.name = name
        self.gamertag = gamertag
        self.season = season
        self.client = Client(api_version, token)
        self.data = None
        if not self.update_csr():
            return


    def update_csr(self):
        response = self.client.request_csr(self.gamertag, self.season)
        csr = CSR(response)
        self.data = {
            'crossplay': csr.playlists['crossplay'],
            'controller': csr.playlists['controller'],
            'mnk': csr.playlists['mnk']
        }

class Client:
    # single_match_url = f'https://halo.api.stdlib.com/infinite@{API_VERSION}/stats/matches/retrieve/?id={match_id}'
    # match_list_url = f'https://halo.api.stdlib.com/infinite@{API_VERSION}/stats/matches/list/?gamertag={gamer_tag}&limit.count={count}&limit.offset={offset}&mode=matchmade'

    def __init__(self, api_version, api_token):
        self.session = requests.session()
        self.session.headers.update({
            f'Authorization': 'Bearer ' + api_token
        })
        self.BASE_URL = f'https://halo.api.stdlib.com/infinite@{api_version}/stats/'

    def request_csr(self, gamertag, season):
        url = furl(self.BASE_URL)
        url /= 'csrs/'
        url.args['gamertag'] = gamertag
        url.args['season'] = season
        response = self.session.get(url.url)
        print(response.json())
        if response.status_code != 200:
            raise Exception
        return response.json()


