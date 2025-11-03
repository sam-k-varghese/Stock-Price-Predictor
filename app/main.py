from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import stock_routes
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI Application starting up...")
    yield
    logger.info("FastAPI Application shutting down...")

app = FastAPI(
    title="Stock Price Predictor API",
    description="Predicts future stock prices using LSTM models trained on real stock data.",
    version="1.0.0"
)

# Include router
app.include_router(stock_routes.stock_router)


@app.get("/")
def root():
    return {"message": "Welcome to Stock Price Predictor API"}
