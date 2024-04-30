import cv2
import os
import sys
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generation.generation_config import detect_explicit_comment, detect_spam_comment
from cv.ocr import get_text
from cv.explicit_content_detection import detect_explicit_content
from utils.utils import explicit_content_check_from_text, explicit_content_check_from_image


def detect_explicit_content_from_video(path):
    # Открываем видеофайл
    video_capture = cv2.VideoCapture(path)

    # Проверяем, открылся ли файл
    if not video_capture.isOpened():
        print("Ошибка при открытии видеофайла")
        exit()

    # Создаем пустой список для хранения кадров
    frames = []

    # Читаем видео по кадрам
    while True:
        # Считываем кадр
        ret, frame = video_capture.read()

        # Проверяем, успешно ли считали кадр
        if not ret:
            break

        # Добавляем кадр в список
        frames.append(frame)

    # Освобождаем объект захвата видео
    video_capture.release()

    analyze_frames = frames[::30]
    print(len(frames))
    print(len(analyze_frames))

    for idx,frame in enumerate(analyze_frames):
        for_image = None
        text = None

        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image.save(f'{idx}.jpg')

        temp_explicit_video_content = detect_explicit_content(f'{idx}.jpg')

        result_for_image = explicit_content_check_from_image(temp_explicit_video_content)


        text = get_text(f'{idx}.jpg')
        # print(text)

        if text['text'] != '' and len(text['text']) > 0:
            text = detect_explicit_comment(text['text'])
            text = explicit_content_check_from_text(text)
        else:
            text = {'is_explicit': 'publish', 'reasons': []}
            # print(text)

        os.remove(f'{idx}.jpg')

        if result_for_image['is_explicit'] == 'ban' or text['is_explicit'] == 'ban':
            # print(f'EXPLICIT CONTENT IN IMAGE: {result_for_image}\nEXPLICIT CONTENT IN TEXT FROM IMAGE: {text}')
            # print(f'BAN reasons: {result_for_image["reasons"]}')
            return result_for_image, text

        elif result_for_image['is_explicit'] == 'same':
            # print(f'EXPLICIT CONTENT IN IMAGE: {result_for_image}\nEXPLICIT CONTENT IN TEXT FROM IMAGE: {text}')
            for_image = result_for_image
            text = text
            
        else:
            # print(f'EXPLICIT CONTENT IN IMAGE: {result_for_image}\nEXPLICIT CONTENT IN TEXT FROM IMAGE: {text}')
            for_image = result_for_image
            text = text
            # print('PUBLISH')

        if text['is_explicit'] == 'same':
            # print(f'EXPLICIT CONTENT IN IMAGE: {result_for_image}\nEXPLICIT CONTENT IN TEXT FROM IMAGE: {text}')
            text = text

        return [for_image, text]

if __name__ == "__main__":
    print(detect_explicit_content_from_video('228.mp4'))