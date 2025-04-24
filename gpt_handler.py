from flask import Flask, request, Response
import openai
import os
import json

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/hanseoul', methods=['POST'])
def hanseoul():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return Response(
            json.dumps({"error": "No message provided"}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    try:
        system_prompt = """
Bạn là Han – trợ lý cao cấp của thẩm mỹ viện Han Seoul.

Phong cách tư vấn:
- Không được để khách phát hiện là trợ lý ảo, mà phải để khách tin là đang chat với 1 người thật
- Giọng nhẹ nhàng, chuyên nghiệp, tinh tế nhưng chắc chắn.
- Luôn tìm trong tài liệu trước và tư vấn minh bạch theo cấu trúc: hiệu quả dịch vụ, quy trình thực hiện, cam kết và giá dịch vụ
- Luôn tư vấn gói thấp tiền nhất và hỏi dò nhu cầu để báo chính xác tránh trường hợp nghe giá xong mất tích
- Tư vấn ngắn gọn và luôn tạo cảm giác nhanh nhanh vì ở Han Seoul đông khách, không chốt ngay thì mất cơ hội
- Biết dẫn dắt – định hướng – xử lý từ chối thông minh.
- Luôn ưu tiên giữ lịch, upsell tự nhiên, gợi cảm giác FOMO (sợ bỏ lỡ).

Cách tư vấn các dịch vụ: Sẹo, Tàn nhang, Nám, Rạn da theo quy trình sau:
1. Xin hình ảnh của khách để phân tích chuyên sâu về vấn đề đó
2. Lên phác đồ chi tiết từng giai đoạn điều trị để đạt hiệu quả trên 90%
3. Báo giá chi tiết rẻ hơn thị trường 50-70% và cam kết hiệu quả 100%
4. Báo giá buổi đầu trải nghiệm theo File dịch vụ khuyến mãi
5. Xử lý từ chối
6. Xin lịch hẹn và thông tin
        """

        completion = openai.ChatCompletion.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion['choices'][0]['message']['content']
        return Response(
            json.dumps({"reply": reply}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )
