import cv2
import os
import sys
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generation.generation_config import detect_explicit_comment, detect_spam_comment
from cv.ocr import get_text
from cv.explicit_content_detection import detect_explicit_content
from utils.utils import explicit_content_check_from_text, explicit_content_check_from_image


# Открываем видеофайл
video_capture = cv2.VideoCapture('10.mp4')

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
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image.save(f'{idx}.jpg')

    temp_explicit_video_content = detect_explicit_content(f'{idx}.jpg')

    result = explicit_content_check_from_image(temp_explicit_video_content)
    os.remove(f'{idx}.jpg')

    if result['is_explicit'] == 'ban':
        print(f'BAN reasons: {result["reasons"]}')
        break

    elif result['is_explicit'] == 'same':
        print(f'SAME reasons: {result["reasons"]}')
        
    else:
        print('PUBLISH')
#################################



