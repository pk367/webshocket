import asyncio
import pandas as pd
from datetime import datetime
from tvdatafeed import TvDatafeed, Interval
import logging
import json
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize TvDatafeed
tv = TvDatafeed(username='', password='')
tv.token = 'eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjo1NDgwNTUyMSwiZXhwIjoxNzI3ODIxNzk0LCJpYXQiOjE3Mjc4MDczOTQsInBsYW4iOiJwcm9fcHJlbWl1bSIsImV4dF9ob3VycyI6MSwicGVybSI6IiIsInN0dWR5X3Blcm0iOiJQVUI7NmEyZWI4MDUxMjc5NDkxOTk0MDk2MWQ4ZjUxMTYwMzUsUFVCOzQ2NjMzNTU3ZDE5YjQwYjE5MjQzMmVmNmYyOTA4ZDE0LFBVQjtjMDYxOTIzODdlMmU0ZDJkYTdjZDEzNmVlMjgxOTVlNixQVUI7ZGJmZGMzZDNmNDA3NDIyZjkzYjE2NDAyYTFmOGMwMGQsUFVCO2YzM2IxNTAzZjIyMDQxYzViZTVmZTkxMzMxY2NjNDE4LFBVQjtjZTNhZDY5MzI5MjQ0NTQ5OTgwMjE3NmM2YzRiNzkxMSxQVUI7NmM5MWEyOTRiM2ViNGQ5MTg3MWZlNzFjMzYyY2VkNTEsUFVCOzdjNGIwOWIyYjRhNjQ5YTNhNjU0ZjY2ZWZmOTE1NTcwLHR2LWNoYXJ0cGF0dGVybnMsUFVCO2YwOTdhNzhmODM0MjRiNmY4MWMwODQ3ZTVjOTg4Y2M4LFBVQjtlYTA4M2Q5MDUzNjQ0NzZkOWRmN2FjODBhMjVkMjg1YixQVUI7NmZiZWE5YmRmMGNmNGQ2YWJiNmFjOWE4NmI4OGM5MjQsUFVCO2UxZjAwZjZlNWY2NjRkNGJiMzM2ZWE5NGVhYzlmY2FlLFBVQjszMGNiYzY5MWJiOTM0YTI1OTkyOGU3NzYxYzg5YjBmNCxQVUI7YTQ4MWI5YzMzMmEwNDZmNThiODhmYmVhYWY4YWFhOTgsUFVCOzNlODU4YWU2MTNiMjQwMGU4MzAyOTE5ZGQ0MWQzOTU4LFBVQjtjNzNlOWMzZDA0YTU0MWQwOTVkMGQ3MzVhYTdiZjU5MSxQVUI7NWEyMGMzZTY2MTdjNDJjNWFjMmRmYzZlZmYxMzlkZjIsUFVCOzAzNzA2NmMyY2VjZTRjYTk4MzI3ODA0MTIzZWFiMjcyLHR2LXByb3N0dWRpZXMsdHYtY2hhcnRfcGF0dGVybnMsUFVCOzJkZDYyMDBkNmJmNjQ1OTI5MGFiNzJiZDZiODQyMzkxLFBVQjtiM2Y3YzBiY2I0NWQ0MzJjYThkNDc4NDczMGE5YzIyMyx0di12b2x1bWVieXByaWNlLFBVQjszOTVkNjAyYzVlZTI0ODMwYTc1MjZjYWFmN2MyNjI3YyIsIm1heF9zdHVkaWVzIjoyNSwibWF4X2Z1bmRhbWVudGFscyI6MTAsIm1heF9jaGFydHMiOjgsIm1heF9hY3RpdmVfYWxlcnRzIjo0MDAsIm1heF9zdHVkeV9vbl9zdHVkeSI6MjQsImZpZWxkc19wZXJtaXNzaW9ucyI6WyJyZWZib25kcyJdLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6NDAwLCJtYXhfYWN0aXZlX2NvbXBsZXhfYWxlcnRzIjo0MDAsIm1heF9jb25uZWN0aW9ucyI6NTB9.cAWGPm30ohtUEBNo1ryPxzxSgkzEHR_zjk8jS3cDI-ERQl2iv-Cs6x-ozIA4HQm9pwF607wk-XMl7AGWdBpRxCaTstq8COYg1pzCbPYYQDW3MIXLG_sL96PZDATfb-EXN3O4ZIPSffAv38QKeBHvnRuU7KbqS_GKjRp3pSXrtAc'

# Mapping for intervals
INTERVAL_MAP = {
    "in_1_minute": Interval.in_1_minute,
    "in_3_minute": Interval.in_3_minute,
    "in_5_minute": Interval.in_5_minute,
    "in_15_minute": Interval.in_15_minute,
    "in_30_minute": Interval.in_30_minute,
    "in_45_minute": Interval.in_45_minute,
    "in_1_hour": Interval.in_1_hour,
    "in_2_hour": Interval.in_2_hour,
    "in_3_hour": Interval.in_3_hour,
    "in_4_hour": Interval.in_4_hour,
    "in_daily": Interval.in_daily,
    "in_weekly": Interval.in_weekly,
    "in_monthly": Interval.in_monthly
}

# Test cases for different exchanges
TEST_CASES = [
    # Indian Markets
    {
        "category": "Indian Indices",
        "symbols": [
            {"symbol": "NIFTY", "exchange": "NSE"},
            {"symbol": "BANKNIFTY", "exchange": "NSE"},
            {"symbol": "SENSEX", "exchange": "BSE"},
        ]
    },
    {
        "category": "Indian Stocks",
        "symbols": [
            {"symbol": "RELIANCE", "exchange": "NSE"},
            {"symbol": "TCS", "exchange": "NSE"},
            {"symbol": "HDFCBANK", "exchange": "NSE"},
        ]
    },
    {
        "category": "Indian Futures",
        "symbols": [
            {"symbol": "NIFTY", "exchange": "NSE", "fut_contract": 1},
            {"symbol": "BANKNIFTY", "exchange": "NSE", "fut_contract": 1},
            {"symbol": "RELIANCE", "exchange": "NSE", "fut_contract": 1},
        ]
    },
    # MCX Commodities
    {
        "category": "MCX Commodities",
        "symbols": [
            {"symbol": "GOLD", "exchange": "MCX", "fut_contract": 1},
            {"symbol": "SILVER", "exchange": "MCX", "fut_contract": 1},
            {"symbol": "CRUDEOIL", "exchange": "MCX", "fut_contract": 1},
            {"symbol": "NATURALGAS", "exchange": "MCX", "fut_contract": 1},
            {"symbol": "COPPER", "exchange": "MCX", "fut_contract": 1},
        ]
    },
    # International Commodities
    {
        "category": "COMEX Futures",
        "symbols": [
            {"symbol": "GC1!", "exchange": "COMEX"},  # Gold
            {"symbol": "SI1!", "exchange": "COMEX"},  # Silver
            {"symbol": "HG1!", "exchange": "COMEX"},  # Copper
        ]
    },
    {
        "category": "NYMEX Futures",
        "symbols": [
            {"symbol": "CL1!", "exchange": "NYMEX"},  # Crude Oil
            {"symbol": "NG1!", "exchange": "NYMEX"},  # Natural Gas
            {"symbol": "RB1!", "exchange": "NYMEX"},  # Gasoline
        ]
    },
    # Crypto Markets
    {
        "category": "Binance Crypto",
        "symbols": [
            {"symbol": "BTCUSDT", "exchange": "BINANCE"},
            {"symbol": "ETHUSDT", "exchange": "BINANCE"},
            {"symbol": "BNBUSDT", "exchange": "BINANCE"},
        ]
    },
    {
        "category": "Coinbase Crypto",
        "symbols": [
            {"symbol": "BTCUSD", "exchange": "COINBASE"},
            {"symbol": "ETHUSD", "exchange": "COINBASE"},
        ]
    },
]

# Test intervals (reduced for faster testing)
TEST_INTERVALS = [
    "in_1_minute",
    "in_5_minute",
    "in_15_minute",
    "in_1_hour",
    "in_daily",
]

def test_symbol(symbol_info, interval_str):
    """Test a single symbol with given interval"""
    try:
        interval = INTERVAL_MAP[interval_str]
        symbol = symbol_info["symbol"]
        exchange = symbol_info["exchange"]
        fut_contract = symbol_info.get("fut_contract")
        
        start_time = datetime.now()
        
        if fut_contract:
            data = tv.get_hist(
                symbol=symbol,
                exchange=exchange,
                interval=interval,
                n_bars=10,
                fut_contract=fut_contract
            )
        else:
            data = tv.get_hist(
                symbol=symbol,
                exchange=exchange,
                interval=interval,
                n_bars=10
            )
            
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        if data is not None and not data.empty:
            return {
                "symbol": symbol,
                "exchange": exchange,
                "interval": interval_str,
                "status": "success",
                "data_points": len(data),
                "response_time": response_time,
                "latest_time": data.index[-1].strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            return {
                "symbol": symbol,
                "exchange": exchange,
                "interval": interval_str,
                "status": "no_data",
                "response_time": response_time,
            }
            
    except Exception as e:
        return {
            "symbol": symbol_info["symbol"],
            "exchange": symbol_info["exchange"],
            "interval": interval_str,
            "status": "error",
            "error": str(e)
        }

def generate_report(results):
    """Generate HTML report from test results"""
    df = pd.DataFrame(results)
    
    # Calculate success rates
    success_by_category = df.groupby('category')['status'].apply(
        lambda x: (x == 'success').mean() * 100
    ).round(2)
    
    success_by_exchange = df.groupby('exchange')['status'].apply(
        lambda x: (x == 'success').mean() * 100
    ).round(2)
    
    # Generate HTML report
    html = """
    <html>
    <head>
        <title>TradingView Data API Test Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .success { color: green; }
            .error { color: red; }
            .no_data { color: orange; }
        </style>
    </head>
    <body>
    """
    
    # Add summary
    html += f"""
    <h1>TradingView Data API Test Report</h1>
    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <h2>Success Rates by Category</h2>
    {success_by_category.to_frame().to_html()}
    
    <h2>Success Rates by Exchange</h2>
    {success_by_exchange.to_frame().to_html()}
    """
    
    # Add detailed results
    html += """
    <h2>Detailed Results</h2>
    """
    
    for category in df['category'].unique():
        html += f"<h3>{category}</h3>"
        category_data = df[df['category'] == category]
        
        # Convert status to colored text
        category_data['status'] = category_data['status'].apply(
            lambda x: f'<span class="{x}">{x}</span>'
        )
        
        html += category_data.to_html(escape=False)
    
    html += "</body></html>"
    
    # Save report
    with open('test_report.html', 'w') as f:
        f.write(html)
    
    logger.info("Test report generated: test_report.html")

def main():
    logger.info("Starting TradingView Data API tests...")
    results = []
    
    for category in TEST_CASES:
        logger.info(f"\nTesting {category['category']}...")
        
        for symbol_info in category["symbols"]:
            symbol_name = f"{symbol_info['symbol']}/{symbol_info['exchange']}"
            logger.info(f"\nTesting {symbol_name}")
            
            for interval in TEST_INTERVALS:
                result = test_symbol(symbol_info, interval)
                result["category"] = category["category"]
                results.append(result)
                
                status_emoji = "✅" if result["status"] == "success" else "❌"
                logger.info(f"{status_emoji} {interval}: {result['status']}")
                
                if result["status"] == "success":
                    logger.info(f"   Data points: {result['data_points']}")
                    logger.info(f"   Response time: {result['response_time']:.2f}s")
                    logger.info(f"   Latest data: {result['latest_time']}")
                elif result["status"] == "error":
                    logger.error(f"   Error: {result['error']}")
                
                # Add delay to prevent rate limiting
                import time
                time.sleep(1)
    
    generate_report(results)
    logger.info("Testing completed!")

if __name__ == "__main__":
    main() 