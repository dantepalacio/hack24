from google.cloud import vision

def detect_explicit_content(path):
    '''Функция для классификации изображения
        path: Путь к изображению
    '''
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    likelihood_name = (
        "0",
        "0.2",
        "0.4",
        "0.6",
        "0.8",
        "1",
    )


    return {'adult': likelihood_name[safe.adult], 
            'medical': likelihood_name[safe.medical],  
            'violence': likelihood_name[safe.violence], 
            'racy': likelihood_name[safe.racy]}


if __name__ == "__main__":
    print(detect_explicit_content('1.jpg'))
