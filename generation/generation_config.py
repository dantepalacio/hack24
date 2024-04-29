import json
import os
import openai

from dotenv import load_dotenv


from generation.prompts.system_prompt import JSON_EXPLICIT_COMMENT_SYSTEM_PROMPT


load_dotenv()


client = openai.OpenAI()

def detect_explicit_comment(text:str) -> str:
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


# comment = 'SODJiuAAIsФЫВоывыва ывафы счч'

# print('--------------------------')
# print(comment)

# print(detect_explicit_comment(comment))