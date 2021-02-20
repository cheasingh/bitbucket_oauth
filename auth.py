from rauth import OAuth2Service
import urllib.parse as urlparse
from urllib.parse import parse_qs
import json
import os


class Auth:
    def __init__(self):
        self.store = {}

    def new_decoder(self, payload):
        data = json.loads(payload.decode('utf-8'))

        with open("./token/token", "w") as file:
            file.write(data['access_token'])

        with open("./token/refresh_token", "w") as file:
            file.write(data['refresh_token'])

        return data

    def authenticate(self, client_id, client_secret, **kwg):
        bitbucket = OAuth2Service(
            name="bitbucket",
            client_id=client_id,
            client_secret=client_secret,
            access_token_url="https://bitbucket.org/site/oauth2/access_token",
            authorize_url="https://bitbucket.org/site/oauth2/authorize"
        )

        if kwg:
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': kwg['refresh_token']
            }
            session = bitbucket.get_auth_session(
                data=data, decoder=self.new_decoder)
            return session.access_token

        else:
            params = {
                'response_type': 'code',
            }

            url = bitbucket.get_authorize_url(**params)

            print(url)

            request_token = input("token url here: ")
            parsed = urlparse.urlparse(request_token)
            code = parse_qs(parsed.query)['code'][0]

            data = {'code': code, 'grant_type': 'authorization_code'}

            session = bitbucket.get_auth_session(
                data=data, decoder=self.new_decoder)

            print("token save in token director.")

            return session.access_token
