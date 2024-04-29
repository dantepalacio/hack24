import os
import base64

def save_image_from_base64(base64_string, filename):
    filename1 = base64_string.split(';')[0]
    print(filename1)
    save_path = f'.\\uploads\\{filename}.jpg'

    try:
        image_data = base64.b64decode(base64_string)
        
        with open(save_path, 'wb') as file:
            file.write(image_data)
        
        return save_path
    
    except Exception as e:
        print(f"Ошибка при сохранении изображения: {e}")
        return None
    
