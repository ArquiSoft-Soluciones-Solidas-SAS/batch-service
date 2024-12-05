import datetime
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

def printit():
    print(datetime.datetime.now())


@asynccontextmanager
async def lifespan(app:FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(printit,"interval",minutes = 1)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def test():
    return "Ok"