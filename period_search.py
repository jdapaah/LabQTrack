from wsse.client.requests.auth import WSSEAuth
from datetime import datetime
from sys import stderr
import requests
from api_auth import username, API_SECRET
from argparse import ArgumentParser

wsse_auth = WSSEAuth(username, API_SECRET)

"""
Given netids as args, over the provided time period, check what days the TA has
attended the queue, and print out which students they spent too much time on
"""


def main():
    parser = ArgumentParser(
        "Check the current attendance, and \nhow long they're been working with the current student")
    parser.add_argument("--netid", "-t", nargs='+', type=str, default=[], help='Search by NetID substring')
    parser.add_argument("--name", "-n", nargs='+', type=str, default=[], help='Search by name substring')
    parser.add_argument("--start", "-s", nargs="?", help="Start time as 4 digits, MMDD")
    parser.add_argument("--end", "-e", nargs="?", help="End time as 4 digits, MMDD, defualt is today")
    args = parser.parse_args()
    netid_subs = args.netid
    if not args.end:
        end_day =
    print(args.netid, args.name, args.start, args.end)
    exit(0)
    name_subs = [s.lower() for s in args.name]
    if not (name_subs or netid_subs):
        print("Needs at least one argument", file=stderr)
        exit(1)
    start_day, end_day = "2022-02-14T00:00", "2022-03-01T00:00"
    url = "https://www.labqueue.io/api/v1/queues/intro-cs-lab/roster/"
    flagged_users = []
    while url:
        result = requests.get(url, auth=wsse_auth)
        d: dict = result.json()
        for student in d['results']:
            # check that not professor
            if not student['grad_year']:
                continue
            # search ta name
            if name_subs and any(ns in student['full_name'].lower() for ns in name_subs):
                pass
            # search ta netid
            elif netid_subs and any(ns in student['netid'] for ns in netid_subs):
                pass
            else:
                continue
            stats = good_attendance(student['netid'], start_day, end_day)
            if any(stats):
                flagged_users.append((student['full_name'], student['netid'], stats))
            print('-----------------')
        url = d['next']
    # print(flagged_users)


def good_attendance(netid, start_str, end_str):
    print(netid)
    format_str = "%m%d"
    start_day = datetime.strptime(start_str, format_str)
    end_day = datetime.strptime(end_str, format_str)

    bad_cases_count = 0  # how many people you're taking too long
    max_acceptable = 5  # limit before we contact you

    missed_days = 0  # how many days you've missed
    total_count = 0  # total count of days present

    url = "https://www.labqueue.io/api/v1/requests/query/"
    payload = {"is_open": "false",
               "created_after": start_str,
               "created_before": end_str,
               "accepted_by": netid,
               "page": 1
               }

    count = {}
    bcc_list = []
    od = None
    while True:
        json = requests.get(url, auth=wsse_auth, params=payload).json()
        if 'results' in json:  # done, at null page
            results = json['results']
        else:
            break
        for sess in results:
            tc = datetime.strptime(sess['time_closed'], format_str)
            ta = datetime.strptime(sess['time_accepted'], format_str)
            curr_time, curr_day = ta.time(), ta.date()
            if curr_day not in count:  # new day
                count[curr_day] = 0
                if od:  # not first day
                    print("Number of sessions on %s:" % od, count[od])
                    for bc in bcc_list:
                        print("\tSession with %s at %s (%s) ran too long" % bc)
                bcc_list.clear()
            length = (tc - ta).seconds // 60
            count[curr_day] += (length > 5)  # update frequency dict
            #print(length)
            if length > 30:
                bad_cases_count += 1
                bcc_list.append((sess['author_full_name'], curr_time, sess['course'][-3:]))
            od = curr_day
        payload["page"] += 1
    if count:
        print("Number of sessions on %s:" % od, count[od])
        for bc in bcc_list:
            print("\tSession with %s at %s (%s) ran too long" % (bc[0], bc[1], bc[2]))

        # does NOT ACCOUNT FOR 4-HOURS SHIFTS
    print('bcc', bad_cases_count)
    print('Attended %d days in the %d week period' % (len(count), (end_day - start_day).days // 7))
    return missed_days > (end_day - start_day).days // 7, bad_cases_count >= max_acceptable
    # if count < min_acceptable:
    #     bad_cases_count += 1
    #     print('assuming one two-hour shift, not helping enough people (should be at least %d)' % min_acceptable)


if __name__ == '__main__':
    main()
