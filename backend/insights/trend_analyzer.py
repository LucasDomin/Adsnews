import json
import re

from collections import Counter


INPUT_FILE = "data/enriched_ads.json"


STOPWORDS = {

    "de",
    "da",
    "do",
    "e",
    "o",
    "a",
    "para",
    "com",
    "sem",
    "em",
    "um",
    "uma",
    "via",
    "ao",
    "os",
    "as",
    "na",
    "no"
}


def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        " ",
        text
    )

    return text


def tokenize(text):

    text = clean_text(text)

    words = text.split()

    words = [
        w for w in words
        if len(w) > 2
        and w not in STOPWORDS
    ]

    return words


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    ads = json.load(f)


word_counter = Counter()

headline_counter = Counter()

cta_counter = Counter()

media_counter = Counter()


for ad in ads:

    headline = ad.get(
        "headline",
        ""
    )

    ocr_text = ad.get(
        "ocr_text",
        ""
    )

    cta = ad.get(
        "cta",
        ""
    )

    media_type = ad.get(
        "media_type",
        "unknown"
    )

    full_text = f"{headline} {ocr_text}"

    tokens = tokenize(full_text)

    word_counter.update(tokens)

    headline_counter.update(
        [headline]
    )

    cta_counter.update(
        [cta]
    )

    media_counter.update(
        [media_type]
    )


print("\n========================")
print("TOP WORDS")
print("========================\n")

for word, count in word_counter.most_common(30):

    print(f"{word}: {count}")


print("\n========================")
print("TOP HEADLINES")
print("========================\n")

for headline, count in headline_counter.most_common(10):

    print(f"{count}x | {headline}")


print("\n========================")
print("TOP CTAS")
print("========================\n")

for cta, count in cta_counter.most_common(10):

    print(f"{count}x | {cta}")


print("\n========================")
print("MEDIA TYPES")
print("========================\n")

for media, count in media_counter.most_common():

    print(f"{media}: {count}")


print("\n[🔥 TREND ANALYSIS FINALIZADA 🔥]")