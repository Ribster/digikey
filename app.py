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
from flask import redirect, url_for
from flask import Flask
from flask import request, jsonify
from flask import make_response
CLIENT_ID = "3f77a5f9-040a-4fc2-82b5-f33cbac4aec1"
CLIENT_SECRET = "wY0nF1oV0xG7qQ0dC8dK2hB7wW4tW2rO4oI7pI3fN6oW7qH5yL"
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
    if req.get("result").get("action") != "PartNum":
        return {}
    text = '<a href="%s">Authenticate with Digi-Key</a>'
    url_hyper=text % make_authorization_url()
    r=makeWebhookResult("Click! "+make_authorization_url())
    r=json.dumps(r, indent=4)
    res=make_response(r) 
    res.headers['Content-Type']='application/json'
    return res


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
        token_json=response.json()
        access_token=token_json["access_token"]
        refresh_token=token_json["refresh_token"]
	
        post_data_refresh={"client_id":CLIENT_ID,
			   "client_secret":CLIENT_SECRET,
			   "refresh_token":refresh_token,
			   "grant_type":"refresh_token"}
        response_refresh=requests.post("https://sso.digikey.com/as/token.oauth2",
				       headers=headers,
				       data=post_data_refresh)
        token_json_=response_refresh.json()
        access_token_=token_json_["access_token"]
        refresh_token_=token_json_["refresh_token"]
        
        #conn = http.client.HTTPSConnection("api.digikey.com")
        payload = "{\"Part\":\"974-1011-1-ND\"}"
        headers = {
    'x-ibm-client-id': CLIENT_ID,
    'content-type': "application/json",
    'accept': "application/json",
    'x-digikey-locale-site': "KR",
    'x-digikey-locale-language': "ko", #en
    'x-digikey-locale-currency': "KRW",
    'x-digikey-locale-shiptocountry': "",
    'x-digikey-customer-id': "",
    'x-digikey-partner-id': "",
    'authorization': access_token_
    }
        response_price=requests.post("https://api.digikey.com/services/partsearch/v2/partdetails", data=payload, headers=headers)
        #conn.request("POST", "/services/partsearch/v2/partdetails", payload, headers)
        if response_price.status_code==200:
            return jsonify(response_price.json())
        else:
            return Response(response_price.text, response_price.status_code)
	
	'''
        res=response_price.json()
        #res = conn.getresponse()
        data=res['UnitPrice'['PartDetails']]
        #data = res.read()
        #data=data.decode("utf-8")
        
        return data'''
        
        
	
        
        '''return "access_token: "+access_token_ +" refresh_token: "+refresh_token_
        
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
