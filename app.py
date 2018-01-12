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
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    
    #print 'API.AI Parameters'
    #print json.dumps(parameters, indent=4)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "BitcoinPrice":
        return {}
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

    data = {"response_type":"code",
        "client_id":"3f77a5f9-040a-4fc2-82b5-f33cbac4aec1",
        "redirect_uri":"https://digikeybot.herokuapp.com/webhook"}

	r = requests.post("https://sso.digikey.com/as/authorization.oauth2?",
                     allow_redirects=False)










    '''time=datetime.datetime.fromtimestamp(contents['timestamp']/1000)
    time=time.strftime("%Y-%m-%d %H:%M:%S")'''

    bitdata=cryptocurrency+"\n"+\
    "체결가:"+contents['last']+"\n"+\
    "24시간 저가:"+contents['low']+"\n"+\
    "24시간 고가:"+contents['high']+"\n"+\
    "거래량:"+contents['volume']

    bitdata_+=bitdata+"\n"
    
    
    
    res = makeWebhookResult(bitdata_)
    return res


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