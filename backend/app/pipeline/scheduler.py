import time
from app.pipeline.runner import run_pipeline


def start_scheduler():
    while True:
        print("⏱ Running pipeline...")
        run_pipeline()

        time.sleep(60 * 60 * 2)  # 2 horas