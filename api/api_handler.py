import os
import json

from flask import Flask, request, jsonify

from generation.generation_config import detect_explicit_comment
from cv.ocr import get_text
from cv.explicit_content_detection import detect_safe_search

app = Flask(__name__)

@app.route('/process_post_request', methods=['POST'])
def process_post_request():
    data = request.json

    text = data.get('text')
    print(text)

    if 'attachment' in request.files:
        attachment = request.files['attachment']
        attachment.save(os.path.join("uploads", attachment.filename))
        attachment_url = f"/uploads/{attachment.filename}" 


    if not data:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400
    
    # Ваша логика обработки данных может быть здесь
    

    
    return jsonify({'status': 'publish', 'reason': 'сомнительно но окэй'}), 200

if __name__ == '__main__':
    app.run(debug=True)
