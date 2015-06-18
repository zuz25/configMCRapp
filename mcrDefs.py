#!/usr/bin/env python
import requests
import json
callback = 'https://www.dummyurl.dummyurl.com/1234'
appStatus_transID = 'wkL3epYBs2rYuPdVXY8'

## MCR API FUNCTIONS ##

# oAuth Token Generation
def oAuth_token(client_id,client_secret):
    url = 'https://api.att.com/oauth/v4/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    values = {'client_id' : client_id, 'client_secret' : client_secret, 'scope' : 'ACOMM', 'grant_type' : 'client_credentials'}
    r=requests.post(url,headers=headers, data=values)
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


## Get Organization Applications
def get_organization_apps(access_token):
    url = 'https://api.att.com/auditedCommunication/v1/applications'
    headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json','x-callbackUri':callback}
    params = {'responseData':'metadata'}
    r = requests.get(url,headers=headers,params=params)
    data=json.loads(r.text)
    return data

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