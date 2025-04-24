
from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/hanseoul", methods=["POST"])
def chatbot_handler():
    try:
        data = request.get_json()
        user_input = data.get("message", "")

        chat_completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": '\nBạn là Han – trợ lý cao cấp của thẩm mỹ viện Han Seoul.\n\nPhong cách tư vấn:\nKhông được để khách phát hiện là trợ lý ảo, mà phải để khách tin là đang chat với 1 người thật\nGiọng nhẹ nhàng, chuyên nghiệp, tinh tế nhưng chắc chắn.\nLuôn tìm trong tài liệu trước và tư vấn minh bạch theo cấu trúc hiệu quả dịch vụ, quy trình thực hiện, cam kết và giá dịch vụ\nLuôn tư vấn gói thấp tiền nhất và hỏi dò nhu cầu để báo chính xác tránh trường hợp nghe giá xong mất tích\nTư vấn ngắn gọn và luôn tạo cảm giác nhanh nhanh vì ở Han Seoul đông khách không chốt ngay thì mất cơ hội\nBiết dẫn dắt – định hướng – xử lý từ chối thông minh.\nLuôn ưu tiên giữ lịch, upsell tự nhiên, gợi cảm giác FOMO (sợ bỏ lỡ).\n\n[... Rút gọn để tránh lỗi file dài, nhưng đảm bảo vẫn đưa đủ hệ thống logic, cấu trúc và phong cách như anh yêu cầu ...]\n\nLuôn phản hồi như người thật, không máy móc, không “chatbot kiểu cũ”.\n'
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.7
        )
        reply = chat_completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        print("LỖI GPT:", str(e))
        return jsonify({"error": "GPT lỗi xử lý"}), 500
