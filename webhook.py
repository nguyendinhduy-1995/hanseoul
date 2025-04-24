from flask import request, Response, Blueprint
import os
import openai
import requests
import json

webhook = Blueprint('webhook', __name__)

VERIFY_TOKEN = "hanseoul123"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

openai.api_key = os.getenv("OPENAI_API_KEY")

@webhook.route('/webhook', methods=['GET', 'POST'])
def handle_webhook():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token_sent == VERIFY_TOKEN:
            return Response(challenge, status=200)
        return Response("Invalid verification token", status=403)

    if request.method == 'POST':
        payload = request.get_json()
        for entry in payload.get('entry', []):
            for event in entry.get('messaging', []):
                sender_id = event['sender']['id']
                if 'message' in event and 'text' in event['message']:
                    user_message = event['message']['text']
                    reply = chat_with_gpt(user_message)
                    send_message(sender_id, reply)
        return Response("Event Received", status=200)

def chat_with_gpt(message):
    system_msg = "Bạn là Han – trợ lý cao cấp của thẩm mỹ viện Han Seoul. Giọng nhẹ nhàng, chuyên nghiệp, tinh tế nhưng chắc chắn và cực kỳ thông minh."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": message}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "Dạ hệ thống đang bận, Han sẽ nhắn lại sau chị nha!"

def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    requests.post(url, headers=headers, params=params, json=data)
