
"""Detects text in the file."""
from google.cloud import vision

client = vision.ImageAnnotatorClient()

with open('1.jpg', "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
print("Texts:")

for text in texts:
    print(f'\n"{text.description}"')

    vertices = [
        f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
    ]

    print("bounds: {}".format(",".join(vertices)))

if response.error.message:
    raise Exception(
        "{}\nFor more info on error messages, check: "
        "https://cloud.google.com/apis/design/errors".format(response.error.message)
    )
