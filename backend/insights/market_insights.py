import json
import re

from collections import Counter


INPUT_FILE = "data/enriched_ads.json"


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    ads = json.load(f)


total_ads = len(ads)

pix_ads = 0

quiz_ads = 0

money_counter = Counter()

cta_counter = Counter()

media_counter = Counter()

headline_words = Counter()


for ad in ads:

    headline = (
        ad.get("headline", "")
        .lower()
    )

    ocr = (
        ad.get("ocr_text", "")
        .lower()
    )

    media = ad.get(
        "media_type",
        "unknown"
    )

    cta = ad.get(
        "cta",
        "unknown"
    )

    full_text = f"{headline} {ocr}"

    # PIX
    if "pix" in full_text:

        pix_ads += 1

    # QUIZ
    if "quiz" in headline:

        quiz_ads += 1

    # MONEY
    money_matches = re.findall(
        r"r\$\s?\d+[.,]?\d*",
        full_text
    )

    money_counter.update(
        money_matches
    )

    # CTA
    cta_counter.update(
        [cta]
    )

    # MEDIA
    media_counter.update(
        [media]
    )

    # HEADLINE WORDS
    words = headline.split()

    headline_words.update(words)


print("\n========================")
print("MARKET INSIGHTS")
print("========================\n")


print(
    f"Total Ads: {total_ads}"
)

print(
    f"PIX Presence: {(pix_ads/total_ads)*100:.1f}%"
)

print(
    f"Quiz Presence: {(quiz_ads/total_ads)*100:.1f}%"
)


print("\nTOP MONEY VALUES\n")

for value, count in money_counter.most_common(10):

    print(f"{value}: {count}")


print("\nTOP CTAS\n")

for cta, count in cta_counter.most_common():

    print(f"{cta}: {count}")


print("\nMEDIA DISTRIBUTION\n")

for media, count in media_counter.most_common():

    print(f"{media}: {count}")


print("\nTOP HEADLINE WORDS\n")

for word, count in headline_words.most_common(20):

    print(f"{word}: {count}")


print("\n[🔥 MARKET INSIGHTS FINALIZADO 🔥]")