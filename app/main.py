import time
from fastapi import FastAPI, Request
from models import Invoice
from db import create_all_tables

import zoneinfo

from datetime import datetime
from .routers import customers, transactions, plans


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    psorcess_time = time.time() - start_time
    print(f"Request: {request.url} completed in {psorcess_time:.4f} seconds")
    return response


@app.get("/")
async def root():
    return {"message": "Hello, David!"}


@app.get("/time/{iso_code}")
async def get_time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz), "timezone": timezone_str}


@app.post("/invoices")
async def create_invoices(invoice_data: Invoice):
    return invoice_data
