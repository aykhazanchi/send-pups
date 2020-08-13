from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/pup', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'send pup' in incoming_msg:
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} \n- {data["author"]}, the pup'
        else:
            quote: 'I could not retrieve a quote at this time'
        msg.body(quote)
        r = requests.get('https://api.thedogapi.com/v1/images/search')
        if r.status_code == 200:
            data = r.json()
            data = data[0]
            pup = data['url']
        msg.media(pup)
        responded = True

    if not responded:
        response = f'Sorry, I am unable to {incoming_msg} right now. Please type "send pup" if you\'d like an intellectual pupper to appear'
        msg.body(response)
    return str(resp)
