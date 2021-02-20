from call import Bitbucket
import requests
from pprint import pp
import datetime as dt
import pandas as pd


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


repo = Bitbucket()

filter_date = input("Get data since YYYY-MM-DD: ")
filter_branch = input("1- master, 2- demo, 3- prepro: ")

branch = ["master", "sisdemo", "aupp_staing3"]

time = dt.datetime.now()
date = time.strftime("%Y-%m")
query_month = filter_date if filter_date != "" else f"{date}-01"
query_branch = branch[int(filter_branch)] if filter_branch != "" else branch[0]

monthly_report = repo.get_monthly_pullrequest(
    date=query_month, branch=query_branch)

data_dict = prep_data(monthly_report)

print(f"total development: {len(data_dict)}")

export_data = input("export to csv? Y/N: ").lower()

if export_data == "y":
    pd.DataFrame(prep_data(monthly_report)).to_csv("data.csv", index=False)

print("exited")
