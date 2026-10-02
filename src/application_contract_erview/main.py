from fastapi import FastAPI
from routes import base, risk_route

app = FastAPI()


app.include_router(base.base_router)
app.include_router(risk_route.router)