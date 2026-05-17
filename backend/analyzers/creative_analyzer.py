import re


URGENT_WORDS = [
    "agora",
    "hoje",
    "urgente",
    "rápido",
    "instantâneo",
    "liberado",
    "imediato",
    "na hora"
]

TRUST_WORDS = [
    "oficial",
    "taxa",
    "aprovado",
    "seguro",
    "garantia",
    "banco"
]

SPEED_WORDS = [
    "pix",
    "rápido",
    "instantâneo",
    "5 minutos",
    "na hora"
]

ACCESS_WORDS = [
    "sem burocracia",
    "sem consulta",
    "fácil",
    "online",
    "sem compromisso"
]


def count_matches(text, words):

    text = text.lower()

    score = 0

    matches = []

    for word in words:

        if word.lower() in text:

            score += 1

            matches.append(word)

    return score, matches


def analyze_creative_text(text):

    urgency_score, urgency_matches = count_matches(
        text,
        URGENT_WORDS
    )

    trust_score, trust_matches = count_matches(
        text,
        TRUST_WORDS
    )

    speed_score, speed_matches = count_matches(
        text,
        SPEED_WORDS
    )

    access_score, access_matches = count_matches(
        text,
        ACCESS_WORDS
    )

    return {

        "urgency_score": urgency_score,

        "trust_score": trust_score,

        "speed_score": speed_score,

        "accessibility_score": access_score,

        "urgency_words": urgency_matches,

        "trust_words": trust_matches,

        "speed_words": speed_matches,

        "access_words": access_matches
    }