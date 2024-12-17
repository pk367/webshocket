import asyncio
import websockets
import json
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_rest_api():
    """Test REST API endpoints"""
    async with aiohttp.ClientSession() as session:
        # Test health check
        async with session.get('http://localhost:8000/') as response:
            data = await response.json()
            logger.info(f"Health check response: {data}")
            assert response.status == 200

        # Test single symbol data
        payload = {
            "symbol": "NIFTY",
            "exchange": "NSE",
            "interval": "1m",
            "n_bars": 10
        }
        async with session.post('http://localhost:8000/api/v1/market-data', json=payload) as response:
            data = await response.json()
            logger.info(f"Single symbol data response status: {response.status}")
            assert response.status == 200
            logger.info(f"Data points received: {len(data['data'])}")

        # Test batch data
        payload = {
            "symbols": [
                {
                    "symbol": "NIFTY",
                    "exchange": "NSE",
                    "interval": "1m",
                    "n_bars": 10
                },
                {
                    "symbol": "BANKNIFTY",
                    "exchange": "NSE",
                    "interval": "1m",
                    "n_bars": 10
                }
            ]
        }
        async with session.post('http://localhost:8000/api/v1/market-data/batch', json=payload) as response:
            data = await response.json()
            logger.info(f"Batch data response status: {response.status}")
            assert response.status == 200
            logger.info(f"Number of responses: {len(data)}")

async def test_websocket():
    """Test WebSocket connection and data streaming"""
    uri = "ws://localhost:8000/ws/test_client"
    async with websockets.connect(uri) as websocket:
        # Subscribe to a symbol
        subscribe_message = {
            "action": "subscribe",
            "symbol": "NIFTY",
            "exchange": "NSE",
            "interval": "1m"
        }
        await websocket.send(json.dumps(subscribe_message))
        logger.info("Subscribed to NIFTY data")

        # Wait for some data
        for _ in range(3):
            response = await websocket.recv()
            data = json.loads(response)
            logger.info(f"Received WebSocket data: {len(data['data'])} data points")
            await asyncio.sleep(1)

        # Unsubscribe
        unsubscribe_message = {
            "action": "unsubscribe",
            "symbol": "NIFTY",
            "exchange": "NSE",
            "interval": "1m"
        }
        await websocket.send(json.dumps(unsubscribe_message))
        logger.info("Unsubscribed from NIFTY data")

async def main():
    """Run all tests"""
    logger.info("Starting API tests...")
    
    try:
        logger.info("\nTesting REST API endpoints...")
        await test_rest_api()
        
        logger.info("\nTesting WebSocket functionality...")
        await test_websocket()
        
        logger.info("\nAll tests completed successfully!")
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 