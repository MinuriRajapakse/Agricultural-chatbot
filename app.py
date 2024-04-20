import requests
from flask import Flask, render_template, request, jsonify

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json['message']
    print("User Message:", user_message)
    rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
    rasa_response_json = rasa_response.json()
    print("Rasa Response:", rasa_response_json)
    bot_response1 = rasa_response_json[0]['text'] if rasa_response_json else 'Sorry, I didn\'t understand that.'
    bot_image = None
    bot_response2 = None
    bot_response3 = None
    bot_response4 = None
    bot_response5 = None

    for response_item in rasa_response_json:
        if 'image' in response_item:
            bot_image = response_item['image']
            break

    if len(rasa_response_json) > 1:
        try:
            bot_response2 = rasa_response_json[1]['text']
        except KeyError:
            bot_response3 = rasa_response_json[2]['text'] if rasa_response_json else None

    if len(rasa_response_json) > 2:
        try:
            bot_response3 = rasa_response_json[2]['text']
        except KeyError:
            bot_response4 = rasa_response_json[3]['text'] if rasa_response_json else None

    if len(rasa_response_json) > 3:
        try:
            bot_response4 = rasa_response_json[3]['text']
        except KeyError:
            bot_response5 = rasa_response_json[4]['text'] if rasa_response_json else None

    return jsonify({'response_1': bot_response1, 'image': bot_image, 'response_2': bot_response2,
                    'response_3': bot_response3, 'response_4': bot_response4, 'response_5': bot_response5})


if __name__ == "__main__":
    app.run(debug=True)
