import json

from image_analyzer import extract_text_from_image
from creative_analyzer import analyze_creative_text


with open(
    "data/normalized/ads_normalized.json",
    "r",
    encoding="utf-8"
) as f:

    ads = json.load(f)


for ad in ads:

    image_url = ad.get("image_url")

    if image_url:

        print("\n======================")

        print("[HEADLINE]")
        print(ad["headline"])

        print("\n[OCR]")

        text = extract_text_from_image(
            image_url
        )

        print(text[:1000])

        print("\n[ANALYSIS]")

        analysis = analyze_creative_text(text)

        print(
            json.dumps(
                analysis,
                indent=2,
                ensure_ascii=False
            )
        )

        break