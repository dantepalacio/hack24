import os
import sys

from uuid import uuid4

from flask import Flask, request, jsonify, send_from_directory

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cv.check import check_post
from sqlite.db_operations import insert_data, get_post_id, get_table

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route("/")
def client():
    return send_from_directory('static/', 'index.html')

@app.route("/<path:path>")
def base(path):
    return send_from_directory('static/', path)


def get_attachment_from_request(file):
    *_, extension = file.filename.split(".")
    file_filename = f"{uuid4()}.{extension}"
    file_path = f"{app.config['UPLOAD_FOLDER']}{file_filename}"
    file.save(file_path)

    image_path = None
    video_path = None
    if file.mimetype.startswith("image/"):
        image_path = file_path
    elif file.mimetype.startswith("video/"):
        video_path = file_path
    return image_path, video_path


@app.route('/process_post_request', methods=['POST'])
def process_post_request():

    if not request:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400

    text = request.form.get('text')
    attachment = request.files.get("attachment")
    
    if not text and attachment is None:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400
    

    if attachment is None:
        image_path = video_path = None
    
    else:
        image_path, video_path = get_attachment_from_request(attachment)



    post_dict = {
        "text": text,
        "image": image_path,
        "video": video_path
    }

    answer = check_post(post_dict)


    if answer['text'] is not None:

        text_result = answer['text']
        print(f'TEXT:{text_result}')

    else:
        text_result = {'is_explicit': 'publish', 'reasons': []}

    if answer['image'] is not None:

        overall_image_result = answer['image']
        image_result = overall_image_result[0]
        ocr_image_result = overall_image_result[1]
        print(f'IMAGE:{image_result}')
        print(f'OCR IMAGE:{ocr_image_result}')

    else:
        overall_image_result = {'is_explicit': 'publish', 'reasons': []}


    if answer['video'] is not None:
        print()
        overall_video_result = answer['video']
        print(f'VIDEO:{overall_video_result[0]}')
        print(f'VIDEO OCR:{overall_video_result[1]}')
        
        audio_result = answer['audio']
        print(f'AUDIO FROM VIDEO:{audio_result}')

    else:
        overall_video_result = {'is_explicit': 'publish', 'reasons': []}
        audio_result = {'is_explicit': 'publish', 'reasons': []}


    overall_reasons = []
    temp_status = 'publish'
    for res_key, res_val in answer.items():
        if res_val is not None:
            for i in res_val:
                if i['is_explicit'] == 'ban':
                    temp_status = 'ban'
                    overall_reasons += i['reasons']
                elif i['is_explicit'] == 'same':
                    temp_status = 'same'
                    overall_reasons += i['reasons']
        
        else:
            continue
    

    insert_data(temp_status, text, image_path, video_path, ', '.join(overall_reasons))

    id = get_post_id(temp_status, text, image_path, video_path, ', '.join(overall_reasons))

    return jsonify({'status': temp_status, 'id': id, 'reasons': overall_reasons}), 200



@app.route('/get_posts_request', methods=['GET'])
def get_posts_request():
    
    if not request:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400
    
    results = get_table()
    
    return jsonify({'results': results}), 200



if __name__ == '__main__':
    app.run(debug=True)
