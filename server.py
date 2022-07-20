##
from sys import stdout, stderr
from datetime import date, datetime, tzinfo
from argparse import ArgumentParser
import os
from urllib import response

from dateutil import parser
from flask import Flask, request, session
from flask import render_template, make_response, redirect, url_for
from flask_talisman import Talisman


import auth

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/', methods=['GET'])
def home_page():
    if session.get('username'):
        html = render_template('homescreen.html')
        response = make_response(html)
        return response
    else:
        return redirect('/landing')


@app.route('/landing', methods=['GET'])
def landing_page():
    html = render_template('landing.html')
    response = make_response(html)
    return response


@app.route('/next', methods=['GET'])
def go_to_cas():
    auth.authenticate()
    return redirect(url_for('homescreen'))


@app.route('/index', methods=['GET'])
def homescreen():
    if not session.get('username'):
        return redirect('/landing')  # go to landing page
    html = render_template('homescreen.html')
    response = make_response(html)
    return response

@app.route('/active', methods=['GET'])
def landing_page():
    html = render_template('active.html')
    response = make_response(html)
    return response


@app.route('/period', methods=['GET'])
def landing_page():
    html = render_template('period.html')
    response = make_response(html)
    return response


@app.route('/shift', methods=['GET'])
def landing_page():
    html = render_template('shift.html')
    response = make_response(html)
    return response


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
    print('host: ', args.host, file=stdout)

    try:
        # redirect to HTTPS when on heroku, don't use security protocol on localhost
        if host != 'localhost':
            talisman = Talisman(app, content_security_policy=None)
            print('talisman security', file=stdout)
        else:
            print('running local host, no talisman security', file=stdout)

        port = int(os.environ.get('PORT', 5001))
        app.run(host=host, port=port, debug=False)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)
