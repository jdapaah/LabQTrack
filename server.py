##
from sys import stdout, stderr
from datetime import datetime, timedelta
from argparse import ArgumentParser
import os

from flask import Flask, session, request
from flask import render_template, make_response, redirect
from flask_talisman import Talisman
from wsse.client.requests.auth import WSSEAuth
import requests

import auth
from api_auth import username, API_SECRET
from roster import student_search
import json
# from shift_search import shift

app = Flask(__name__)
app.secret_key = os.urandom(16)
wsse_auth = WSSEAuth(username, API_SECRET)
TIME_FORMAT_STR = "%H:%M"
DATE_FORMAT_STR = "%Y-%m-%d"
DATE_TIME_FORMAT_STR = DATE_FORMAT_STR+"T"+TIME_FORMAT_STR

# the full roster of the students, saved to speed up search process
full_roster = {}


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def home_page():
    if not session.get('username'):
        return redirect('/next')
    html = render_template('homescreen.html',
                           active={},
                           period={},
                           shift={})
    response = make_response(html)
    return response


@app.route('/addstudent', methods=['GET'])
def add_student():
    return make_response(
        json.dumps(
            single_student_data(
                request.args.get('netid')
            )
        )
    )


def single_student_data(netid):
    activeHtml = None
    activeDict = active(netid)
    if activeDict['present']:
        activeHtml = render_template('active/present.html', student=activeDict)
    else:
        activeHtml = render_template('active/absent.html', student=activeDict)

    return {'periodhtml': periodDataHTML(netid),
            'activehtml': activeHtml,
            'present': activeDict['present'],
            'selectedhtml': "<button class='selected {}-comp' value={}><span>{} ({})</span></button>\n".format(netid, netid, full_roster[netid]['name'], netid),
            # TODO fix this please
            'script': "<script>$('.selected').click(removeStudent)</script>"
            }


@app.route('/coursestudents', methods=['GET'])
def course_students():
    rawnetids = request.args.get('sel')
    alreadyThere = rawnetids.split(',') if rawnetids else []
    print(alreadyThere)
    course = {'126': '126', '2xx': '226', 'none':'clear'}[request.args.get('course')]
    print(course)
    add = set()
    if course == 'clear':
        remove = alreadyThere
    else:
        remove = set()
        for netid in full_roster:
            if course in full_roster[netid]['courses'] and netid not in alreadyThere:
                add.add(netid)
            elif course not in full_roster[netid]['courses'] and netid in alreadyThere:
                remove.add(netid)
        remove = list(remove)
    print('add', add)
    print('remove', remove)
    return make_response(
        json.dumps({
            'add': [single_student_data(netid) for netid in add],
            'remove': remove
        })
    )


def periodDataHTML(netid):
    try:
        pst = request.args.get('pst')
        pet = request.args.get('pet')
        netiddata = period(*time_format(pst, pet), netid)
        return render_template('periodDataWrapper.html', netiddata=netiddata)
    except (ValueError, TypeError):
        return ""


@app.route('/updateperiod', methods=['GET'])
def update_period():
    rawnetids = request.args.get('sel')
    netids = rawnetids.split(',') if rawnetids else []
    jsonObj = json.dumps([periodDataHTML(netid) for netid in netids])
    response = make_response(jsonObj)
    return response


@app.route('/students', methods=['GET'])
def search_students():
    netid = request.args.get('netid')
    name = request.args.get('name')
    year = request.args.get('year')
    selected = request.args.get('sel').split(',')

    code, students = student_search(netid, name, year, full_roster)
    # only list students that aren't in the list already
    students = {key: val for
                key, val in students.items()
                if key not in selected}
    html = ""
    if code == 0:  # success
        for i in students:
            html += "<button class='searchresult' value={}><span>{} ({})</span></button>\n".format(
                i, students[i], i)
        html += """<script>$('.searchresult').click(addStudent)</script>"""
    elif code == 1:  # success, but too many results
        html += "<em>Too many results, try narrowing your search</em>"
    elif code == 2:  # empty result
        pass
    response = make_response(html)
    return response


@app.route('/next', methods=['GET'])
def go_to_cas():
    auth.authenticate()
    return redirect('/index')


@app.route('/logout', methods=['GET'])
def logout_route():
    auth.logout()


def period(start_str, end_str, netid):
    url = "https://www.labqueue.io/api/v1/requests/query/"
    payload = {"is_open": "false",
               "created_after": start_str,
               "created_before": end_str,
               "accepted_by": netid,
               "page": 1
               }
    student_ret = {'days': {}, 'students_over': 0,
                   'students': 0, 'netid': netid,
                   'name': full_roster[netid]['name']}
    while url:
        json = requests.get(url, auth=wsse_auth, params=payload).json()
        results = json['results']
        for sess in results:
            tc = datetime.strptime(
                sess['time_closed'], DATE_TIME_FORMAT_STR)
            ta = datetime.strptime(
                sess['time_accepted'], DATE_TIME_FORMAT_STR)
            length = (tc - ta).seconds // 60
            if length < 2:
                continue
            day: str = sess['time_accepted'][:10]
            if day not in student_ret['days']:
                student_ret['days'][day] = []
            student_ret['days'][day].append({
                'start_time':   sess['time_accepted'][-5:],
                'end_time':     sess['time_closed'][-5:],
                'length':       length,
                'colorclass':   ['not-over-limit', 'over-limit'][length > 25],
                'student_info': "{} ({})".format(sess['author_full_name'], sess['course'][-3:])
            })
            student_ret['students'] += 1
            student_ret['students_over'] += student_ret['days'][day][-1]['colorclass'] == 'over-limit'
        url = json['next']
        payload = {}  # ignore the params after the first run, included in the url going forward

    return student_ret


def shift():
    return {}


def active(netid):
    url = "https://www.labqueue.io/api/v1/requests/query/"
    current_time_obj = datetime.now()
    # current_time_str = '2021-11-10T21:59'
    # current_time_obj = datetime.strptime(current_time_str, DATE_TIME_FORMAT_STR)
    payload = {
        "is_open": "true",
        # 'open_at_time': current_time_str,
        # 'accepted_before': current_time_str,
        "accepted_by": netid
    }
    sessions = requests.get(url=url,
                            auth=wsse_auth,
                            params=payload).json()['results']
    if not sessions:  # student not in queue
        return {
            'present': False,
            'netid': netid,
            'name': full_roster[netid]['name']
        }
    else:
        sess = sessions.pop()
        ta = datetime.strptime(sess['time_accepted'], DATE_TIME_FORMAT_STR)
        return {
            'present': True,
            'netid': netid,
            'info': "{} ({}) started current session with {} ({}) at {}, has been working for {} minutes.".format(
                full_roster[netid]['name'],
                netid,
                sess['author_full_name'],
                sess['author_netid'],
                ta.strftime(TIME_FORMAT_STR),
                (current_time_obj - ta).seconds // 60
            )
        }


@app.add_template_filter
def date_format(value):
    date = datetime.strptime(value, DATE_FORMAT_STR)
    return date.strftime("%B %d, %Y")


def time_format(start_str_short, end_str_short):
    start_str = datetime.strptime(start_str_short, DATE_FORMAT_STR)\
        .strftime(DATE_TIME_FORMAT_STR)
    end_time = datetime.strptime(end_str_short, DATE_FORMAT_STR)\
        + timedelta(days=1)
    end_str = end_time.strftime(DATE_TIME_FORMAT_STR)
    return start_str, end_str


def fill_roster():
    ret = {}
    roster_url = "https://www.labqueue.io/api/v1/queues/intro-cs-lab/roster/"
    while roster_url:
        result = requests.get(url=roster_url,
                              auth=wsse_auth)
        full_dict = result.json()
        for d in full_dict['results']:
            # some faculty grad_year values (cmorretti) are null instead of 0
            d['grad_year'] = d['grad_year'] if d['grad_year'] != None else 0
            ret[d['netid']] = {'name': d['full_name'],
                               # some grad_year_values are 24 vs 2024
                               'year': d['grad_year'] % 100 + 2000,
                               'courses': [s[-3:] for s in d['courses']]}
        roster_url = full_dict['next']
    return ret


if __name__ == "__main__":
    arg_parser = ArgumentParser(allow_abbrev=False,
                                description="Web Server")
    arg_parser.add_argument(
        "host",
        type=str,
        nargs='?',
        metavar="host",
        default="localhost",
        help="the ip address the server is running on",
    )
    args = arg_parser.parse_args()
    host = args.host
    print('host:', host, file=stdout)

    try:
        # redirect to HTTPS when on heroku, don't use security protocol on localhost
        if host != 'localhost':
            talisman = Talisman(app, content_security_policy=None)
            print('talisman security', file=stdout)
        else:
            print('running local host, no talisman security', file=stdout)

        port = int(os.environ.get('PORT', 5001))
        full_roster = fill_roster()

        app.run(host=host, port=port, debug=False)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)
