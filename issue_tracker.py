import os
import json
import requests
from prettytable import PrettyTable
import datetime
from urlparse import urlparse
from time import sleep


def displayTable(total=0, prev_day=0, prev_week=0):
    t = PrettyTable(['Number of open issues', 'Value'])
    t.add_row(['Total Open', total])
    t.add_row(['Opened in last 24hrs', prev_day])
    t.add_row(['Opened before 24hrs but less than 7 days ago', prev_week])
    t.add_row(['Opened more than 7 days ago ', (total - prev_week)])
    print t


def qweryUrl(url):
    # Get the path of url by parsing it
    url = urlparse(url)
    page = 1
    data = []
    flag = 0
    prev_day = 0
    prev_week = 0
    
    while flag == 0:
        try:
            r = requests.get('http://api.github.com/repos' + url.path +
                             '/issues?state=open' + '&page=' + str(page) + '&per_page=100')
            print r.status_code
            time.sleep(5)
            if r.status_code == 404:
                raise AssertionError('Private or wrong repo!')
                break
            print r.text
            print len(r.json())
            data.append(r.json())
            if len(r.json()) == 0:
                flag = 1
            page = page + 1
        except requests.exceptions.ConnectionError:
            flag = 1
            print "Connection refused!"
    
    # Total open issues are number of elements added to data
    total_open = len(data)
    print total_open

    # Find current time
    cur_time = datetime.datetime.now()
    print cur_time

    for ele in data:
        open_time = ele[created_at]
        # Need to create datetime object
        delta = cur_time - open_time

        if delta.days < 1:
            prev_day = prev_day + 1
        elif delta.day >= 1 and delta.day < 7:
            prev_week = prev_week + 1
        else:
            pass

    return total_open, prev_day, prev_week


if __name__ == '__main__':
    url = raw_input('Please enter link to public GitHub repo:')
    print "Link:{0}".format(url)
    total, prev_day, prev_week = qweryUrl(url)
    displayTable(total, prev_day, prev_week)
