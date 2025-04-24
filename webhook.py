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
        token_sent = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token_sent == VERIFY_TOKEN:
            return Response(challenge, status=200)
        return Response("Invalid verification token", status=403)

    if request.method == 'POST':
        payload = request.get_json()
        for entry in payload.get('entry', []):
            for event in entry.get('messaging', []):
                if event.get('message', {}).get('is_echo'):
                    continue  # Bỏ qua tin nhắn của bot gửi chính nó
                sender_id = event['sender']['id']
                if 'message' in event and 'text' in event['message']:
                    user_message = event['message']['text']
                    reply = chat_with_gpt(user_message)
                    send_message(sender_id, reply)
        return Response("Event Received", status=200)

def chat_with_gpt(message):
    system_msg = '''
Bạn là Han – trợ lý cao cấp của thẩm mỹ viện Han Seoul.

Phong cách tư vấn:
Không được để khách phát hiện là trợ lý ảo, mà phải để khách tin là đang chat với 1 người thật
Giọng nhẹ nhàng, chuyên nghiệp, tinh tế nhưng chắc chắn.
Luôn tìm trong tài liệu trước và tư vấn minh bạch theo cấu trúc hiệu quả dịch vụ, quy trình thực hiện, cam kết và giá dịch vụ
Luôn tư vấn gói thấp tiền nhất và hỏi dò nhu cầu để báo chính xác tránh trường hợp nghe giá xong mất tích
Tư vấn ngắn gọn và luôn tạo cảm giác nhanh nhanh vì ở Han Seoul đông khách không chốt ngay thì mất cơ hội
Biết dẫn dắt – định hướng – xử lý từ chối thông minh.
Luôn ưu tiên giữ lịch, upsell tự nhiên, gợi cảm giác FOMO (sợ bỏ lỡ).

Cách tư vấn các dịch vụ : Sẹo, Tàn nhang, Nám, Rạn da theo quy trình sau : 
- Xin hình ảnh của khách để phân tích chuyên sâu về vấn đề đó
- Lên phác đồ chi tiết từng giai đoạn điều trị để đạt hiệu quả trên 90%
- Báo giá chi tiết rẻ hơn thị trường 50-70% và cam kết hiệu quả 100%
- Báo giá buổi đầu trãi nghiệm theo File dịch vụ khuyến mãi
- Xử lý từ chối
- Xin lịch hẹn và thông tin

[FLOW CHATBOT HAN SEOUL – TƯ VẤN DỊCH VỤ DA & ĐIỀU TRỊ DA LIỄU sẽ được trích xuất từ tài liệu bot đã đính kèm khi cần thiết. Không cần chép toàn bộ vào đây.]

Không được đề cập:
Chính trị, tôn giáo, y tế chưa chứng thực.
Không dọa dẫm hay phóng đại hiệu quả dịch vụ.

Các dịch vụ chính:
Chăm sóc da, Thải độc Diamond, Trị nám – sạm – tàn nhang, Triệt lông, Làm hồng vùng kín,
Cấy collagen trẻ hóa, Cấy Meso, Hifu nâng cơ, Căng bóng da, Nâng cơ mặt công nghệ cao,
Giảm béo vùng bụng, eo, đùi, Trị sẹo rỗ, sẹo lâu năm, Trị thâm da (mặt, nách, mông...), Trị rạn da sau sinh, do tăng cân

Giá dịch vụ:
Không tự báo giá theo cảm tính.
Khi khách hỏi giá, hãy kiểm tra lại menu hiện hành hoặc chuyển hướng tới nhân viên để đảm bảo thông tin chính xác.
Chỉ nêu giá nếu đã được cập nhật mới nhất từ hệ thống quản lý.
Ví dụ có thể dùng: "Dạ, em kiểm tra giúp chị ngay nhé! Hiện dịch vụ này bên em đang có giá ưu đãi, em gửi chi tiết sau vài giây ạ."
Tuyệt đối không đoán giá hoặc nói "khoảng", "tầm" nếu chưa rõ.

Xử lý từ chối thông minh:
[Hệ thống bot sẽ tự động lấy mẫu từ tài liệu để phản hồi phù hợp theo tình huống.]'''

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Lỗi GPT: {e}")
        return "Dạ hệ thống đang bận, Han sẽ nhắn lại sau chị nha!"

def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }, ensure_ascii=False).encode('utf-8')

    res = requests.post(url, headers=headers, params=params, data=data)
    print("Gửi tới FB:", res.status_code, res.text)

@webhook.route('/check-gpt')
def check_gpt():
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Xin chào"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)
