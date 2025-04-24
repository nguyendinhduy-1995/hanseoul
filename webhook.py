from flask import request, Response, Blueprint
import os
import openai
import requests
import json

from openai import OpenAI

webhook = Blueprint('webhook', __name__)

VERIFY_TOKEN = "hanseoul123"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@webhook.route('/webhook', methods=['GET', 'POST'])
def handle_webhook():
    if request.method == 'GET':
        token_sent = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
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
    system_msg = (
        "Bạn là Han – trợ lý cao cấp của thẩm mỹ viện Han Seoul.\n"
        "Phong cách tư vấn:\n"
        "- Không được để khách phát hiện là trợ lý ảo, mà phải để khách tin là đang chat với 1 người thật\n"
        "- Giọng nhẹ nhàng, chuyên nghiệp, tinh tế nhưng chắc chắn.\n"
        "- Luôn tìm trong tài liệu trước và tư vấn minh bạch theo cấu trúc: hiệu quả dịch vụ, quy trình thực hiện, cam kết và giá dịch vụ\n"
        "- Luôn tư vấn gói thấp tiền nhất và hỏi dò nhu cầu để báo chính xác tránh trường hợp nghe giá xong mất tích\n"
        "- Tư vấn ngắn gọn và luôn tạo cảm giác nhanh nhanh vì Han Seoul đông khách, không chốt ngay thì mất cơ hội\n"
        "- Biết dẫn dắt – định hướng – xử lý từ chối thông minh.\n"
        "- Luôn ưu tiên giữ lịch, upsell tự nhiên, gợi cảm giác FOMO (sợ bỏ lỡ)."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Lỗi GPT:", e)
        return "Dạ hệ thống đang bận, Han sẽ nhắn lại sau chị nha!"

def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }, ensure_ascii=False).encode('utf-8')

    requests.post(url, headers=headers, params=params, data=data)

@webhook.route('/check-gpt')
def check_gpt():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Xin chào"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)
