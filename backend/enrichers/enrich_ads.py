import json


def enrich_ads(ads):
    print("[ENRICHER] enriquecendo ads...")

    enriched = []

    for ad in ads:
        try:
            # exemplo de enriquecimento simples (você vai evoluir isso depois)
            ad["has_pix"] = "pix" in str(ad.get("ocr_text", "")).lower()
            ad["has_quiz"] = "quiz" in str(ad.get("headline", "")).lower()
            ad["score_basic"] = (
                int(ad["has_pix"]) + int(ad["has_quiz"])
            )

            enriched.append(ad)

        except Exception as e:
            print(f"[ENRICH ERROR] {e}")

    return enriched


def run_enrichment(ads=None):
    print("[ENRICHER] run_enrichment executando...")

    if ads is None:
        try:
            with open("ads_normalized.json", "r", encoding="utf-8") as f:
                ads = json.load(f)
        except Exception as e:
            print(f"[ENRICHER ERROR] não conseguiu ler ads_normalized.json: {e}")
            return []

    enriched = enrich_ads(ads)

    with open("ads_enriched.json", "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)

    print(f"[ENRICHER] {len(enriched)} ads enriquecidos")

    return enriched