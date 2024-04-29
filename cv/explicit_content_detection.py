from google.cloud import vision

def detect_explicit_content(path):
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = (
        "0",
        "0.2",
        "0.4",
        "0.6",
        "0.8",
        "1",
    )


    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return {'adult': likelihood_name[safe.adult], 'medical': likelihood_name[safe.medical], 'spoofed': likelihood_name[safe.spoof], 'violence': likelihood_name[safe.violence], 'racy': likelihood_name[safe.racy]}


if __name__ == "__main__":
    print(detect_explicit_content('1.jpg'))