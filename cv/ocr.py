from google.cloud import vision


def get_text(path):

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    if len(texts) > 0:
        answer = texts[0].description

    else:
        return ''

    if texts != []:
        answer = texts[0].description
    else:
        answer = 0


    if response.error.message:
        raise Exception(
            "{}\nЧТО-ТО С OCR "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return {'text': answer}

