import os
import json
import requests
from prettytable import PrettyTable
import datetime

def displayTable(total=0,prev_day=0,prev_week=0):
    t = PrettyTable(['Number of open issues', 'Value'])
    t.add_row(['Total Open', total])
    t.add_row(['Opened in last 24hrs', prev_day])
    t.add_row(['Opened before 24hrs but less than 7 days ago', prev_week])
    t.add_row(['Opened more than 7 days ago ', (total-prev_week)])
    print t

def qweryUrl(url):
    #r=requests.get('http://api.github.com/Shippable/support/issues?state=opened')
    #r=requests.get("http://api.github.com/Shippable/support/issues")
    r=requests.get("https://api.github.com/issues?state=opened",auth=('kaasha','Kickst@rtyourd@y'))
    #r = requests.get('https://github.com/issues')
    print r.status_code
    print r.text
    total_open=0,prev_day=0,prev_week=0
    #Convert r to list
    #total_open=len(r)
    #print total_open
    cur_time= datetime.datetime.now()
    print cur_time
    for ele in r:
        open_time=ele[open_time]
        ##Need to create datetime object
        delta=cur_time-open_time

        if delta.days<1:
            prev_day=prev_day+1
        elif delta.day>=1 and delta.day<7:
            prev_week=prev_week+1
        else:
            pass
    return total_open,prev_day,prev_week

    

if __name__ == '__main__':
    url=raw_input('Please enter link to public GitHub repo:')
    print "Link:{0}".format(url)
    cmd= "git ls-remote "+url
    #Check whether repo exists
    if os.system(cmd) != 0:
        raise AssertionError('Incorrect link entered!')
    total,prev_day,prev_week=qweryUrl(url)
    displayTable(total,prev_day,prev_week)
