import os

from flask_mail import Mail, Message

from dotenv import load_dotenv

load_dotenv()

HOST_EMAIL = os.environ.get('HOST_EMAIL')
HOST_EMAIL_PAS = os.environ.get('HOST_EMAIL_PAS')

RED = '#f40b0b'
GREEN = '#05a573'
ORANGE = '#d08700'

def configure_mail(app):
    app.config['MAIL_SERVER']="smtp.gmail.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = HOST_EMAIL
    app.config['MAIL_PASSWORD'] = HOST_EMAIL_PAS
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    mail = Mail(app)
    return mail

API_PATH = "http://217.151.230.141:5000"
def send_mail(mail, temp_status:str, body:dict, text:str=None, image_path:str=None, video_path:str=None):
    id = body["id"]
    if text is not None:
        if temp_status == 'ban':
            thesis = 'Мы заблокировали запрещенный контент'
            body_message = f'Публикация #{id} была заблокирована. \n\n Причины блокировки: {body["reasons"]}\n\n Содержание публикации:\n{text}'
        elif temp_status == 'same':
            thesis = 'Опубликован сомнительный контент'
            body_message = f'Публикация #{id} была помечена, как сомнительный контент. \n\n Причины блокировки: {body["reasons"]}\n\n Содержание публикации:\n{text}'
        mail_message = Message(
                thesis, 
                sender =   HOST_EMAIL, 
                recipients = ['anuar.beisenbaev2003@gmail.com'])
    
    else:
        if temp_status == 'ban':
            thesis = 'Мы заблокировали запрещенный контент'
            body_message = f'Публикация #{id} была заблокирована. \n\n Причины блокировки: {body["reasons"]}\n\n Содержание публикации:\n'
        elif temp_status == 'same':
            thesis = 'Опубликован сомнительный контент'
            body_message = f'Публикация #{id} была помечена, как сомнительный контент.\n\nПричины блокировки: {body["reasons"]}\n\n Содержание публикации:\n'
        mail_message = Message(
                thesis, 
                sender =   HOST_EMAIL, 
                recipients = ['anuar.beisenbaev2003@gmail.com'])
        
    buttonStyle = """color: white;
display: inline-block;
border-radius: 8px;
padding: 8px;
text-decoration: none;"""
    
    mail_message.body = body_message
    mail_message.html = body_message.replace("\n\n", "<br><br>") + f"""
    <div style="margin-top: 20px">
        <a style='{buttonStyle}background-color: {GREEN};' href='{API_PATH}/rate?id={id}&action=like'>Правильно</a>
        <a style='{buttonStyle}background-color: {RED};' href='{API_PATH}/rate?id={id}&action=dislike'>Неправильно</a>
    </div>
    """
    

    if image_path is not None:
        with open(image_path, 'rb') as f:
            image = f.read()
        mail_message.attach(filename='image.jpg', content_type='image/jpg', data=image)

    if video_path is not None:
        with open(video_path, 'rb') as f:
            video = f.read()
        mail_message.attach(filename='video.mp4', content_type='video/mp4', data=video)
        



    mail.send(mail_message)
    print('Отправлено почта')



def send_appelation_mail(mail, id:int, user_message:str, post_data:dict):
    temp_status = post_data['status'] 
    post_text = post_data['comment']
    post_image = post_data['image']
    post_video = post_data['video']
    post_reasons = post_data['reasons']

    if post_text is not None:
        if temp_status == 'ban':
            thesis = f'Подана аппеляция на заблокированную публикацию #{id}'
            body_message = f'Публикация #{id} была заблокирована.\n\n Сообщение от пользователя:\n{user_message} \n\n Причины блокировки: {post_reasons}\n\n Содержание публикации:\n{post_text}'
        elif temp_status == 'same':
            thesis = f'Подана аппеляция на сомнительную публикацию #{id}'
            body_message = f'Публикация #{id} была помечена, как сомнительный контент.\n\n Сообщение от пользователя:\n{user_message} \n\n Причины блокировки: {post_reasons}\n\n Содержание публикации:\n{post_text}'
        elif temp_status == 'publish':
            thesis = f'Подана аппеляция на опубликованную публикацию #{id}'
            body_message = f'Публикация #{id} была помечена, как опубликованный контент.\n\n Сообщение от пользователя:\n{user_message} \n\n Содержание публикации:\n{post_text}'
        
        mail_message = Message(
                thesis,
                sender = HOST_EMAIL, 
                recipients = ['anuar.beisenbaev2003@gmail.com'])

    else:
        if temp_status == 'ban':
            thesis = f'Подана аппеляция на заблокированную публикацию #{id}'
            body_message = f'Публикация #{id} была заблокирована.\n\n Сообщение от пользователя:\n{user_message} \n\n Причины блокировки: {post_reasons}\n\n Содержание публикации:\n'
        elif temp_status == 'same':
            thesis = f'Подана аппеляция на сомнительную публикацию #{id}'
            body_message = f'Публикация #{id} была помечена, как сомнительный контент.\n\n Сообщение от пользователя:\n{user_message} \n\n Причины блокировки: {post_reasons}\n\n Содержание публикации:\n'
        elif temp_status == 'publish':
            thesis = f'Подана аппеляция на опубликованную публикацию #{id}'
            body_message = f'Публикация #{id} была помечена, как опубликованный контент.\n\n Сообщение от пользователя:\n{user_message} \n\n Содержание публикации:\n'
        
        mail_message = Message(
                thesis,
                sender = HOST_EMAIL, 
                recipients = ['anuar.beisenbaev2003@gmail.com'])

    buttonStyle = """color: white;
display: inline-block;
border-radius: 8px;
padding: 8px;
text-decoration: none;"""
    
    mail_message.body = body_message

    if temp_status == 'ban':
        mail_message.html = body_message.replace("\n\n", "<br><br>") + f"""
        <div style="margin-top: 20px">
            <a style='{buttonStyle}background-color: {GREEN};' href='{API_PATH}/change_post_status?id={id}&new_status=publish'>Опубликовать</a>
            <a style='{buttonStyle}background-color: {ORANGE};' href='{API_PATH}/change_post_status?id={id}&new_status=same'>Сомнительный контент</a>
        </div>
        """
    elif temp_status == 'same':
        mail_message.html = body_message.replace("\n\n", "<br><br>") + f"""
        <div style="margin-top: 20px">
            <a style='{buttonStyle}background-color: {GREEN};' href='{API_PATH}/change_post_status?id={id}&new_status=publish'>Опубликовать</a>
            <a style='{buttonStyle}background-color: {RED};' href='{API_PATH}/change_post_status?id={id}&new_status=ban'>Заблокировать</a>
        </div>
        """
    elif temp_status == 'publish':
        mail_message.html = body_message.replace("\n\n", "<br><br>") + f"""
        <div style="margin-top: 20px">
            <a style='{buttonStyle}background-color: {ORANGE};' href='{API_PATH}/change_post_status?id={id}&new_status=same'>Сомнительный контент</a>
            <a style='{buttonStyle}background-color: {RED};' href='{API_PATH}/change_post_status?id={id}&new_status=ban'>Заблокировать</a>
        </div>
        """

    if post_image is not None:
        with open(post_image, 'rb') as f:
            image = f.read()
        mail_message.attach(filename='image.jpg', content_type='image/jpg', data=image)

    if post_video is not None:
        with open(post_video, 'rb') as f:
            video = f.read()
        mail_message.attach(filename='video.mp4', content_type='video/mp4', data=video)
        



    mail.send(mail_message)
    print('Отправлена аппеляция')