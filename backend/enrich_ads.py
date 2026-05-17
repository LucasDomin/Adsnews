import json
import time

from image_analyzer import extract_text_from_image
from creative_analyzer import analyze_creative_text


INPUT_FILE = "data/normalized/ads_normalized.json"

OUTPUT_FILE = "data/enriched_ads.json"


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    ads = json.load(f)


enriched_ads = []


for index, ad in enumerate(ads):

    print(f"\n[{index+1}/{len(ads)}]")

    image_url = ad.get("image_url")

    ocr_text = ""

    analysis = {}

    if image_url:

        print("[*] Rodando OCR...")

        ocr_text = extract_text_from_image(
            image_url
        )

        print("[*] Analisando copy...")

        analysis = analyze_creative_text(
            ocr_text
        )

    enriched_ad = {

        **ad,

        "ocr_text": ocr_text,

        "creative_analysis": analysis
    }

    enriched_ads.append(
        enriched_ad
    )

    print(
        f"[+] {ad.get('headline')}"
    )

    time.sleep(1)


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        enriched_ads,
        f,
        ensure_ascii=False,
        indent=2
    )


print("\n[🔥 ENRICHMENT FINALIZADO 🔥]")
print(f"[+] Salvo em: {OUTPUT_FILE}")