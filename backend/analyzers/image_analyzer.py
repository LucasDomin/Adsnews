import os
import requests
import pytesseract

from PIL import Image
from io import BytesIO


# caminho do tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image_url):

    try:

        response = requests.get(
            image_url,
            timeout=20
        )

        image = Image.open(
            BytesIO(response.content)
        )

        text = pytesseract.image_to_string(
            image,
            lang="por+spa+eng"
        )

        return text.strip()

    except Exception as e:

        print(f"[OCR ERROR] {e}")

        return ""