import json

from normalizer import normalize_ad
from storage import save_json


print("[*] Abrindo page.html...")

with open(
    "page.html",
    "r",
    encoding="utf-8"
) as f:

    html = f.read()


marker = '"collated_results":['

start_positions = []

start = 0

while True:

    pos = html.find(marker, start)

    if pos == -1:
        break

    start_positions.append(pos)

    start = pos + 1


print(f"[+] {len(start_positions)} blocos collated_results encontrados")


all_ads = []


for block_index, pos in enumerate(start_positions):

    print(f"\n[*] Processando bloco {block_index + 1}")

    # início real do array
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

        print(f"[+] {len(ads)} ads encontrados no bloco")

        all_ads.extend(ads)

    except Exception as e:

        print(f"[X] Erro bloco {block_index + 1}: {e}")

        with open(
            f"debug_block_{block_index + 1}.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(raw_json)


print(f"\n[+] TOTAL ADS EXTRAÍDOS: {len(all_ads)}")


normalized_ads = []


for index, ad in enumerate(all_ads):

    try:

        normalized = normalize_ad(ad)

        normalized_ads.append(normalized)

        print(
            f"[NORMALIZED] {index + 1} | "
            f"{normalized.get('media_type')} | "
            f"{normalized.get('headline', '')[:60]}"
        )

        # salva ads problemáticos
        if normalized["media_type"] == "unknown":

            with open(
                f"debug_unknown_ad_{index + 1}.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    ad,
                    f,
                    ensure_ascii=False,
                    indent=2
                )

        # salva templates dinâmicos
        if normalized["media_type"] == "dynamic_template":

            with open(
                f"debug_dynamic_ad_{index + 1}.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    ad,
                    f,
                    ensure_ascii=False,
                    indent=2
                )

    except Exception as e:

        print(f"[ERRO NORMALIZE {index + 1}] {e}")

        with open(
            f"normalize_error_{index + 1}.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                ad,
                f,
                ensure_ascii=False,
                indent=2
            )


print(
    f"\n[+] {len(normalized_ads)} anúncios normalizados"
)


# remove duplicados por ad_id
unique_ads = {}

for ad in normalized_ads:

    ad_id = ad.get("ad_id")

    if ad_id:
        unique_ads[ad_id] = ad


final_ads = list(unique_ads.values())

print(f"[+] {len(final_ads)} anúncios únicos")


save_json(
    final_ads,
    "ads_normalized.json"
)


# estatísticas rápidas
media_stats = {}

for ad in final_ads:

    media_type = ad.get("media_type", "unknown")

    media_stats[media_type] = (
        media_stats.get(media_type, 0) + 1
    )


print("\n📊 MEDIA TYPES:")

for media_type, count in media_stats.items():

    print(f"{media_type}: {count}")


print("\n[🔥 PIPELINE FINALIZADO 🔥]")