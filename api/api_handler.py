import os
import json
import sys
import base64


from flask import Flask, request, jsonify


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generation.generation_config import detect_explicit_comment
from cv.ocr import get_text
from cv.explicit_content_detection import detect_safe_search
from utils.b64_decode import save_image_from_base64

app = Flask(__name__)

@app.route('/process_post_request', methods=['POST'])
def process_post_request():
    data = request.json

    text = data.get('text')
    attachment = data.get('attachment')


    if attachment is not None:
        image_path = save_image_from_base64(base64_string=attachment, filename='1')


        detect_safe_search(image_path)

        recognized_text_from_image = get_text(image_path)

        if len(recognized_text_from_image) > 0:
            print(detect_explicit_comment(recognized_text_from_image))
        else:
            print('Текст в изображении не обнаружен')

        
        result_comment = detect_explicit_comment(text)
        print(result_comment)

        

    if not data:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400
    
    

    

    
    return jsonify({'status': 'publish', 'reason': 'сомнительно но окэй'}), 200

if __name__ == '__main__':
    app.run(debug=True)
