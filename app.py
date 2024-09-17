from flask import Flask, request, jsonify, session
from flask_cors import CORS
from PIL import Image, ImageDraw
import io
import random

app = Flask(__name__)
app.secret_key = '140388'  # Đặt SECRET_KEY để mã hóa cookie

# Cấu hình CORS
CORS(app)

@app.route('/api/captcha', methods=['GET'])
def generate_captcha():
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    operator = random.choice(['+', '-'])
    captcha_text = f"{num1} {operator} {num2}"
    answer = eval(captcha_text)
    
    captcha_token = str(random.randint(1000, 9999))
    session[captcha_token] = answer
    
    img = Image.new('RGB', (100, 50), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 10), captcha_text, fill=(0, 0, 0))
    
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    response = app.response_class(
        img_io.read(),
        mimetype='image/png',
        headers={'captcha-token': captcha_token}
    )
    return response

@app.route('/api/validate', methods=['POST'])
def validate_captcha():
    data = request.get_json()
    user_input = int(data.get('user_input'))
    captcha_token = str(data.get('captcha_token'))

    print("Session:", session)
    print("Captcha Token:", captcha_token)
    print("User Input:", user_input)
    
    if session.get(captcha_token) == user_input:
        session.pop(captcha_token, None)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})

if __name__ == '__main__':
    app.run()
