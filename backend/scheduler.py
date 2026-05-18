import schedule, time, logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [SCHEDULER] %(message)s")
log = logging.getLogger(__name__)

def run_pipeline():
    log.info("Iniciando pipeline...")
    try:
        from app.pipeline.runner import run_pipeline as _run
        _run()
        log.info("Pipeline concluido.")
    except Exception as e:
        log.error(f"Erro: {e}")

schedule.every().day.at("12:00").do(run_pipeline)
schedule.every().day.at("23:00").do(run_pipeline)
log.info("Scheduler ativo. Rodara as 12:00 e 23:00.")

while True:
    schedule.run_pending()
    time.sleep(30)
