import uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from batch.report_generator import generate_reports

app = FastAPI()

# Configurar APScheduler
scheduler = BackgroundScheduler()

# Ejecutar la tarea cada minuto
scheduler.add_job(generate_reports, "cron", minute="*")

# Iniciar el scheduler
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
def read_root():
    return {"message": "API activa y cronjob configurado."}