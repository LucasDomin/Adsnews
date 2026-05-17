import json
import os


def save_json(data, filename):

    os.makedirs("data/normalized", exist_ok=True)

    path = f"data/normalized/{filename}"

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"[+] Salvo: {path}")