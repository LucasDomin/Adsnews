import re


def extract_financial_entities(text):

    text = text.lower()

    money = re.findall(
        r"r\$\s?\d+[.,]?\d*",
        text
    )

    percentages = re.findall(
        r"\d+[.,]?\d*\s?%",
        text
    )

    installments = re.findall(
        r"\d{1,3}x",
        text
    )

    years = re.findall(
        r"\d+\s?anos?",
        text
    )

    return {

        "money_values": list(set(money)),

        "percentages": list(set(percentages)),

        "installments": list(set(installments)),

        "years": list(set(years))
    }