import json

from image_analyzer import extract_text_from_image


with open(
    "data/normalized/ads_normalized.json",
    "r",
    encoding="utf-8"
) as f:

    ads = json.load(f)


for ad in ads:

    image_url = ad.get("image_url")

    if image_url:

        print("\n===================")

        print(ad["headline"])

        print("\n[OCR]\n")

        text = extract_text_from_image(
            image_url
        )

        print(text[:1000])

        break