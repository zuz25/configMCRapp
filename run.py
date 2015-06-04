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

client_id=client_ID
client_secret=client_secret
#Global Variables

callback = 'https://www.dummyurl.dummyurl.com/1234'
appStatus_transID = 'wkL3epYBs2rYuPdVXY8'
##Classes##

class Status:
    def __init__(self,status,info):
        self.status = status
        self.info =info
    def __str__(self):
        p="status: "+ self.status +"\n"+"info: "+self.info
        return p

## MCR API FUNCTIONS ##

# oAuth Token Generation
def oAuth_token(client_id,client_secret):
    url = 'https://api.att.com/oauth/v4/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    values = {'client_id' : client_id, 'client_secret' : client_secret, 'scope' : 'ACOMM', 'grant_type' : 'client_credentials'}
    r=requests.post(url,headers=headers, data=values)
    print(r.text)
    access_token=r.json()['access_token']
    return access_token

def get_app_provisioning_status(access_token,appStatus_transID):
    url = 'https://api.att.com/auditedCommunication/v1/applicationProvisioningTransactions/'+appStatus_transID
    headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json'}
    r = requests.get(url,headers=headers)
    data=json.loads(r.text)
    #status= Status(data['applicationProvisioningStatus']['status'],data['applicationProvisioningStatus']['statusInfo'])
    #print(str(data['applicationProvisioningStatus']['status']))
    return str(data['applicationProvisioningStatus']['status'])

##Create Application
#createApp_callback = 'https://www.dummyurl.dummyurl.com/1234'
#url = 'https://api.att.com/auditedCommunication/v1/applications'
#headers = {'Authorization':'Bearer '+access_token,'Content-Type':'application/gzip','x-callbackUri':createApp_callback}
#fn='MCR-Onboarding-Form_OrecX.tar.gz'
#appfiles = {'file': open('MCRappConfigs/'+fn, 'rb')}
#r = requests.post(url,headers=headers,files=appfiles)
#print(r.headers['x-provisioningTransactionId'])
#f=open('log_orecx.txt','a')
#f.write('App Provisioning Transaction ID ' + str(r.headers['x-provisioningTransactionId'])+'\n')

#print(r.text)
#
## Get Organization Applications
def get_organization_apps(access_token):
    url = 'https://api.att.com/auditedCommunication/v1/applications'
    headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json','x-callbackUri':callback}
    params = {'responseData':'metadata'}
    r = requests.get(url,headers=headers,params=params)
    data=json.loads(r.text)
    return data
#
## Get Specific Application Detail
#application = '133'
#url = 'https://api.att.com/auditedCommunication/v1/applications/'+application
#headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json','x-callbackUri':callback}
#r = requests.get(url,headers=headers)
#print(r.text)
#
## Get phone numbers subscribers provisioned to specific application
#application = '133'
#limit = '10'
#index = '0'
#url = 'https://api.att.com/auditedCommunication/v1/applications/'+application+'/subscriptions'
#headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json','x-callbackUri':callback}
#params = {'limit': limit, 'index':index}
#r = requests.get(url,headers=headers,params=params)
#print(r.text)
#
## Get Subscription details --NEEDS TO BE FINISHED
#subNumbers = {'subscriptionNumber':'+12769200800'}
#url = 'https://api.att.com/auditedCommunication/v1/applications/'+application+'/subscriptions'
#headers = {'Authorization':'Bearer '+access_token,'Content-Type':'application/json','x-callbackUri':callback}
#data = {'subscriptions':subNumbers}
#r = requests.get(url,data=json.dumps(data),params=params)
#print(r.text)

##Remove Subscriber
#Application='133'
#subNumbers = '+12769200800'
#url = 'https://api.att.com/auditedCommunication/v1/applications/'+Application+'/subscriptions'
#headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json','x-callbackUri':callback}
#params = {'subscriptions':subNumbers}
#r = requests.get(url,headers=headers,params=subNumbers)
#print(r.text)

## Get Application Provisioning Status
#subStatus_transID = ''
#url = 'https://api.att.com/auditedCommunication/v1/subscriptionProvisioningTransactions/'+subStatus_transID
#headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json'}
#r = requests.get(url,headers=headers)
#print(r.text)


#Provision Subscriber

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
class ExampleForm(Form):
    apiAdminEmail = TextField('Email', description='Enter API Admin Email (Existing or desired)', validators=[Required(),Email(message=u'Invalid Email address')])
    applicationName = TextField('Name of Call Recording Configuration', description='Enter a name for the call recording configuration')
    url1=FormField(UrlConfig)
    url2=FormField(UrlConfig)
    notification = FileField('Initial Announcement audio file', description='.mp3 or .wav file of a notification to be played at start of call')
    beep = FileField('Intermittent tone audio file', description='.mp3 or .wav file to be played at a specified interval throughout the call')
    interval = IntegerField('Seconds between beeps', description='Enter the number of seconds between beeps 12-15s',validators=[NumberRange(min=12, max=15)])
    endCall = FileField('Call Ending Notification', description='.mp3 or .wav file to be played at the end of 90 mins to inform callers that call will end')

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
        form = ExampleForm()
        access_token=oAuth_token(client_id,client_secret)
        status=get_app_provisioning_status(access_token,appStatus_transID)
        #print(status)
        appDetails=get_organization_apps(access_token)
        #print(appDetails)
        createTimestamp=appDetails['applicationInfoList']['applicationInfo'][1]
        print(str(createTimestamp))
        
        #    print(str(key)+": " + str(value) +"\n")
        #print(appDetails)
        if form.validate_on_submit():
            url=form.url.data
            password=form.password.data
            user=form.user.data
            interval=form.interval.data
            beep=form.beep
            notification=form.notification
            endCall=form.endCall
            #for field in form:
            #    print(str(field.name)+": "+str(field.data))
            applicationName=form.applicationName.data
            upload_file(beep,applicationName)
            upload_file(notification,applicationName)
            upload_file(endCall,applicationName)
            status=get_app_provisioning_status(appStatus_transID)
            return render_template('index.html',form=form,beep=beep.data.filename,notification=notification.data.filename, endCall=notification.data.filename)
        else:
            print(form.errors)
        #flash('critical message', 'critical')
        #flash('error message', 'error')
        #flash('warning message', 'warning')
        #flash('info message', 'info')
        #flash('debug message', 'debug')
        #flash('different message', 'different')
        #flash('uncategorized message')
        return render_template('index.html', form=form,status=status,appDetails=appDetails)
    return app

if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)
