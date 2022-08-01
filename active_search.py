from wsse.client.requests.auth import WSSEAuth
from datetime import datetime as dt
from argparse import ArgumentParser
from sys import stderr
import requests
from api_auth import username, API_SECRET



wsse_auth = WSSEAuth(username, API_SECRET)
"""


Command Line Args:
    Given args --netid/-t, give a substring of the TA's netid
    Given args --name/-n, give a substring of the TA's name
"""

def how_long(netid):
    format_str = "%Y-%m-%dT%H:%M"
    url = "https://www.labqueue.io/api/v1/requests/query/"
    payload = {"is_open": "true",
               "accepted_by": netid
               }
    for sess in requests.get(url, auth=wsse_auth, params=payload).json()['results']:
        ta = dt.strptime(sess['time_accepted'], format_str)
        start_time = ta.time()
        print("\tStarted current session at %s:%s, has been working for %d minutes." %
              (start_time.hour, start_time.minute, (dt.now() - ta).seconds // 60))


if __name__ == '__main__':
    main()
