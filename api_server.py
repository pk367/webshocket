from fastapi import FastAPI, WebSocket, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import logging
import json
import asyncio
from datetime import datetime
from tvdatafeed import TvDatafeed, Interval

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TradingView Data API",
    description="Real-time market data API powered by TradingView",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TvDatafeed
tv = TvDatafeed(username='', password='')
tv.token = 'eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjo1NDgwNTUyMSwiZXhwIjoxNzI3ODIxNzk0LCJpYXQiOjE3Mjc4MDczOTQsInBsYW4iOiJwcm9fcHJlbWl1bSIsImV4dF9ob3VycyI6MSwicGVybSI6IiIsInN0dWR5X3Blcm0iOiJQVUI7NmEyZWI4MDUxMjc5NDkxOTk0MDk2MWQ4ZjUxMTYwMzUsUFVCOzQ2NjMzNTU3ZDE5YjQwYjE5MjQzMmVmNmYyOTA4ZDE0LFBVQjtjMDYxOTIzODdlMmU0ZDJkYTdjZDEzNmVlMjgxOTVlNixQVUI7ZGJmZGMzZDNmNDA3NDIyZjkzYjE2NDAyYTFmOGMwMGQsUFVCO2YzM2IxNTAzZjIyMDQxYzViZTVmZTkxMzMxY2NjNDE4LFBVQjtjZTNhZDY5MzI5MjQ0NTQ5OTgwMjE3NmM2YzRiNzkxMSxQVUI7NmM5MWEyOTRiM2ViNGQ5MTg3MWZlNzFjMzYyY2VkNTEsUFVCOzdjNGIwOWIyYjRhNjQ5YTNhNjU0ZjY2ZWZmOTE1NTcwLHR2LWNoYXJ0cGF0dGVybnMsUFVCO2YwOTdhNzhmODM0MjRiNmY4MWMwODQ3ZTVjOTg4Y2M4LFBVQjtlYTA4M2Q5MDUzNjQ0NzZkOWRmN2FjODBhMjVkMjg1YixQVUI7NmZiZWE5YmRmMGNmNGQ2YWJiNmFjOWE4NmI4OGM5MjQsUFVCO2UxZjAwZjZlNWY2NjRkNGJiMzM2ZWE5NGVhYzlmY2FlLFBVQjszMGNiYzY5MWJiOTM0YTI1OTkyOGU3NzYxYzg5YjBmNCxQVUI7YTQ4MWI5YzMzMmEwNDZmNThiODhmYmVhYWY4YWFhOTgsUFVCOzNlODU4YWU2MTNiMjQwMGU4MzAyOTE5ZGQ0MWQzOTU4LFBVQjtjNzNlOWMzZDA0YTU0MWQwOTVkMGQ3MzVhYTdiZjU5MSxQVUI7NWEyMGMzZTY2MTdjNDJjNWFjMmRmYzZlZmYxMzlkZjIsUFVCOzAzNzA2NmMyY2VjZTRjYTk4MzI3ODA0MTIzZWFiMjcyLHR2LXByb3N0dWRpZXMsdHYtY2hhcnRfcGF0dGVybnMsUFVCOzJkZDYyMDBkNmJmNjQ1OTI5MGFiNzJiZDZiODQyMzkxLFBVQjtiM2Y3YzBiY2I0NWQ0MzJjYThkNDc4NDczMGE5YzIyMyx0di12b2x1bWVieXByaWNlLFBVQjszOTVkNjAyYzVlZTI0ODMwYTc1MjZjYWFmN2MyNjI3YyIsIm1heF9zdHVkaWVzIjoyNSwibWF4X2Z1bmRhbWVudGFscyI6MTAsIm1heF9jaGFydHMiOjgsIm1heF9hY3RpdmVfYWxlcnRzIjo0MDAsIm1heF9zdHVkeV9vbl9zdHVkeSI6MjQsImZpZWxkc19wZXJtaXNzaW9ucyI6WyJyZWZib25kcyJdLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6NDAwLCJtYXhfYWN0aXZlX2NvbXBsZXhfYWxlcnRzIjo0MDAsIm1heF9jb25uZWN0aW9ucyI6NTB9.cAWGPm30ohtUEBNo1ryPxzxSgkzEHR_zjk8jS3cDI-ERQl2iv-Cs6x-ozIA4HQm9pwF607wk-XMl7AGWdBpRxCaTstq8COYg1pzCbPYYQDW3MIXLG_sL96PZDATfb-EXN3O4ZIPSffAv38QKeBHvnRuU7KbqS_GKjRp3pSXrtAc'

# Mapping for intervals
INTERVAL_MAP = {
    "1m": Interval.in_1_minute,
    "3m": Interval.in_3_minute,
    "5m": Interval.in_5_minute,
    "15m": Interval.in_15_minute,
    "30m": Interval.in_30_minute,
    "45m": Interval.in_45_minute,
    "1h": Interval.in_1_hour,
    "2h": Interval.in_2_hour,
    "3h": Interval.in_3_hour,
    "4h": Interval.in_4_hour,
    "1d": Interval.in_daily,
    "1w": Interval.in_weekly,
    "1M": Interval.in_monthly
}

# Request models
class MarketDataRequest(BaseModel):
    symbol: str
    exchange: str
    interval: str
    n_bars: Optional[int] = 100
    fut_contract: Optional[int] = None

class SymbolsRequest(BaseModel):
    symbols: List[MarketDataRequest]

# Cache for storing recent data
data_cache = {}
CACHE_DURATION = 10  # seconds

async def get_market_data(request: MarketDataRequest):
    """Fetch market data for a single symbol"""
    try:
        cache_key = f"{request.symbol}_{request.exchange}_{request.interval}_{request.fut_contract}"
        
        # Check cache
        cached_data = data_cache.get(cache_key)
        if cached_data:
            current_time = datetime.now().timestamp()
            if current_time - cached_data['timestamp'] < CACHE_DURATION:
                return cached_data['data']

        # Get interval
        interval = INTERVAL_MAP.get(request.interval)
        if not interval:
            raise HTTPException(status_code=400, detail=f"Invalid interval: {request.interval}")

        # Fetch data
        if request.fut_contract:
            data = tv.get_hist(
                symbol=request.symbol,
                exchange=request.exchange,
                interval=interval,
                n_bars=request.n_bars,
                fut_contract=request.fut_contract
            )
        else:
            data = tv.get_hist(
                symbol=request.symbol,
                exchange=request.exchange,
                interval=interval,
                n_bars=request.n_bars
            )

        if data is None or data.empty:
            raise HTTPException(status_code=404, detail="No data found")

        # Process data
        result = {
            "symbol": request.symbol,
            "exchange": request.exchange,
            "interval": request.interval,
            "data": json.loads(data.round(2).reset_index().to_json(orient="records")),
            "timestamp": datetime.now().timestamp()
        }

        # Update cache
        data_cache[cache_key] = {
            'data': result,
            'timestamp': datetime.now().timestamp()
        }

        return result

    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Routes
@app.get("/")
async def root():
    """API health check endpoint"""
    return {
        "status": "ok",
        "message": "TradingView Data API is running",
        "version": "1.0.0"
    }

@app.post("/api/v1/market-data")
async def get_data(request: MarketDataRequest):
    """Get market data for a single symbol"""
    return await get_market_data(request)

@app.post("/api/v1/market-data/batch")
async def get_batch_data(request: SymbolsRequest):
    """Get market data for multiple symbols"""
    tasks = [get_market_data(symbol) for symbol in request.symbols]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    processed_results = []
    for result in results:
        if isinstance(result, Exception):
            processed_results.append({
                "status": "error",
                "error": str(result)
            })
        else:
            processed_results.append({
                "status": "success",
                "data": result
            })
    
    return processed_results

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.subscriptions = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        # Remove subscriptions for this connection
        for symbol in list(self.subscriptions.keys()):
            if websocket in self.subscriptions[symbol]:
                self.subscriptions[symbol].remove(websocket)
            if not self.subscriptions[symbol]:
                del self.subscriptions[symbol]

    async def subscribe(self, websocket: WebSocket, symbol: str, exchange: str, interval: str):
        key = f"{symbol}_{exchange}_{interval}"
        if key not in self.subscriptions:
            self.subscriptions[key] = set()
        self.subscriptions[key].add(websocket)

    async def unsubscribe(self, websocket: WebSocket, symbol: str, exchange: str, interval: str):
        key = f"{symbol}_{exchange}_{interval}"
        if key in self.subscriptions and websocket in self.subscriptions[key]:
            self.subscriptions[key].remove(websocket)
            if not self.subscriptions[key]:
                del self.subscriptions[key]

    async def broadcast_to_subscribers(self, symbol: str, exchange: str, interval: str, data: dict):
        key = f"{symbol}_{exchange}_{interval}"
        if key in self.subscriptions:
            for connection in self.subscriptions[key].copy():
                try:
                    await connection.send_json(data)
                except Exception as e:
                    logger.error(f"Error sending data to subscriber: {str(e)}")
                    await self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            
            if action == "subscribe":
                symbol = data.get("symbol")
                exchange = data.get("exchange")
                interval = data.get("interval", "1m")
                await manager.subscribe(websocket, symbol, exchange, interval)
                
                # Send initial data
                request = MarketDataRequest(
                    symbol=symbol,
                    exchange=exchange,
                    interval=interval,
                    n_bars=1
                )
                market_data = await get_market_data(request)
                await websocket.send_json(market_data)
                
            elif action == "unsubscribe":
                symbol = data.get("symbol")
                exchange = data.get("exchange")
                interval = data.get("interval", "1m")
                await manager.unsubscribe(websocket, symbol, exchange, interval)
                
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        manager.disconnect(websocket)

# Background task to update subscribed symbols
async def update_subscriptions():
    while True:
        try:
            for key in manager.subscriptions.keys():
                symbol, exchange, interval = key.split("_")
                request = MarketDataRequest(
                    symbol=symbol,
                    exchange=exchange,
                    interval=interval,
                    n_bars=1
                )
                data = await get_market_data(request)
                await manager.broadcast_to_subscribers(symbol, exchange, interval, data)
        except Exception as e:
            logger.error(f"Error updating subscriptions: {str(e)}")
        
        await asyncio.sleep(1)  # Update every second

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_subscriptions())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 