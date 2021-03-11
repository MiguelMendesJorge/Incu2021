from flask import Flask, request
import requests
import json

############## Bot details ##############
bot_name = 'miguelautotest@webex.bot'
#roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vMWM4ZWRjMjQtMzBmYi0zZTFjLTk3OTgtODU5ZGVlMTYyNThl'
token = 'YWFlMDU4OWYtOWIxZS00YTQzLTg1ZGYtODE0ZDQxMDIzYmE2MDJiMDExY2YtNWJi_PF84_consumer'

header = {"content-type": "application/json; charset=utf-8", 
 "authorization": "Bearer " + token}

############## Flask Application ##############
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sendMessage():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages'
    msg = {"roomId": webhook["data"]["roomId"]}
    sender = webhook["data"]["personEmail"]
    message = getMessage()
    if (sender != bot_name):
        if (message == "help"):
            msg["markdown"] = "Welcome to **Tea Bot**! I will tell you the benefits of any tea. \n List of available commands: \n- tea [teaName] \n- help"
        elif (message.split(' ')[0] == "tea"):
            teaName = message.split(' ')[1]
            response = requests.get('https://tea-api-vic-lo.herokuapp.com/tea/' + teaName)
            msg["markdown"] = response.text
            if(response.text[0] != "\""):
                msg["markdown"] = teaName + " tea originates from " + response.json()["origin"] + ". " + response.json()["description"] + ' Go make yours!'
        else:
            msg["markdown"] = "Sorry! I didn't recognize that command. Type **help** to see the list of available commands."
        requests.post(url,data=json.dumps(msg), headers=header, verify=True)

def getMessage():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages/' + webhook["data"]["id"]
    get_msgs = requests.get(url, headers=header, verify=True)
    message = get_msgs.json()['text']
    return message

app.run(debug = True)