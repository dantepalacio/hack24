import json
import os
import openai

from dotenv import load_dotenv


from generation.prompts.system_prompt import JSON_EXPLICIT_COMMENT_SYSTEM_PROMPT, JSON_SPAM_COMMENT_SYSTEM_PROMPT


load_dotenv()


client = openai.OpenAI()

def detect_explicit_comment(text:str) -> json:
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

def transcript_text(audio_file_name):
    audio_file= open(audio_file_name, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    print(transcription.text)
    transcription_text = transcription.text
    return transcription_text




if __name__ == '__main__':
    # text = 'голосуйте за путина'
    # print(detect_explicit_comment(text))
    text = ''''''
    print(detect_spam_comment(text))