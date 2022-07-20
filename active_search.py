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
def main():
    parser = ArgumentParser("Check the current attendance, and \nhow long they're been working with the current student")
    parser.add_argument("--netid", "-t", nargs='+', type=str, default=[], help='Search by NetID substring')
    parser.add_argument("--name", "-n", nargs='+', type=str, default=[], help='Search by name substring')
    args = parser.parse_args()
    netid_subs = args.netid
    name_subs = [s.lower() for s in args.name]
    if not (name_subs or netid_subs):
        print("Needs at least one argument", file=stderr)
        exit(1)
    url = "https://www.labqueue.io/api/v1/queues/intro-cs-lab/roster/"
    while url:
        result = requests.get(url, auth=wsse_auth)
        d: dict = result.json()
        for student in d['results']:
            # check that not professor
            if student['grad_year'] == None:
                continue
            # search ta name
            if name_subs and any(ns in student['full_name'].lower() for ns in name_subs):
                pass
            # search ta netid
            elif netid_subs and any(ns in student['netid'] for ns in netid_subs):
                pass
            else:
                continue
            print(student['netid'], student['full_name'])
            how_long(student['netid'])
            print('-----------------')
        url = d['next']


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
