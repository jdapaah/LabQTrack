##
from sys import stdout, stderr
from datetime import date, datetime, tzinfo
from argparse import ArgumentParser
import os

from dateutil import parser
from flask import Flask, session, request
from flask import render_template, make_response, redirect
from flask_talisman import Talisman
from wsse.client.requests.auth import WSSEAuth
import requests

import auth
from api_auth import username, API_SECRET
from roster import student_search

app = Flask(__name__)
app.secret_key = os.urandom(16)
selected_students = {}

# the full roster of the students, saved to speed up search process
full_roster = {}


def fill_roster():
    ret = {}
    roster_url = "https://www.labqueue.io/api/v1/queues/intro-cs-lab/roster/"
    while roster_url:
        result = requests.get(url=roster_url,
                              auth=WSSEAuth(username, API_SECRET))
        full_dict = result.json()
        for d in full_dict['results']:
            # some faculty grad_year values (cmorretti) are null instead of 0
            d['grad_year'] = d['grad_year'] if d['grad_year'] != None else 0
            ret[d['netid']] = {'name': d['full_name'],
                               'year': d['grad_year'] % 100 + 2000}  # some grad_year_values are 24 vs 2024
        roster_url = full_dict['next']
    return ret


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def home_page():
    if not session.get('username'):
        return redirect('/next')
    html = render_template('homescreen.html')
    response = make_response(html)
    return response


@app.route('/next', methods=['GET'])
def go_to_cas():
    auth.authenticate()
    return redirect('/index')


# JS route for updating search list of students
@app.route('/students', methods=['GET'])
def search_students():
    netid = request.args.get('netid')
    name = request.args.get('name')
    year = request.args.get('year')

    code, students = student_search(netid, name, year, full_roster)
    # only list students that aren't in the list already
    students = {key: val for
                key, val in students.items()
                if key not in selected_students}
    html = ""
    if code == 0:  # success
        # html += "<ul>"
        # for i in students:
        # html += "<li class='searchresult' value={}><span>{} ({})</span></li>\n".format(
        # i, students[i], i)
        # html += "</ul>"
        for i in students:
            html += "<button class='searchresult' value={}><span>{} ({})</span></button>\n".format(
                i, students[i], i)
        html += \
            """
        <script>
        $('.searchresult').click(addStudent)
        </script>
        """ # add javascript
    elif code == 1:  # success, but too many results
        html += "<em>Too many results, try narrowing your search</em>"
    elif code == 2: # empty result
        pass
    response = make_response(html)
    return response

# JS route for adding students to the selected list


def update_student():
    # TODO selected_students from client side
    html = ""
    if selected_students:
        html += '<h4>Selected Students</h4>\n'
        for i in selected_students:
            html += "<button class='selected' value={}><span>{} ({})</span></button>\n".format(
                    i, selected_students[i], i)
        html += \
            """
    <script>
    $('.selected').click(removeStudent)
    </script>
    """

    response = make_response(html)
    return response


@app.route('/addstudent', methods=['POST'])
def add_student():
    global selected_students
    netid = request.args.get('netid')
    selected_students[netid] = full_roster[netid]['name']
    return update_student()


@app.route('/removestudent', methods=['POST'])
def remove_student():
    global selected_students
    netid = request.args.get('netid')
    selected_students.pop(netid)
    return update_student()


# @app.route('/active', methods=['GET'])
# def active_page():
#     html = render_template('active.html')
#     response = make_response(html)
#     return response


# @app.route('/period', methods=['GET'])
# def period_page():
#     html = render_template('period.html')
#     response = make_response(html)
#     return response


# @app.route('/shift', methods=['GET'])
# def shift_page():
#     html = render_template('shift.html')
#     response = make_response(html)
#     return response


@app.route('/logout', methods=['GET'])
def logout_route():
    auth.logout()


@app.route('/about', methods=['GET'])
def about_page():
    html = render_template('about.html')
    return make_response(html)


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

    # try:
    # redirect to HTTPS when on heroku, don't use security protocol on localhost
    if host != 'localhost':
        talisman = Talisman(app, content_security_policy=None)
        print('talisman security', file=stdout)
    else:
        print('running local host, no talisman security', file=stdout)

    port = int(os.environ.get('PORT', 5001))
    full_roster = fill_roster()

    app.run(host=host, port=port, debug=False)
    # except Exception as ex:
    #     print(ex, file=stderr)
    #     exit(1)
