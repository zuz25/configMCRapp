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
#import requests
import json
from config import client_ID, client_secret
from mcrDefs import oAuth_token, get_app_provisioning_status, get_organization_apps
client_id=client_ID
client_secret=client_secret
#Global Variables


##Classes##

class Status:
    def __init__(self,status,info):
        self.status = status
        self.info =info
    def __str__(self):
        p="status: "+ self.status +"\n"+"info: "+self.info
        return p


##Application Functions##
def exists_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def upload_file(file, applicationName):
    if file.has_file and allowed_file(file.data.filename):
        exists_directory(UPLOAD_FOLDER)
        directory = exists_directory(os.path.join(UPLOAD_FOLDER,applicationName))
        open(os.path.join(directory,file.data.filename), 'w').write(file.data.filename)
        print(file.data.filename,"Saved")
        return file.data.filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = "MCRconfigs"

ALLOWED_EXTENSIONS = set(['mp3','wav'])

class UrlConfig(Form):
    url = TextField('URL', description='Enter URL to send recordings',validators=[Required(),URL(require_tld=True, message=u'Invalid URL')])
    user = TextField('Username', description='Enter Username for URL to support Basic Authentication',validators=[Required()])
    password = PasswordField('Password', description='Enter Password for URL to support Basic  Authentication',validators=[Required(),EqualTo('confirm',message=u'Passwords must match')])
    confirm = PasswordField('Confirm Password', description='Confirm Password for URL to support Basic  Authentication',validators=[Required()])
    
    #"C:\Users\bh680n\Documents\scripts\LearnForms\MCRconfigs"
class provApplication(Form):
    #apiAdminEmail = TextField('Email', description='Enter API Admin Email (Existing or desired)', validators=[Required(),Email(message=u'Invalid Email address')])
    #applicationName = TextField('Name of Call Recording Configuration', description='Enter a name for the call recording configuration')
    url1=FormField(UrlConfig)
    #url2=FormField(UrlConfig)
    #notification = FileField('Initial Announcement audio file', description='.mp3 or .wav file of a notification to be played at start of call')
    #beep = FileField('Intermittent tone audio file', description='.mp3 or .wav file to be played at a specified interval throughout the call')
    #interval = IntegerField('Seconds between beeps', description='Enter the number of seconds between beeps 12-15s',validators=[NumberRange(min=12, max=15)])
    #endCall = FileField('Call Ending Notification', description='.mp3 or .wav file to be played at the end of 90 mins to inform callers that call will end')

    submit_button = SubmitField('Submit Form')

    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')


        
def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    #app.config['RECAPTCHA_PUBLIC_KEY'] = \
    #    '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/', methods=('GET', 'POST'))
    def index():
        access_token=oAuth_token(client_id,client_secret)
        #status=get_app_provisioning_status(access_token,appStatus_transID)
        #print(status)
        appDetails=get_organization_apps(access_token)
        #print(appDetails)
        createTimestamp=appDetails['applicationInfoList']['applicationInfo'][1]
        #print(str(createTimestamp))
        #    print(str(key)+": " + str(value) +"\n")
        #print(appDetails)
        #flash('critical message', 'critical')
        #flash('error message', 'error')
        #flash('warning message', 'warning')
        #flash('info message', 'info')
        #flash('debug message', 'debug')
        #flash('different message', 'different')
        #flash('uncategorized message')
        return render_template('index.html',appDetails=appDetails)
    
    @app.route('/provisionApplication', methods=('GET', 'POST'))
    def provisionApplication():
        form=provApplication()
        access_token=oAuth_token(client_id,client_secret)
        print('Redirect to provApplication Successful')
        if form.validate_on_submit():
            url=form.url.data
            print(url)
            #password=form.password.data
            #user=form.user.data
            #interval=form.interval.data
            #beep=form.beep
            #notification=form.notification
            #endCall=form.endCall
            #for field in form:
            #    print(str(field.name)+": "+str(field.data))
            #applicationName=form.applicationName.data
            #upload_file(beep,applicationName)
            #upload_file(notification,applicationName)
            #upload_file(endCall,applicationName)
            print('i made it here')
            flash('Your Call Recording Configuration was successfully submitted','info')
            print('i made it past the flash')
            return render_template('subAppConf.html')
        else:
            flash('Failed')
            print('Failed')
            render_template('provisionApplication.html',form=form)
        return render_template('provisionApplication.html',form=form)
    
    @app.route('/subAppConf',methods=('GET'))
    def subAppConf():
        return render_template('subAppConf.html')
    
    return app

if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)
