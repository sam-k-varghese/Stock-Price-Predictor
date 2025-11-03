from fastapi import APIRouter, HTTPException
from app.models.lstm_model import StockPricePredictor
from app.utils.logger import logger

stock_router = APIRouter(prefix="/stock", tags=["Stock Price Prediction"])


@stock_router.post("/train/{symbol}")
def train_stock_model(symbol: str):
    """
    Train LSTM model for a specific stock symbol.
    """
    try:
        logger.info(f"Training initiated for {symbol.upper()}")
        predictor = StockPricePredictor(symbol)
        predictor.train(epochs=5)
        return {
            "message": f"Model trained successfully for {symbol.upper()}",
            "payload": None,
            "status": 200
        }
    except Exception as e:
        logger.exception(f"Training failed for {symbol.upper()}: {e}")
        raise HTTPException(status_code=500, detail={
            "message": "Model training failed",
            "payload": str(e),
            "status": 500
        })


@stock_router.get("/predict/{symbol}")
def predict_next_price(symbol: str):
    """
    Predict the next day's closing price for a stock.
    """
    try:
        logger.info(f"Prediction initiated for {symbol.upper()}")
        predictor = StockPricePredictor(symbol)
        predicted_price = predictor.predict_next()
        return {
            "message": "Prediction successful",
            "payload": {
                "symbol": symbol.upper(),
                "predicted_price": round(predicted_price, 2)
            },
            "status": 200
        }
    except FileNotFoundError:
        logger.exception(f"Prediction failed for {symbol.upper()}: as model training data file not found")
        raise HTTPException(status_code=404, detail={
            "message": f"Model not found for {symbol}. Train it first.",
            "payload": None,
            "status": 404
        })
    except Exception as e:
        logger.exception(f"Prediction failed for {symbol.upper()}: {e}")
        raise HTTPException(status_code=500, detail={
            "message": "Prediction failed",
            "payload": str(e),
            "status": 500
        })
