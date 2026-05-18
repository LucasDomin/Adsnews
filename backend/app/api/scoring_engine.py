def score_ad(ad):
    score = 0

    headline = (ad.get("headline") or "").lower()
    body = (ad.get("body") or "").lower()
    cta = (ad.get("cta") or "").lower()

    # 🔥 gatilhos de conversão
    hooks = ["grátis", "simule", "rápido", "pix", "crédito", "aprovado"]
    urgency = ["hoje", "agora", "limitado", "últimas vagas"]
    money = ["r$", "1000", "5000", "10000"]

    for h in hooks:
        if h in headline or h in body:
            score += 10

    for u in urgency:
        if u in headline:
            score += 15

    for m in money:
        if m in body:
            score += 8

    if "saiba mais" in cta.lower():
        score += 5

    return min(score, 100)