import base64
import json
import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='Username for VOXI account', type=str)
parser.add_argument('-p', '--password', help='Password for VOXI account', type=str)
parser.add_argument('-l', '--loginfile', help='Login file in json forat with username and password', type=str)
parser.add_argument('-d', '--debug', help='Dump the json returned in more detailed form', action='store_true')
parser.add_argument('-j', '--json', help='Only return the json data gathered', action='store_true')
args = parser.parse_args()

if args.debug or args.json:
    import pprint


signurl = 'https://www.voxi.co.uk/auth/sign-in'

if args.loginfile:
    infile = open(args.loginfile)
    jsontmp = json.loads(''.join(infile.readlines()))
    args.username = jsontmp['username']
    args.password = jsontmp['password']

payload = {
    'username': args.username.upper(),
    'password': base64.b64encode(args.password.encode()),
}

session_requests = requests.session()
session_requests.get(signurl)
result = session_requests.post(signurl, data = payload, headers = dict(referer = signurl))

if args.debug:
    print('login: {}'.format(result))        

result = session_requests.post('https://www.voxi.co.uk/dashboard', headers = dict(referer = signurl))
jresult = json.loads(result.text)

if args.debug:
    pprint.pprint(jresult['data']['currentPlan'])
elif args.json:
    pprint.pprint(jresult)    
else:
    print('Data: {}/{}'.format(jresult['data']['currentPlan']['dataRemaining'],
                               jresult['data']['currentPlan']['dataTotal']))
    print('International Voice: {}/{}'.format(jresult['data']['extrasAndPasses'][0]['consumables'][0]['remaining'],
                                              jresult['data']['extrasAndPasses'][0]['consumables'][0]['total']))	

