import os
import json
import sys
import base64


from flask import Flask, request, jsonify


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generation.generation_config import detect_explicit_comment
from cv.ocr import get_text
from cv.explicit_content_detection import detect_explicit_content
from utils.b64_decode import save_image_from_base64
from utils.utils import check_post

app = Flask(__name__)

@app.route('/process_post_request', methods=['POST'])
def process_post_request():
    data = request.json

    text = data.get('text')
    attachment = data.get('attachment')


    if attachment is not None:
        image_path = save_image_from_base64(base64_string=attachment, filename='1')


        # detect_explicit_content(image_path)

        # recognized_text_from_image = get_text(image_path)

        # if len(recognized_text_from_image) > 0:
        #     print(detect_explicit_comment(recognized_text_from_image))
        # else:
        #     print('Текст в изображении не обнаружен')

        
    # with open(image_path, "rb") as image_file:
    #     image_content = image_file.read()

    post_dict = {
        "text": text,
        "image": image_path
    }

    result_for_text, result_for_image, result_for_text_from_image = check_post(post_dict)
    os.remove('uploads\\1.jpg')######################
    if result_for_text['is_explicit'] == 'ban' or result_for_image['is_explicit']=='ban' or result_for_text_from_image['is_explicit']=='ban':
        return jsonify({'status': 'ban', 'reason': [{'comment':result_for_text['reasons'], 'image':result_for_image['reasons'], 'text_in_image':result_for_text_from_image['reasons']}]}), 200
    

    elif result_for_text['is_explicit'] == 'publish' and result_for_image['is_explicit']=='same' and result_for_text_from_image['is_explicit']=='publish':
        return jsonify({'status': 'same', 'reason': [{'comment':result_for_text['reasons'], 'image':result_for_image['reasons'], 'text_in_image':result_for_text_from_image['reasons']}]}), 200
    

    elif result_for_text['is_explicit'] == 'publish' and result_for_image['is_explicit']=='publish' and result_for_text_from_image['is_explicit']=='publish':
        return jsonify({'status': 'publish', 'reason': [{'comment':result_for_text['reasons'], 'image':result_for_image['reasons'], 'text_in_image':result_for_text_from_image['reasons']}]}), 200


        
    # result_comment = detect_explicit_comment(text)
    # print(result_comment)



    if not data:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400
    
    

    

    
    return jsonify({'status': 'publish', 'reason': 'сомнительно но окэй'}), 200

if __name__ == '__main__':
    app.run(debug=True)
