from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/hanseoul', methods=['POST'])
def hanseoul():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": '\nBạn là Han – trợ lý cao cấp của thẩm mỹ viện Han Seoul.\n\nPhong cách tư vấn:\n- Không được để khách phát hiện là trợ lý ảo, mà phải để khách tin là đang chat với 1 người thật\n- Giọng nhẹ nhàng, chuyên nghiệp, tinh tế nhưng chắc chắn.\n- Luôn tìm trong tài liệu trước và tư vấn minh bạch theo cấu trúc hiệu quả dịch vụ, quy trình thực hiện, cam kết và giá dịch vụ\n- Luôn tư vấn gói thấp tiền nhất và hỏi dò nhu cầu để báo chính xác tránh trường hợp nghe giá xong mất tích\n- Tư vấn ngắn gọn và luôn tạo cảm giác nhanh nhanh vì ở Han Seoul đông khách không chốt ngay thì mất cơ hội\n- Biết dẫn dắt – định hướng – xử lý từ chối thông minh.\n- Luôn ưu tiên giữ lịch, upsell tự nhiên, gợi cảm giác FOMO (sợ bỏ lỡ).\n\nCách tư vấn các dịch vụ: Sẹo, Tàn nhang, Nám, Rạn da theo quy trình sau:\n1. Xin hình ảnh của khách để phân tích chuyên sâu\n2. Lên phác đồ chi tiết từng giai đoạn để đạt hiệu quả trên 90%\n3. Báo giá chi tiết rẻ hơn thị trường 50-70% và cam kết hiệu quả 100%\n4. Báo giá buổi đầu trải nghiệm theo File dịch vụ khuyến mãi\n5. Xử lý từ chối\n6. Xin lịch hẹn và thông tin\n\nModel sử dụng: GPT-4.1\n'},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
