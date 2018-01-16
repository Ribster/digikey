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
import http.client
from flask import redirect
from flask import Flask
from flask import request
from flask import make_response
CLIENT_ID = "3f77a5f9-040a-4fc2-82b5-f33cbac4aec1"
CLIENT_SECRET = "3f77a5f9-040a-4fc2-82b5-f33cbac4aec1"
REDIRECT_URI = "https://digikeybot.herokuapp.com/callback"
# Flask app should start in global layout
app = Flask(__name__)
@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with Digi-Key</a>'
    return text % make_authorization_url()

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    if req.get("result").get("action") != "BitcoinPrice":
        return {}
    data={"response_type":"code",
          "client_id":CLIENT_ID,
          "redirect_uri":REDIRECT_URI}
    url="https://sso.digikey.com/as/authorization.oauth2"#?" + urlencode(data)
    return requests.post(url, data=data)
    #redirect
	
def make_authorization_url():
    data={"response_type":"code",
          "client_id":CLIENT_ID,
          "redirect_uri":REDIRECT_URI}
    url="https://sso.digikey.com/as/authorization.oauth2?" + urlencode(data)
    return url
def is_valid_state(state):
    return True

@app.route('/callback')
def callback():
    error=request.args.get('error','')
    code=request.args.get('code')
    if error:
        return "Error: "+error
    state=request.args.get('state','')
    if not is_valid_state(state):
        abort(403)
    code=request.args.get('code')
    if code:
        #return code
        post_data={"code":code,
		   "client_id":CLIENT_ID,
		   "client_secret":CLIENT_SECRET,
		   "redirect_uri":REDIRECT_URI,
		   "grant_type":"authorization_code"}
        

        headers={"content-type":"application/x-www-form-urlencoded"}
        response=requests.post("https://sso.digikey.com/as/token.oauth2",
                               headers=headers,
                               data=post_data)
		
        token_json=json.dump(response)
	return token_json
        '''
        if token_json["access_token"]:
            return "access_token: " + token_json["access_token"]
        else:
            return "No token"'''
	
	
		   
		   



'''
def processRequest(req):
    
    cryptocurrency=req['result']['parameters'].get('any')
    #cryptocurrency="btc_krw"
    bitdata_=""
    #for cryptocurrency in ["btc_krw", "bch_krw", "eth_krw", "xrp_krw"]:
    if cryptocurrency =="1":
    	cryptocurrency="btc_krw"
    elif cryptocurrency =="2":
    	cryptocurrency="bch_krw"
    elif cryptocurrency =="3":
    	cryptocurrency="eth_krw"
    elif cryptocurrency =="4":
    	cryptocurrency="xrp_krw"
    payload={"currency_pair": cryptocurrency}
    r= requests.get("https://api.korbit.co.kr/v1/ticker/detailed", params=payload)
    contents = r.json()
    time=datetime.datetime.fromtimestamp(contents['timestamp']/1000)
    time=time.strftime("%Y-%m-%d %H:%M:%S")
    bitdata=cryptocurrency+"\n"+\
    "체결가:"+contents['last']+"\n"+\
    "24시간 저가:"+contents['low']+"\n"+\
    "24시간 고가:"+contents['high']+"\n"+\
    "거래량:"+contents['volume']
    bitdata_+=bitdata+"\n"
    
    res = makeWebhookResult(url)
    return res
    '''


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

    app.run(debug=True, port=port, host='0.0.0.0')
'''#!/usr/bin/env python
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
app=Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook():
    error=request.args.get('error','')
    code=request.args.get('code')
    if error:
        r=make_response(makeWebhookResult('omg'))
    elif code:
        r=make_response(makeWebhookResult('we got code yeah!'))
    else:
    req=request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    r=make_response(makeWebhookResult("first"))
    r.headers['Content-Type']='application/json'
    return r
def makeWebhookResult(bitdata):
    speech=bitdata
    print("response:")
    print(speech)
    return {
        "speech":speech,
        "displayText":speech,
        }
if __name__=='__main__':
    port=int(os.getenv('PORT',5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
def save_created_state(state):
	pass
def make_authorization_url():
	# Generate a random string for the state parameter
	# Save it for use later to prevent xsrf attacks
	from uuid import uuid4
	state = str(uuid4())
	save_created_state(state)
    	data = {"response_type":"code",
        	"client_id":"3f77a5f9-040a-4fc2-82b5-f33cbac4aec1",
        	"redirect_uri":"https://digikeybot.herokuapp.com/webhook"}
	import urllib
	url = "https://sso.digikey.com/as/authorization.oauth2?" + urllib.urlencode(data)
	return url
def processRequest(req):
    	if req.get("result").get("action") != "BitcoinPrice":
        	return {}
    	url=make_authorization_url()
	return url
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
    	app.run(debug=False, port=port, host='0.0.0.0')'''
