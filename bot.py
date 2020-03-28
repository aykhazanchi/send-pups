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
            quote = f'Pup alert:\n\n{data["content"]} \n- {data["author"]}'
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
        msg.body("Sorry, I only know about intellectual pups. Please say \"send pup\" if you'd like an intellectual pupper to appear")
    return str(resp)
