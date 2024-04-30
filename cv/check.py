import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cv.ocr import get_text
from cv.explicit_content_detection import detect_explicit_content
from generation.generation_config import detect_explicit_comment, get_text_from_audio, detect_spam_comment
from cv.take_frames import detect_explicit_content_from_video
from utils.utils import explicit_content_check_from_image, explicit_content_check_from_text




def check_post(content: dict) -> bool:
    answer = {'text': None, 'image': None, 'video': None, 'audio': None}
    if content['text'] is not None:
        # print(f"text: {content['text']}")
        comment_result = detect_explicit_comment(content['text'])
        comment_result = explicit_content_check_from_text(comment_result)

        is_spam = detect_spam_comment(content['text'])
        print(f'SPAMM TEST\n {is_spam}')
        if comment_result['is_explicit'] == 'ban':
            if is_spam['status']:
                comment_result['reasons'] = comment_result['reasons'] + is_spam['reasons']
        else:
            if is_spam['status']:
                comment_result['is_explicit'] = 'ban'
                comment_result['reasons'] = comment_result['reasons'] + is_spam['reasons']

    
        answer['text'] = [comment_result]
    
    if content['image'] is not None:
        result_for_image = detect_explicit_content(content['image'])
        result_for_image = explicit_content_check_from_image(result_for_image)

        result_for_text_from_image = get_text(content['image'])

        if result_for_text_from_image['text'] != '' and len(result_for_text_from_image['text']) > 0:
            result_for_text_from_image = detect_explicit_comment(result_for_text_from_image['text'])
            result_for_text_from_image = explicit_content_check_from_text(result_for_text_from_image)

        else:
            result_for_text_from_image = {'is_explicit': 'publish', 'reasons': []}

        # print(f'EXPLICIT CONTENT IN TEXT: {comment_result}\nEXPLICIT CONTENT IN IMAGE: {result_for_image}\nEXPLICIT CONTENT IN TEXT FROM IMAGE: {result_for_text_from_image}')

        answer['image'] = [result_for_image, result_for_text_from_image]
    
    if content['video'] is not None:
        result_for_video = detect_explicit_content_from_video(content['video'])

        temp_explicit_audio_content = get_text_from_audio(content['video'])

        temp_explicit_audio_content = temp_explicit_audio_content['text']
        
        if len(temp_explicit_audio_content) == 0:
            results_for_audio = {'is_explicit': 'publish', 'reasons': []}
        else:
            results_for_audio = detect_explicit_comment(temp_explicit_audio_content)
            results_for_audio = explicit_content_check_from_text(results_for_audio)


        answer['video'] = result_for_video
        answer['audio'] = [results_for_audio]
        


    return answer


if __name__ == "__main__":
    print(check_post({'text': 'я люблю гнилых оленей', 'image': '2.jpg', 'video': 'dear.mp4'}))