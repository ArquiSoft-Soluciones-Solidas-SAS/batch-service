import uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from batch.report_generator import generate_reports
from contextlib import asynccontextmanager

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(generate_reports, "cron", minute="*")
scheduler.start()

# Usar un manejador de ciclo de vida en lugar de @app.on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)

# Configurar FastAPI con el ciclo de vida
app = FastAPI(lifespan=lifespan)

# Ruta para comprobar el estado del servicio
@app.get("/")
async def read_root():
    return {"message": "API activa y cronjob configurado."}

# Punto de entrada principal
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
