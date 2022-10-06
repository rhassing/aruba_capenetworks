#!/usr/bin/python3
### Script made by Rob Hassing (rob.hassing@deltics.nl) 01-04-2021

import json
import sys
import getopt
import urllib
import requests

#def help():
#    print ("Display help!!!")

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "n:i:k:u:vh"
long_options = ["node=", "appid=", "appkey=", "url=", "verbose", "help"]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print ("Display help!!!")
    print (str(err))
    sys.exit(2)

verbose = False
# Evaluate given options
for current_argument, current_value in arguments:
    if current_argument in ("-v", "--verbose"):
        print ("Enabling verbose mode")
        verbose = True
    elif current_argument in ("-h", "--help"):
        print ("Usage: check_uxi-node -u https://api.capenetworks.com/v1/nodes/ -n <node-id> -i <APP id> -k <APP Key>")
        sys.exit(2)
    elif current_argument in ("-n", "--node"):
        node = (current_value)
#        if(len(node) == 0):
#           print ("Yes")
#        else :
#           help()
    elif current_argument in ("-i", "--appid"):
        appids = (current_value)
    elif current_argument in ("-k", "--appkey"):
        appkey = (current_value)
    elif current_argument in ("-u", "--url"):
        url = (current_value)


#url = "https://api.capenetworks.com/v1/nodes/"
url2 = url+node
headers = {'accept': 'application/json', 'X-API-KEY': appkey, 'X-APP-ID': appids}

try:
    t = requests.get(url2, headers=headers)

except requests.exceptions.Timeout:
    print("Timeout on URL")
except requests.exceptions.TooManyRedirects:
    print("Too many redirects")
except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    raise SystemExit(e)

if t.status_code == 404:
    print("Resource Not Found")
    sys.exit(1)

r_dictionary= t.json()


ok_msg = []
warnings = []
criticals = []

if verbose == True:
   print(r_dictionary)
if 'status' not in r_dictionary:
    for p in r_dictionary['payload']['state_summary']['sensors']:
            name = p['name']
            state = p['state']
            if state == "good":
                ok_msg.append(f"OK: {str(name)}, status is: {str(state)}")
            elif state == "warning":
                for w in r_dictionary['payload']['issue_summary']:
                    code = w['code']
                    desc = w['description']
                    warnings.append(f"WARNING: {str(name)}, status is: {str(state)}, Description: {str(desc)}")
            else:
                for c in r_dictionary['payload']['issue_summary']:
                    code = c['code']
                    desc = c['description']
                    criticals.append(f"CRITICAL: {str(name)} status is {str(state)} Description: {str(desc)}")
    if len(criticals) > 0:
        print('\n'.join(criticals))
        print('\n'.join(warnings))
        print('\n'.join(ok_msg))
        sys.exit(2)
    elif len(warnings) > 0:
        print('\n'.join(warnings))
        print('\n'.join(ok_msg))
        sys.exit(1)
    else:
        print('\n'.join(ok_msg))
        sys.exit(0)
elif r_dictionary['status']==500:
    print("WARNING: " + "error conecting to api statuscode is: " + str(r_dictionary['status']))

