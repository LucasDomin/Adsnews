from app.services.scraper_service import run_scraper
from app.services.parser_service import run_parser
from app.services.enrichment_service import run_enrichment
from app.services.storage_service import run_storage


def run_pipeline():
    print("🚀 PIPELINE START")

    html = run_scraper()
    ads = run_parser(html)
    enriched = run_enrichment(ads)
    run_storage(enriched)

    print("🔥 PIPELINE DONE")
    return True