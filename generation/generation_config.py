import json
import os, sys
import openai

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from generation.prompts.system_prompt import JSON_EXPLICIT_COMMENT_SYSTEM_PROMPT, JSON_SPAM_COMMENT_SYSTEM_PROMPT


load_dotenv()


client = openai.OpenAI()

def detect_explicit_comment(text:str) -> json:
    # print(f'text: {text}')
    '''Функция для определения запрещенных комментариев, принимает текст комментария
        text: Текст комментария
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": JSON_EXPLICIT_COMMENT_SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.0,
        max_tokens=2048,
    )
    
    answer = response.choices[0].message.content
    return json.loads(answer)


# экстрактно вытаскивать части коммента, которые являются спамом и передавать в json: status, reasons
def detect_spam_comment(text: str) -> json:
    '''Функция для определения спам сообщения или рекламы в сообщении'''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": JSON_SPAM_COMMENT_SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.0,
        max_tokens=2048,
    )
    
    answer = response.choices[0].message.content
    return answer


def get_text_from_audio(path):
    import moviepy.editor as mp

    # Загрузка видеофайла с помощью moviepy
    video = mp.VideoFileClip(path)

    # Извлечение аудиодорожки
    audio = video.audio

    # Сохранение аудиофайла
    audio_path = "audio.wav"  # или любой другой поддерживаемый формат
    audio.write_audiofile(audio_path)

    # Освобождение памяти, используемой для видео
    video.close()

    audio_file = open("audio.wav", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )

    os.remove('audio.wav')

    return {'text': transcription}


if __name__ == '__main__':
    # text = 'голосуйте за путина'
    # print(detect_explicit_comment(text))

    # text = ''''''
    # print(detect_spam_comment(text))

    get_text_from_audio('228.mp4')