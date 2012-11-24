#!/usr/bin/env python
# -*- encoding:utf8 -*-
from flask import Flask, redirect, render_template, request, url_for
application = Flask(__name__)
from pymongo import Connection
import sys
import hashlib

argvs = sys.argv

conn = Connection("localhost")
ul = conn["myapp"]["user_admin"]
name = argvs[1]
password = hashlib.sha256(argvs[2]).hexdigest()

ul.insert({"user_id":name,"password":password,"disable":0,"group_master_id":1})
admin_list = ul.find({"disable":0})
for i in admin_list:
    print i['password']
onfig = "fujikura"
#query = {"disable":0,"user_id":config} 
#admin = ul.find_one(query)

#print admin


