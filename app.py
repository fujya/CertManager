#!/usr/bin/env python
# -*- encoding:utf8 -*-

import os
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash ,escape
from werkzeug.contrib.sessions import Session, SessionStore
from cPickle import HIGHEST_PROTOCOL
from random import random
from flask import json
from pymongo import Connection
import datetime
import hashlib

#import local modules
from lib.MemcachedSessionStore.MemcachedSessionStore import *




#settings
mongo_connect='localhost'
session_key_name = '_sess_myflask'
memd_host = '127.0.0.1:11211'
memd_prefix = 'myflask:'
LISTEN_HOST = '0.0.0.0'
DEBUG_FLG = 'True'


class MyFlask( SessionMixin, Flask): pass



class Logout(object):
    def __init__(self):
        pass
    def __new__(cls):
        session.pop('username', None)
        return redirect(url_for("index"))

class SessionCheck(object):
    def __init__(self):
        pass
    def __new__(cls):
        if session.has_key('username'):
            return True
        else:
            return False

#Flask Initialize
application = MyFlask(__name__)
application.session_key = session_key_name
application.session_store = MemcachedSessionStore([memd_host], memd_prefix)
#MongoDB connection
conn = Connection(mongo_connect)


@application.route("/add_user", methods=['POST'])
def add_user():
    name = request.form['name']
    ul.insert({"name":name})
    return redirect(url_for("index"))


@application.route("/login", methods=['POST','GET'])
def login():
    error = None

    if SessionCheck():
        return render_template('login_after.html')

    if request.method == 'POST':
        query = {"disable":0,"user_id":request.form['username']}
        ul = conn["myapp"]["user_admin"]
        admin = ul.find_one(query)
        if not admin:
            error = 'Invalid username'
        elif hashlib.sha256(request.form['password']).hexdigest() != admin['password']:
            error = 'Invalid password'
        else:
           session['username'] = request.form['username']
           return redirect(url_for('index'))
    return render_template('login.html', error=error)



@application.route('/')
def index():
    if SessionCheck():
        return render_template('login_after.html')
    else:
        return render_template('login.html', error="")




@application.route('/logout')
def logout():
    if SessionCheck(): return Logout()
    
    return redirect(url_for("index"))


if __name__ == "__main__":
    application.run(host=LISTEN_HOST, debug=DEBUG_FLG)
