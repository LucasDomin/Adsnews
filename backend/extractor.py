import re
import json


with open("page.html", "r", encoding="utf-8") as f:
    html = f.read()


print("[*] Procurando collated_results...")

match = re.search(
    r'"collated_results":(.*?),"page_info"',
    html
)

if not match:
    print("[X] collated_results não encontrado")
    exit()


raw = match.group(1)

print("[+] Encontrado")

with open(
    "raw_collated_results.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(raw)

print("[+] raw_collated_results.txt salvo")