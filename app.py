#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import requests
import json
import os
import datetime

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():

	error=request.args.get('error','')
	code = request.args.get('code')
	if error:
		r=make_response(makeWebhookResult("omg"))

	elif code:
		r=make_response(makeWebhookResult("we got code yeah!"))

	else:
    	req = request.get_json(silent=True, force=True)
    	print("Request:")
    	print(json.dumps(req, indent=4))
     	#print 'API.AI Parameters'
    	#print json.dumps(parameters, indent=4)
    	processRequest(req)
    	
    	# print(res)
    	
    r.headers['Content-Type'] = 'application/json'
    return r

def make_authorization():
    data = {"response_type":"code",
        	"client_id":"3f77a5f9-040a-4fc2-82b5-f33cbac4aec1",
        	"redirect_uri":"https://digikeybot.herokuapp.com/webhook"}
 
	r = requests.post("https://sso.digikey.com/as/authorization.oauth2", data=data)


def processRequest(req):
    if req.get("result").get("action") != "BitcoinPrice":
        return {}
    

    make_authorization()


def makeWebhookResult(bitdata):
    
    speech = bitdata
	
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],       
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')