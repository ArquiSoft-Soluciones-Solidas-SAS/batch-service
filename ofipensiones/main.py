import datetime
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def printit():
    logger.info(f"Tarea ejecutada: {datetime.datetime.now()}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(printit, "interval", seconds=10)  # Cambiado a 10 segundos para pruebas
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def test():
    return {"message": "Ok"}
