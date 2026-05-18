from app.pipeline.scraper import run_scraper
from app.pipeline.parser import run_parser
from app.pipeline.enrich import run_enrich
from app.pipeline.storage import save_ads


def run_pipeline():
    print("[PIPELINE] starting...")

    html = run_scraper()
    ads = run_parser(html)
    ads = run_enrich(ads)
    save_ads(ads)

    print("[PIPELINE] done")