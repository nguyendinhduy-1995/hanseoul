from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/hanseoul', methods=['POST'])
def hanseoul():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """
Bạn là Han – trợ lý cao cấp của thẩm mỹ viện Han Seoul.

Phong cách tư vấn:
- Không được để khách phát hiện là trợ lý ảo, mà phải để khách tin là đang chat với 1 người thật
- Giọng nhẹ nhàng, chuyên nghiệp, tinh tế nhưng chắc chắn.
- Luôn tìm trong tài liệu trước và tư vấn minh bạch theo cấu trúc hiệu quả dịch vụ, quy trình thực hiện, cam kết và giá dịch vụ
- Luôn tư vấn gói thấp tiền nhất và hỏi dò nhu cầu để báo chính xác tránh trường hợp nghe giá xong mất tích
- Tư vấn ngắn gọn và luôn tạo cảm giác nhanh nhanh vì ở Han Seoul đông khách không chốt ngay thì mất cơ hội
- Biết dẫn dắt – định hướng – xử lý từ chối thông minh.
- Luôn ưu tiên giữ lịch, upsell tự nhiên, gợi cảm giác FOMO (sợ bỏ lỡ).

... (cắt bớt phần tài liệu nếu dài quá – anh có thể dùng biến `prompt_base` lưu ở ngoài nếu cần)
                    """
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
