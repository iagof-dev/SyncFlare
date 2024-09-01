import requests
import datetime

# this is just one time use to get the DNS RECORD ID
# once you have the DNS RECORD ID you can just use the main file
# to update the DNS record
# Only use this file if you don't have the ID or
# if you want to get from another dns record

# -----

cfZoneID = '';
cfApiKey = '';
cfEmail = '';

# -----

def makeGetRequest(url, headers):
    response = requests.get(url,headers=headers)
    return response.json()

if(cfZoneID == '' and cfApiKey == '' and cfEmail == ''):
    print('Enter your Cloudflare API Key and Email to get the DNS RECORD ID\n')
    cfApiKey = input('CF API KEY:\n')
    cfEmail = input('CF Email:\n')
    cfZoneID = input('Domain ZoneID:\n')

    for i in range(0, 100):
        print(' ')


result = makeGetRequest('https://api.cloudflare.com/client/v4/zones/' + cfZoneID + '/dns_records', headers={'X-Auth-Email': cfEmail, 'X-Auth-Key': cfApiKey})
print(result)

now = datetime.datetime.now()
file_name = 'output-' + now.strftime("%Y-%m-%d-%H_%M_%S") + '.txt'
with open(file_name, 'w') as f:
     f.write(str(result))
     f.close()

print('\n\nAbove is all records dns informations')
print('also saved as ' + file_name)