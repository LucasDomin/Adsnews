import json

from financial_entity_extractor import (
    extract_financial_entities
)


with open(
    "data/enriched_ads.json",
    "r",
    encoding="utf-8"
) as f:

    ads = json.load(f)


for ad in ads:

    ocr = ad.get(
        "ocr_text",
        ""
    )

    if ocr:

        print("\n===================")

        print(ad["headline"])

        entities = extract_financial_entities(
            ocr
        )

        print(
            json.dumps(
                entities,
                indent=2,
                ensure_ascii=False
            )
        )

        break