import os
import sys

from uuid import uuid4

from flask import Flask, request, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cv.check import check_post
from utils.utils import generate_random_int_id
from sqlite.db_operations import insert_data, view_table

app = Flask(__name__,
            static_url_path='', 
            static_folder='static/',
            template_folder='templates/')


app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/process_post_request', methods=['POST'])
def process_post_request():

    if not request:
        return jsonify({'status': 'ban', 'reason': 'Пустое тело'}), 400
    

    image = request.files['attachment']
    image_filename = str(uuid4())+".jpg"
    image_path = f'uploads/{image_filename}'
    image.save(image_path)


    video = request.files['video']
    video_filename = str(uuid4())+".mp4"
    video_path = f'uploads/{video_filename}'
    video.save(video_path)


    text = request.form.get('text')


    post_dict = {
        "text": text,
        "image": image_path,
        "video": video_path
    }

    answer = check_post(post_dict)


    text_result = answer['text']
    print(f'TEXT:{text_result}')

    overall_image_result = answer['image']
    image_result = overall_image_result[0]
    ocr_image_result = overall_image_result[1]
    print(f'IMAGE:{image_result}')
    print(f'OCR IMAGE:{ocr_image_result}')

    print()
    overall_video_result = answer['video']
    print(f'VIDEO:{overall_video_result[0]}')
    print(f'VIDEO OCR:{overall_video_result[1]}')
    
    audio_result = answer['audio']
    print(f'AUDIO FROM VIDEO:{audio_result}')




    overall_reasons = []
    temp_status = 'publish'
    for res_key, res_val in answer.items():
        for i in res_val:
            if i['is_explicit'] == 'ban':
                temp_status = 'ban'
                overall_reasons += i['reasons']
            elif i['is_explicit'] == 'same':
                temp_status = 'same'
                overall_reasons += i['reasons']
    

    id = generate_random_int_id()
    # ЗАПИСЬ В БД

    insert_data(id, temp_status, text, image_path, video_path, ', '.join(overall_reasons))
    print('success added to BD')

    view_table()

    return jsonify({'status': temp_status, 'id':id, 'reasons': overall_reasons}), 200
                    # {'status': str, 'id':int, 'reasons': list}

     

if __name__ == '__main__':
    app.run(debug=True)
