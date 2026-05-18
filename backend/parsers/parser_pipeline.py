import json
from parsers.normalizer import normalize_ad
from storage.save import save_json


def extract_ads_from_html(html: str):
    marker = '"collated_results":['
    start_positions = []

    start = 0
    while True:
        pos = html.find(marker, start)
        if pos == -1:
            break
        start_positions.append(pos)
        start = pos + 1

    all_ads = []

    for block_index, pos in enumerate(start_positions):

        start = pos + len('"collated_results":')

        bracket_count = 0
        end = start
        started = False

        for i in range(start, len(html)):
            char = html[i]

            if char == '[':
                bracket_count += 1
                started = True

            elif char == ']':
                bracket_count -= 1

            if started and bracket_count == 0:
                end = i + 1
                break

        raw_json = html[start:end]

        try:
            ads = json.loads(raw_json)
            all_ads.extend(ads)

        except Exception as e:
            with open(f"debug_block_{block_index + 1}.txt", "w", encoding="utf-8") as f:
                f.write(raw_json)

    return all_ads


def run_parser(file_path="page.html"):
    print("[PARSER] lendo HTML...")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        ads = extract_ads_from_html(html)

        print(f"[PARSER] {len(ads)} ads extraídos")

        normalized_ads = []

        for index, ad in enumerate(ads):

            try:
                normalized = normalize_ad(ad)
                normalized_ads.append(normalized)

                print(
                    f"[NORMALIZED] {index + 1} | "
                    f"{normalized.get('media_type')} | "
                    f"{normalized.get('headline', '')[:60]}"
                )

                if normalized.get("media_type") == "unknown":
                    with open(f"debug_unknown_ad_{index + 1}.json", "w", encoding="utf-8") as f:
                        json.dump(ad, f, ensure_ascii=False, indent=2)

                if normalized.get("media_type") == "dynamic_template":
                    with open(f"debug_dynamic_ad_{index + 1}.json", "w", encoding="utf-8") as f:
                        json.dump(ad, f, ensure_ascii=False, indent=2)

            except Exception as e:
                print(f"[ERRO NORMALIZE {index + 1}] {e}")

        # remove duplicados
        unique = {}
        for ad in normalized_ads:
            ad_id = ad.get("ad_id")
            if ad_id:
                unique[ad_id] = ad

        final_ads = list(unique.values())

        print(f"\n[+] {len(normalized_ads)} anúncios normalizados")
        print(f"[+] {len(final_ads)} anúncios únicos")

        save_json(final_ads, "ads_normalized.json")

        media_stats = {}

        for ad in final_ads:
            media_type = ad.get("media_type", "unknown")
            media_stats[media_type] = media_stats.get(media_type, 0) + 1

        print("\n📊 MEDIA TYPES:")
        for k, v in media_stats.items():
            print(f"{k}: {v}")

        print("\n[🔥 PIPELINE FINALIZADO 🔥]")

        return final_ads

    except Exception as e:
        print(f"[PARSER ERROR] {e}")
        return []


def main():
    return run_parser()