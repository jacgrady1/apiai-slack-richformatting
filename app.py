#!/usr/bin/env python

import urllib
import json
import os
import requests

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

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):

    if req.get("result").get("action") == "yahooWeatherForecast":
        print("processing yahoo weather forecast");
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = makeYqlQuery(req)
        if yql_query is None:
            return {}
        yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
        print(yql_url)

        result = urllib.urlopen(yql_url).read()
        print("yql result: ")
        print(result)

        data = json.loads(result)
        res = makeWebhookResult(data)
        return res
    elif req.get("result").get("action") == "fetchtrending":
        # data = makeSlickQuery()
        res = makeTrendingWebhookResult()
        print("res")
        print res
        return res
    else:
        return {}

def makeSlickQuery():
    print("fetching")
    cookies = {
        'AO': 'u=1',
        'F': 'a=0rgKcNsMvSCF0N5045RXwlxetl37NSgLCONbUe_aBsVDfUwkvCZ24aGPxj3j3DeG1AlDbqI-&b=k9_6&d=.mC3jjE9vM7t9g6Elm6HUDPjNFcVWUhcfXnTH3n_bpy_GkiEIsTbWE8-',
        'PH': 'l=en-US&i=us&fn=93JSgadVdkQBNEpn5uD4_Q--',
        'YBY': 'id%3D196244%26userid%3Dgongxun%26sign%3DJOpT5ARLg6Bm37sshW6n2Z0ifZTd611IbUf8UFaB5gqCxWl4oWRW0LGmUJu2NY5CcK062tjYtfW747x4RCTjk2atwW13ea1M0VWSh4cQ6eTYOByoU_2up.ZidYPU2OJ1yuFrUiqhWwKW6uhB0lB2ULglZ1qYlfMwWPRnV.py2yI3PaqJvC1evgQGGPwcEQja52A0RT6yCQ3ihbBWhpBhx4J6wQvFsFulvJRoCKL4yZLVMeEY2ua6eCZes1nXcFwizg8pdetUoBR8EF_fgsZXQyigcQuchMO8HPXAJJ0sH6Z_d6W_l8gsDhDPp2en5oiRCGRNLSsP78nKXZ1sM3XlOg--%26time%3D1495138558%26expires%3D600%26ip%3D209.131.62.113%26roles%3D%7C1.IE%7C10197.B%7C10633.U%7C11330.G%7C11524.AFMTP%7C11555.U%7C121.U%7C13.V%7C20.U%7C3.I%7C4.E%7C50.U%7C6951.I%7C6982.I%7C7181.I%7C7741.U%7C8031.B%7C8165.E%7C9026.T%7C9108.R%7C%5BProperty%7CViewers%5D%7Cdomain.yahoo.com%7Cip2.10.72.122.245%7Ckve.1%7Ckvr.1%7Csign2.MEQCIDr88GWHhlLANjsC1EwhVfR2bUT8LbKGI3TVwZujtRjlAiBDBzinMQtUpy2Pbop1veDyoFNfS6RgO9FDmNtAjNRkng--%7C',
        'B': 'bhfekh1c179k1&b=4&d=xVBu5qNpYEJ5gR3CUS8mPw--&s=fh&i=YY8hVV0_RJ3_yFo2mZCj',
        'ucs': 'lnct=1492122051&spt=1495141795',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://slick.video.yahoo.com/trending-articles',
        'X-Requested-With': 'XMLHttpRequest',
        'If-None-Match': 'W/"4ea8-i0Yamx7dR2ZiW2a8ZZM7FtdDFuE"',
        'Connection': 'keep-alive',
    }

    params = (
        ('returnMeta', 'true'),
    )

    response = requests.get('https://slick.video.yahoo.com/api/articleService', headers=headers, cookies=cookies)
    print("response: ")
    responseArr = json.loads(response.text)[:5]

    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # requests.get('https://slick.video.yahoo.com/api/articleService?returnMeta=true', headers=headers, cookies=cookies)
    print(responseArr)
    data = []
    for elem in responseArr:
        elemObj = str(elem.get("url"))
        data.append("www.yahoo.com"+elemObj)

    return data

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"

def makeTrendingWebhookResult():

    speech = "Check these links out?"

    print("Response:")
    print(speech)

    slack_message = {
        "text": speech,
        "attachments": [
            {
                "title": "channel1",
                "title_link": "www.yahoo.com/news/fm-us-understands-turkeys-position-against-syrian-kurds-101104760.html",
                "color": "#36a64f",
            } , {
                "title": "channel2",
                "title_link": "www.yahoo.com/news/fm-us-understands-turkeys-position-against-syrian-kurds-101104760.html",
                "color": "#36a64f",
            }, {
                "title": "channel3",
                "title_link": "www.yahoo.com/news/fm-us-understands-turkeys-position-against-syrian-kurds-101104760.html",
                "color": "#36a64f",
            }
        ]
    }

    print(json.dumps(slack_message))

    return {
        "speech": speech,
        "displayText": speech,
        "data": {"slack": slack_message},
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    slack_message = {
        "text": speech,
        "attachments": [
            {
                "title": channel.get('title'),
                "title_link": channel.get('link'),
                "color": "#36a64f",

                "fields": [
                    {
                        "title": "Condition",
                        "value": "Temp " + condition.get('temp') +
                                 " " + units.get('temperature'),
                        "short": "false"
                    },
                    {
                        "title": "Wind",
                        "value": "Speed: " + channel.get('wind').get('speed') +
                                 ", direction: " + channel.get('wind').get('direction'),
                        "short": "true"
                    },
                    {
                        "title": "Atmosphere",
                        "value": "Humidity " + channel.get('atmosphere').get('humidity') +
                                 " pressure " + channel.get('atmosphere').get('pressure'),
                        "short": "true"
                    }
                ],

                "thumb_url": "http://l.yimg.com/a/i/us/we/52/" + condition.get('code') + ".gif"
            }
        ]
    }

    print(json.dumps(slack_message))

    return {
        "speech": speech,
        "displayText": speech,
        "data": {"slack": slack_message},
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
