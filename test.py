#!/usr/bin/env python

from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators, PasswordField
from wtforms.validators import Required, NumberRange, URL, Email, EqualTo
import requests
from flask.ext.appconfig import AppConfig
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import requests
import json
from config import client_ID, client_secret

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    create_app()
    app.run()