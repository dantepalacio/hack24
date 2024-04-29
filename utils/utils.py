import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cv.ocr import get_text
from cv.explicit_content_detection import detect_explicit_content
from generation.generation_config import detect_explicit_comment


def explicit_content_check_from_text(result: str) -> bool:
    explicit = 'publish'
    reasons = []

    for key in result.keys():
        if result[key] == 1:
            explicit = 'ban'
            reasons.append(key)
    
    return {'is_explicit': explicit, 'reasons': reasons}
    

def explicit_content_check_from_image(result: dict) -> bool:
    explicit = 'publish'
    reasons = []

    for key in result.keys():
        if float(result[key]) == 0.6:
            explicit = 'same'
            reasons.append(key)
        elif float(result[key]) > 0.6:
            explicit = 'ban'
            reasons.append(key)

        
    
    return {'is_explicit': explicit, 'reasons': reasons}


def check_post(content: dict) -> bool:
    if content['text']:
        print(f"text: {content['text']}")
        result_for_text = detect_explicit_comment(content['text'])
        result_for_text = explicit_content_check_from_text(result_for_text)
    
    if content['image']: 
        result_for_image = detect_explicit_content(content['image'])
        result_for_image = explicit_content_check_from_image(result_for_image)

        result_for_text_from_image = get_text(content['image'])
        if result_for_text_from_image:
            result_for_text_from_image = explicit_content_check_from_text(result_for_text_from_image)
        else:
            result_for_text_from_image = {'is_explicit': 'publish', 'reasons': []}


    print(f'EXPLICIT CONTENT IN TEXT: {result_for_text}\nEXPLICIT CONTENT IN IMAGE: {result_for_image}\nEXPLICIT CONTENT IN TEXT FROM IMAGE: {result_for_text_from_image}')

    return result_for_text, result_for_image, result_for_text_from_image


if __name__ == "__main__":
    check_post({'text': 'я люблю белый порошок', 'image': '2.jpg'})