from call import Bitbucket
import requests
from pprint import pp

repo = Bitbucket()
monthly_report = repo.get_monthly_pullrequest()


def prep_data(data):
    branch_info = []

    if len(data) > 1:
        total = 0
        for i in data:
            total += len(i['values'])
            for x in i['values']:
                dev_info = {
                    'title': x['title'],
                    'commit': x['destination']['commit']['hash'],
                    'created_on': x['created_on'],
                    'author': x['author']['nickname'],
                    'fullname': x['author']['display_name'],
                }
                branch_info.append(dev_info)
        return branch_info

    for x in data[0]['values']:
        dev_info = {
            'title': x['title'],
            'commit': x['destination']['commit']['hash'],
            'created_on': x['created_on'],
            'author': x['author']['nickname'],
            'fullname': x['author']['display_name'],
        }
        branch_info.append(dev_info)

    return branch_info


pp(prep_data(monthly_report))
