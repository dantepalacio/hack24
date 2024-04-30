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
    answer = json.loads(answer)
    return answer

def transcript_text(audio_file_name):
    audio_file= open(audio_file_name, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    transcription_text = transcription.text
    print(transcription_text)
    return transcription_text



def get_text_from_audio(path):
    import moviepy.editor as mp

    video = mp.VideoFileClip(path)

    audio = video.audio


    audio_path = "audio.wav"  
    audio.write_audiofile(audio_path)

    video.close()


    transcription_text = transcript_text(audio_path)
    return {'text': transcription_text}

