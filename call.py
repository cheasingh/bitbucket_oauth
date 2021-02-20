from auth import Auth
from os import environ as env
import requests


auth = Auth()


class Bitbucket:
    def __init__(self):
        try:
            with open("./token/token", "r") as file:
                self.header = {
                    "Authorization": f"Bearer {file.read()}"
                }
        except FileNotFoundError:
            token = auth.authenticate(
                env['sisaupp_key'], env['sisaupp_secret'])

            self.header = {
                "Authorization": f"Bearer {token}"
            }

        self.endpoint = "https://api.bitbucket.org/2.0/repositories/auppteam/www.sisaupp.com"

    def get_monthly_pullrequest(self):
        pullrequest_endpoint = f"{self.endpoint}/pullrequests"
        params = {
            "q": 'state="MERGED" AND created_on > 2021-02-19 AND destination.branch.name = "aupp_staging3"'
        }

        try:
            r = requests.get(pullrequest_endpoint,
                             params=params, headers=self.header)
            status_code = r.status_code

        except requests.exceptions.ConnectionError as err:
            print(err)

        else:

            if status_code == 401:
                print("token expired")

                with open("./token/refresh_token", "r") as file:
                    refresh_token = file.reader()

                refresh = auth.authenticate(
                    env['sisaupp_key'], env['sisaupp_secret'], refresh_token=refresh_token)

                self.header['Authorization'] = f"Bearer {refresh}"

                rt = requests.get(pullrequest_endpoint,
                                  params=params, headers=self.header)

                print(rt.json()['size'])

            else:
                print(r.json()['size'])
