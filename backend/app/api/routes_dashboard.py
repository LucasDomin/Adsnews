from fastapi import APIRouter, BackgroundTasks
from app.db.db import SessionLocal
from app.db.models import Ad

router = APIRouter()


@router.get("/summary")
def summary():
    db = SessionLocal()
    ads = db.query(Ad).all()
    total = len(ads)

    media = {}
    pages = {}
    countries = {}

    for a in ads:
        media[a.media_type or "outro"] = media.get(a.media_type or "outro", 0) + 1
        pages[a.page_name or "—"] = pages.get(a.page_name or "—", 0) + 1
        if a.country:
            countries[a.country] = countries.get(a.country, 0) + 1

    top_pages = sorted(pages.items(), key=lambda x: x[1], reverse=True)[:10]

    db.close()
    return {
        "total_ads": total,
        "media_distribution": media,
        "top_pages": top_pages,
        "countries": countries,
    }


_pipeline_running = False


@router.post("/refresh")
def refresh(background_tasks: BackgroundTasks):
    global _pipeline_running
    if _pipeline_running:
        return {"status": "already_running", "message": "Pipeline já está em execução"}

    def run():
        global _pipeline_running
        _pipeline_running = True
        try:
            from app.pipeline.runner import run_pipeline
            run_pipeline()
        except Exception as e:
            print(f"[REFRESH] Erro: {e}")
        finally:
            _pipeline_running = False

    background_tasks.add_task(run)
    return {"status": "started", "message": "Pipeline iniciado em background"}


@router.get("/refresh/status")
def refresh_status():
    return {"running": _pipeline_running}