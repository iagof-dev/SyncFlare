import requests
import sys
import json

#---------------------

# Ngrok API
# https://dashboard.ngrok.com/api-keys

ngrokApiKey = ''
ngrokIP = ''
ngrokPort = 0

# Cloudflare API
# https://developers.cloudflare.com/api/
# https://dash.cloudflare.com/profile/api-tokens

cfApiKey = ''
cfEmail = ''

# Domain Details
cfZoneID = ''
cfDNSRecordID = ''
cfDNSname = ''

#---------------------

if ((cfZoneID == '' and cfApiKey == '' and cfEmail == '') or (cfZoneID == '') or (cfApiKey == '') or (cfEmail == '')):
    print('CF API Key and Email are required')
    sys.exit()

if ngrokApiKey == '':
    print('Ngrok Token is required')
    sys.exit()

def makeGetRequest(url, headers):
    response = requests.request("GET", url, headers=headers)
    return response.json()

def makePatchRequest(url, headers, data):
    response = requests.request("PATCH", url, json=data, headers=headers)
    return response.json()


ngrokResult = makeGetRequest('https://api.ngrok.com/endpoints', headers = {'Ngrok-Version': '2', 'Authorization': f'Bearer {ngrokApiKey}'})
ngrokValue = ngrokResult['endpoints'][0]['hostport']
ngrokIP, ngrokPort = ngrokValue.split(":")

updateData = { "type": "SRV", "name": cfDNSname, "data": { "port": ngrokPort, "priority": 1, "weight": 1, "target": ngrokIP }, "comment": "update port by SF" }
headers = { "Content-Type": "application/json", "X-Auth-Email": cfEmail, "X-Auth-Key": cfApiKey }
url = 'https://api.cloudflare.com/client/v4/zones/' + cfZoneID + '/dns_records/' + cfDNSRecordID

responseCF = makePatchRequest(url, headers={"Content-Type": "application/json", 'X-Auth-Email': cfEmail, 'X-Auth-Key': cfApiKey}, data=updateData)
if(responseCF['success'] == 'true' or responseCF['success'] == True):
    print('DNS Record Updated')
else:
    print('Failed to update DNS Record')
    print(responseCF)
