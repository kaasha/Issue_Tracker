import os
import json
import requests
from prettytable import PrettyTable
from datetime import datetime
from urlparse import urlparse


def displayTable(total=0, prev_day=0, prev_week=0):
    t = PrettyTable(['Number of open issues', 'Value'])
    t.add_row(['Total Open', total])
    t.add_row(['Opened in last 24hrs', prev_day])
    t.add_row(['Opened before 24hrs but less than 7 days ago', prev_week])
    t.add_row(['Opened more than 7 days ago ', (total - prev_day - prev_week)])
    print t


def qweryUrl(url):
    # Get the path of url by parsing it
    url = urlparse(url)
    page = 1
    data = []
    flag = 0
    prev_day = 0
    prev_week = 0
    total_open=0
    while flag == 0:
        try:
            url_get='https://api.github.com/repos'+url.path+'/issues?state=open&page=' + str(page) + '&per_page=100'
            r = requests.get(url_get)
            if r.status_code == 404:
                raise AssertionError('Private or wrong repo!')
                break
            total_open= total_open + len(r.json())
            data = json.loads(r.text)
            if page%5 == 0:
                print "Please wait..."
            # Find current time as datetime object
            dt_obj1 = datetime.now()
            for ele in data:
                open_time = ele['created_at']
                #Create datetime object for open time of issue
                dt_obj2=datetime.strptime(open_time,'%Y-%m-%dT%H:%M:%SZ')
                delta = dt_obj1 - dt_obj2
                #Compare based on delta time
                if delta.days < 1:
                    prev_day = prev_day + 1
                elif delta.days >= 1 and delta.days < 7:
                    prev_week = prev_week + 1
                else:
                    pass
            ##Check whether its last page
            if len(r.json()) < 100:
                flag = 1
            page = page + 1
        ##Handling connection exception    
        except requests.exceptions.ConnectionError:
            flag = 1
            print "Connection refused!"
    
    return total_open, prev_day, prev_week


if __name__ == '__main__':
    url = raw_input('Please enter link to public GitHub repo:')
    print "Link:{0}".format(url)
    total, prev_day, prev_week = qweryUrl(url)
    displayTable(total, prev_day, prev_week)
