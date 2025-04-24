
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/hanseoul", methods=["POST"])
def chatbot_handler():
    data = request.get_json()
    user_input = data.get("message", "")

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "Bạn là Han – trợ lý ảo cao cấp của thẩm mỹ viện Han Seoul. Tư vấn dịch vụ da, xử lý từ chối khéo léo, không nói sai thông tin. Trả lời như người thật, không máy móc."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    reply = response['choices'][0]['message']['content']
    return jsonify({"reply": reply})
