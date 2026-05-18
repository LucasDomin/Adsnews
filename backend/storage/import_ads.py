import json

def run_import(ads):
    print("[STORAGE] salvando ads no banco/file...")

    with open("ads_final.json", "w", encoding="utf-8") as f:
        json.dump(ads, f, ensure_ascii=False, indent=2)

    print(f"[STORAGE] {len(ads)} ads salvos")
    return len(ads)