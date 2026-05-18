import schedule
import time
from datetime import datetime

from collectors.scraper import run_scraper
from parsers.parser_pipeline import run_parser
from enrichers.enrich_ads import run_enrichment
from storage import save_json


def run_pipeline():
    print("\n==========================")
    print("🚀 PIPELINE:", datetime.now())
    print("==========================\n")

    try:
        run_scraper()
        run_parser()
        run_enrichment()
        run_import()

        print("\n🔥 PIPELINE FINALIZADO COM SUCESSO\n")

    except Exception as e:
        print("❌ ERRO NA PIPELINE:", e)


schedule.every(2).hours.do(run_pipeline)

run_pipeline()

print("⏱ Scheduler ativo (2h)")

while True:
    schedule.run_pending()
    time.sleep(30)