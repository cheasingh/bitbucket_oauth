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
        self.perpage = 25

    def pagement(self, datapoint):
        data_size = datapoint.json()['size']
        data = [datapoint.json()]
        page = 1
        while data_size > self.perpage:
            page += 1
            data_size -= self.perpage

            per_page = requests.get(
                datapoint.url, params={"page": page}, headers=self.header)

            data.append(per_page.json())
        return data

    def get_monthly_pullrequest(self, date, branch):

        pullrequest_endpoint = f"{self.endpoint}/pullrequests"
        params = {
            "q": f'state="MERGED" AND created_on > {date} AND destination.branch.name = "{branch}"',
            "pagelen": self.perpage
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
                    refresh_token = file.read()

                refresh = auth.authenticate(
                    env['sisaupp_key'], env['sisaupp_secret'], refresh_token=refresh_token)

                self.header['Authorization'] = f"Bearer {refresh}"

                rt = requests.get(pullrequest_endpoint,
                                  params=params, headers=self.header)

                if rt.json()['size'] > self.perpage:
                    return self.pagement(rt)
                else:
                    return [rt.json()]

            else:
                if r.json()['size'] > self.perpage:
                    return self.pagement(r)
                else:
                    return [r.json()]
