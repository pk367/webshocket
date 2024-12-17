import json
from tvDatafeed import TvDatafeed, Interval
from collections import OrderedDict
import logging
import traceback
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set environment variable for auth token
os.environ['TVDATAFEED_TOKEN'] = 'eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjo1NDgwNTUyMSwiZXhwIjoxNzI3ODIxNzk0LCJpYXQiOjE3Mjc4MDczOTQsInBsYW4iOiJwcm9fcHJlbWl1bSIsImV4dF9ob3VycyI6MSwicGVybSI6IiIsInN0dWR5X3Blcm0iOiJQVUI7NmEyZWI4MDUxMjc5NDkxOTk0MDk2MWQ4ZjUxMTYwMzUsUFVCOzQ2NjMzNTU3ZDE5YjQwYjE5MjQzMmVmNmYyOTA4ZDE0LFBVQjtjMDYxOTIzODdlMmU0ZDJkYTdjZDEzNmVlMjgxOTVlNixQVUI7ZGJmZGMzZDNmNDA3NDIyZjkzYjE2NDAyYTFmOGMwMGQsUFVCO2YzM2IxNTAzZjIyMDQxYzViZTVmZTkxMzMxY2NjNDE4LFBVQjtjZTNhZDY5MzI5MjQ0NTQ5OTgwMjE3NmM2YzRiNzkxMSxQVUI7NmM5MWEyOTRiM2ViNGQ5MTg3MWZlNzFjMzYyY2VkNTEsUFVCOzdjNGIwOWIyYjRhNjQ5YTNhNjU0ZjY2ZWZmOTE1NTcwLHR2LWNoYXJ0cGF0dGVybnMsUFVCO2YwOTdhNzhmODM0MjRiNmY4MWMwODQ3ZTVjOTg4Y2M4LFBVQjtlYTA4M2Q5MDUzNjQ0NzZkOWRmN2FjODBhMjVkMjg1YixQVUI7NmZiZWE5YmRmMGNmNGQ2YWJiNmFjOWE4NmI4OGM5MjQsUFVCO2UxZjAwZjZlNWY2NjRkNGJiMzM2ZWE5NGVhYzlmY2FlLFBVQjszMGNiYzY5MWJiOTM0YTI1OTkyOGU3NzYxYzg5YjBmNCxQVUI7YTQ4MWI5YzMzMmEwNDZmNThiODhmYmVhYWY4YWFhOTgsUFVCOzNlODU4YWU2MTNiMjQwMGU4MzAyOTE5ZGQ0MWQzOTU4LFBVQjtjNzNlOWMzZDA0YTU0MWQwOTVkMGQ3MzVhYTdiZjU5MSxQVUI7NWEyMGMzZTY2MTdjNDJjNWFjMmRmYzZlZmYxMzlkZjIsUFVCOzAzNzA2NmMyY2VjZTRjYTk4MzI3ODA0MTIzZWFiMjcyLHR2LXByb3N0dWRpZXMsdHYtY2hhcnRfcGF0dGVybnMsUFVCOzJkZDYyMDBkNmJmNjQ1OTI5MGFiNzJiZDZiODQyMzkxLFBVQjtiM2Y3YzBiY2I0NWQ0MzJjYThkNDc4NDczMGE5YzIyMyx0di12b2x1bWVieXByaWNlLFBVQjszOTVkNjAyYzVlZTI0ODMwYTc1MjZjYWFmN2MyNjI3YyIsIm1heF9zdHVkaWVzIjoyNSwibWF4X2Z1bmRhbWVudGFscyI6MTAsIm1heF9jaGFydHMiOjgsIm1heF9hY3RpdmVfYWxlcnRzIjo0MDAsIm1heF9zdHVkeV9vbl9zdHVkeSI6MjQsImZpZWxkc19wZXJtaXNzaW9ucyI6WyJyZWZib25kcyJdLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6NDAwLCJtYXhfYWN0aXZlX2NvbXBsZXhfYWxlcnRzIjo0MDAsIm1heF9jb25uZWN0aW9ucyI6NTB9.cAWGPm30ohtUEBNo1ryPxzxSgkzEHR_zjk8jS3cDI-ERQl2iv-Cs6x-ozIA4HQm9pwF607wk-XMl7AGWdBpRxCaTstq8COYg1pzCbPYYQDW3MIXLG_sL96PZDATfb-EXN3O4ZIPSffAv38QKeBHvnRuU7KbqS_GKjRp3pSXrtAc'

# Mapping for intervals
INTERVAL_MAP = {
    "in_1_minute": Interval.in_1_minute,
    "in_3_minute": Interval.in_3_minute,
    "in_5_minute": Interval.in_5_minute,
    "in_10_minute": Interval.in_5_minute,  # Using 5-minute value for 10-minute data
    "in_15_minute": Interval.in_15_minute,
    "in_30_minute": Interval.in_30_minute,
    "in_45_minute": Interval.in_45_minute,
    "in_75_minute": Interval.in_15_minute,  # Using 15-minute value for 75-minute data
    "in_125_minute": Interval.in_5_minute,  # Using 5-minute value for 125-minute data
    "in_1_hour": Interval.in_1_hour,
    "in_2_hour": Interval.in_2_hour,
    "in_3_hour": Interval.in_3_hour,
    "in_4_hour": Interval.in_4_hour,
    "in_5_hour": Interval.in_1_hour,
    "in_6_hour": Interval.in_3_hour,
    "in_8_hour": Interval.in_4_hour,
    "in_10_hour": Interval.in_1_hour,
    "in_12_hour": Interval.in_1_hour,
    "in_daily": Interval.in_daily,
    "in_weekly": Interval.in_weekly,
    "in_monthly": Interval.in_monthly
}

# Mapping for resampling rules
RULE_MAP = {
    'in_10_minute': '10min',
    'in_75_minute': '75min',
    'in_125_minute': '125min',
    'in_5_hour': '5h',
    'in_6_hour': '6h',
    'in_8_hour': '8h',
    'in_10_hour': '10h',
    'in_12_hour': '12h',
}

def fetch_stock_data_and_resample(symbol, exchange, interval_str, interval, n_bars, fut_contract):
    try:
        logger.debug(f"Attempting to fetch data for {symbol} on {exchange}")
        
        # Initialize TvDatafeed with a dummy session
        tv = TvDatafeed(username='', password='')
        
        # Set the auth token directly
        tv.token = 'eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjo1NDgwNTUyMSwiZXhwIjoxNzI3ODIxNzk0LCJpYXQiOjE3Mjc4MDczOTQsInBsYW4iOiJwcm9fcHJlbWl1bSIsImV4dF9ob3VycyI6MSwicGVybSI6IiIsInN0dWR5X3Blcm0iOiJQVUI7NmEyZWI4MDUxMjc5NDkxOTk0MDk2MWQ4ZjUxMTYwMzUsUFVCOzQ2NjMzNTU3ZDE5YjQwYjE5MjQzMmVmNmYyOTA4ZDE0LFBVQjtjMDYxOTIzODdlMmU0ZDJkYTdjZDEzNmVlMjgxOTVlNixQVUI7ZGJmZGMzZDNmNDA3NDIyZjkzYjE2NDAyYTFmOGMwMGQsUFVCO2YzM2IxNTAzZjIyMDQxYzViZTVmZTkxMzMxY2NjNDE4LFBVQjtjZTNhZDY5MzI5MjQ0NTQ5OTgwMjE3NmM2YzRiNzkxMSxQVUI7NmM5MWEyOTRiM2ViNGQ5MTg3MWZlNzFjMzYyY2VkNTEsUFVCOzdjNGIwOWIyYjRhNjQ5YTNhNjU0ZjY2ZWZmOTE1NTcwLHR2LWNoYXJ0cGF0dGVybnMsUFVCO2YwOTdhNzhmODM0MjRiNmY4MWMwODQ3ZTVjOTg4Y2M4LFBVQjtlYTA4M2Q5MDUzNjQ0NzZkOWRmN2FjODBhMjVkMjg1YixQVUI7NmZiZWE5YmRmMGNmNGQ2YWJiNmFjOWE4NmI4OGM5MjQsUFVCO2UxZjAwZjZlNWY2NjRkNGJiMzM2ZWE5NGVhYzlmY2FlLFBVQjszMGNiYzY5MWJiOTM0YTI1OTkyOGU3NzYxYzg5YjBmNCxQVUI7YTQ4MWI5YzMzMmEwNDZmNThiODhmYmVhYWY4YWFhOTgsUFVCOzNlODU4YWU2MTNiMjQwMGU4MzAyOTE5ZGQ0MWQzOTU4LFBVQjtjNzNlOWMzZDA0YTU0MWQwOTVkMGQ3MzVhYTdiZjU5MSxQVUI7NWEyMGMzZTY2MTdjNDJjNWFjMmRmYzZlZmYxMzlkZjIsUFVCOzAzNzA2NmMyY2VjZTRjYTk4MzI3ODA0MTIzZWFiMjcyLHR2LXByb3N0dWRpZXMsdHYtY2hhcnRfcGF0dGVybnMsUFVCOzJkZDYyMDBkNmJmNjQ1OTI5MGFiNzJiZDZiODQyMzkxLFBVQjtiM2Y3YzBiY2I0NWQ0MzJjYThkNDc4NDczMGE5YzIyMyx0di12b2x1bWVieXByaWNlLFBVQjszOTVkNjAyYzVlZTI0ODMwYTc1MjZjYWFmN2MyNjI3YyIsIm1heF9zdHVkaWVzIjoyNSwibWF4X2Z1bmRhbWVudGFscyI6MTAsIm1heF9jaGFydHMiOjgsIm1heF9hY3RpdmVfYWxlcnRzIjo0MDAsIm1heF9zdHVkeV9vbl9zdHVkeSI6MjQsImZpZWxkc19wZXJtaXNzaW9ucyI6WyJyZWZib25kcyJdLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6NDAwLCJtYXhfYWN0aXZlX2NvbXBsZXhfYWxlcnRzIjo0MDAsIm1heF9jb25uZWN0aW9ucyI6NTB9.cAWGPm30ohtUEBNo1ryPxzxSgkzEHR_zjk8jS3cDI-ERQl2iv-Cs6x-ozIA4HQm9pwF607wk-XMl7AGWdBpRxCaTstq8COYg1pzCbPYYQDW3MIXLG_sL96PZDATfb-EXN3O4ZIPSffAv38QKeBHvnRuU7KbqS_GKjRp3pSXrtAc'
        
        logger.debug("TvDatafeed instance created with token")

        # Fetch data with futures contract if provided
        if fut_contract:
            logger.debug(f"Fetching futures data with contract {fut_contract}")
            data = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=n_bars, fut_contract=fut_contract)
        else:
            logger.debug("Fetching regular data")
            data = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=n_bars)

        if data is None or data.empty:
            logger.warning(f"No data retrieved for symbol: {symbol}")
            return None

        logger.debug(f"Data retrieved successfully. Shape: {data.shape}")
        data = data.round(2)

        # Get resampling rule
        rule = RULE_MAP.get(interval_str)

        if rule:
            logger.debug(f"Resampling data with rule: {rule}")
            df = data.resample(rule=rule, closed='left', label='left', origin=data.index.min()).agg(
                OrderedDict([
                    ('Open', 'first'),
                    ('High', 'max'),
                    ('Low', 'min'),
                    ('Close', 'last'),
                    ('Volume', 'sum')
                ])
            ).dropna()
            return df

        return data

    except Exception as e:
        logger.error(f"Error in fetch_stock_data_and_resample: {str(e)}")
        logger.error(traceback.format_exc())
        return None

def lambda_handler(event, context):
    try:
        logger.debug("Starting lambda_handler")
        logger.debug(f"Event received: {event}")

        # Parse input parameters from query string
        query_params = event.get("queryStringParameters", {})
        symbol = query_params.get("symbol")
        exchange = query_params.get("exchange")
        interval_str = query_params.get("interval", "in_daily")
        n_bars = int(query_params.get("n_bars", 5000))

        logger.debug(f"Parameters: symbol={symbol}, exchange={exchange}, interval={interval_str}, n_bars={n_bars}")

        # Ensure fut_contract is retrieved and converted to int
        fut_contract_str = query_params.get("fut_contract", None)
        fut_contract = int(fut_contract_str) if fut_contract_str is not None else None
        logger.debug(f"Future contract: {fut_contract}")

        # Validate input
        if not symbol or not exchange:
            logger.error("Missing symbol or exchange parameters")
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Missing 'symbol' or 'exchange' in request parameters"})
            }

        # Map interval string to Interval enum
        interval = INTERVAL_MAP.get(interval_str)
        if not interval:
            logger.error(f"Invalid interval value: {interval_str}")
            return {
                'statusCode': 400,
                'body': json.dumps({"error": f"Invalid 'interval' value: {interval_str}"})
            }

        # Fetch data
        try:
            if fut_contract and interval_str in ['in_10_minute', 'in_75_minute', 'in_125_minute']:
                logger.debug("Fetching futures data with resampling")
                data = fetch_stock_data_and_resample(symbol, exchange, interval_str, interval, n_bars, fut_contract)
            elif fut_contract:
                logger.debug("Fetching futures data without resampling")
                tv = TvDatafeed(username='', password='')
                tv.token = 'eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjo1NDgwNTUyMSwiZXhwIjoxNzI3ODIxNzk0LCJpYXQiOjE3Mjc4MDczOTQsInBsYW4iOiJwcm9fcHJlbWl1bSIsImV4dF9ob3VycyI6MSwicGVybSI6IiIsInN0dWR5X3Blcm0iOiJQVUI7NmEyZWI4MDUxMjc5NDkxOTk0MDk2MWQ4ZjUxMTYwMzUsUFVCOzQ2NjMzNTU3ZDE5YjQwYjE5MjQzMmVmNmYyOTA4ZDE0LFBVQjtjMDYxOTIzODdlMmU0ZDJkYTdjZDEzNmVlMjgxOTVlNixQVUI7ZGJmZGMzZDNmNDA3NDIyZjkzYjE2NDAyYTFmOGMwMGQsUFVCO2YzM2IxNTAzZjIyMDQxYzViZTVmZTkxMzMxY2NjNDE4LFBVQjtjZTNhZDY5MzI5MjQ0NTQ5OTgwMjE3NmM2YzRiNzkxMSxQVUI7NmM5MWEyOTRiM2ViNGQ5MTg3MWZlNzFjMzYyY2VkNTEsUFVCOzdjNGIwOWIyYjRhNjQ5YTNhNjU0ZjY2ZWZmOTE1NTcwLHR2LWNoYXJ0cGF0dGVybnMsUFVCO2YwOTdhNzhmODM0MjRiNmY4MWMwODQ3ZTVjOTg4Y2M4LFBVQjtlYTA4M2Q5MDUzNjQ0NzZkOWRmN2FjODBhMjVkMjg1YixQVUI7NmZiZWE5YmRmMGNmNGQ2YWJiNmFjOWE4NmI4OGM5MjQsUFVCO2UxZjAwZjZlNWY2NjRkNGJiMzM2ZWE5NGVhYzlmY2FlLFBVQjszMGNiYzY5MWJiOTM0YTI1OTkyOGU3NzYxYzg5YjBmNCxQVUI7YTQ4MWI5YzMzMmEwNDZmNThiODhmYmVhYWY4YWFhOTgsUFVCOzNlODU4YWU2MTNiMjQwMGU4MzAyOTE5ZGQ0MWQzOTU4LFBVQjtjNzNlOWMzZDA0YTU0MWQwOTVkMGQ3MzVhYTdiZjU5MSxQVUI7NWEyMGMzZTY2MTdjNDJjNWFjMmRmYzZlZmYxMzlkZjIsUFVCOzAzNzA2NmMyY2VjZTRjYTk4MzI3ODA0MTIzZWFiMjcyLHR2LXByb3N0dWRpZXMsdHYtY2hhcnRfcGF0dGVybnMsUFVCOzJkZDYyMDBkNmJmNjQ1OTI5MGFiNzJiZDZiODQyMzkxLFBVQjtiM2Y3YzBiY2I0NWQ0MzJjYThkNDc4NDczMGE5YzIyMyx0di12b2x1bWVieXByaWNlLFBVQjszOTVkNjAyYzVlZTI0ODMwYTc1MjZjYWFmN2MyNjI3YyIsIm1heF9zdHVkaWVzIjoyNSwibWF4X2Z1bmRhbWVudGFscyI6MTAsIm1heF9jaGFydHMiOjgsIm1heF9hY3RpdmVfYWxlcnRzIjo0MDAsIm1heF9zdHVkeV9vbl9zdHVkeSI6MjQsImZpZWxkc19wZXJtaXNzaW9ucyI6WyJyZWZib25kcyJdLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6NDAwLCJtYXhfYWN0aXZlX2NvbXBsZXhfYWxlcnRzIjo0MDAsIm1heF9jb25uZWN0aW9ucyI6NTB9.cAWGPm30ohtUEBNo1ryPxzxSgkzEHR_zjk8jS3cDI-ERQl2iv-Cs6x-ozIA4HQm9pwF607wk-XMl7AGWdBpRxCaTstq8COYg1pzCbPYYQDW3MIXLG_sL96PZDATfb-EXN3O4ZIPSffAv38QKeBHvnRuU7KbqS_GKjRp3pSXrtAc'
                data = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=n_bars, fut_contract=fut_contract)
            elif interval_str in ['in_10_minute', 'in_75_minute', 'in_125_minute']:
                logger.debug("Fetching regular data with resampling")
                data = fetch_stock_data_and_resample(symbol, exchange, interval_str, interval, n_bars, fut_contract=None)
            else:
                logger.debug("Fetching regular data without resampling")
                tv = TvDatafeed(username='', password='')
                tv.token = 'eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjo1NDgwNTUyMSwiZXhwIjoxNzI3ODIxNzk0LCJpYXQiOjE3Mjc4MDczOTQsInBsYW4iOiJwcm9fcHJlbWl1bSIsImV4dF9ob3VycyI6MSwicGVybSI6IiIsInN0dWR5X3Blcm0iOiJQVUI7NmEyZWI4MDUxMjc5NDkxOTk0MDk2MWQ4ZjUxMTYwMzUsUFVCOzQ2NjMzNTU3ZDE5YjQwYjE5MjQzMmVmNmYyOTA4ZDE0LFBVQjtjMDYxOTIzODdlMmU0ZDJkYTdjZDEzNmVlMjgxOTVlNixQVUI7ZGJmZGMzZDNmNDA3NDIyZjkzYjE2NDAyYTFmOGMwMGQsUFVCO2YzM2IxNTAzZjIyMDQxYzViZTVmZTkxMzMxY2NjNDE4LFBVQjtjZTNhZDY5MzI5MjQ0NTQ5OTgwMjE3NmM2YzRiNzkxMSxQVUI7NmM5MWEyOTRiM2ViNGQ5MTg3MWZlNzFjMzYyY2VkNTEsUFVCOzdjNGIwOWIyYjRhNjQ5YTNhNjU0ZjY2ZWZmOTE1NTcwLHR2LWNoYXJ0cGF0dGVybnMsUFVCO2YwOTdhNzhmODM0MjRiNmY4MWMwODQ3ZTVjOTg4Y2M4LFBVQjtlYTA4M2Q5MDUzNjQ0NzZkOWRmN2FjODBhMjVkMjg1YixQVUI7NmZiZWE5YmRmMGNmNGQ2YWJiNmFjOWE4NmI4OGM5MjQsUFVCO2UxZjAwZjZlNWY2NjRkNGJiMzM2ZWE5NGVhYzlmY2FlLFBVQjszMGNiYzY5MWJiOTM0YTI1OTkyOGU3NzYxYzg5YjBmNCxQVUI7YTQ4MWI5YzMzMmEwNDZmNThiODhmYmVhYWY4YWFhOTgsUFVCOzNlODU4YWU2MTNiMjQwMGU4MzAyOTE5ZGQ0MWQzOTU4LFBVQjtjNzNlOWMzZDA0YTU0MWQwOTVkMGQ3MzVhYTdiZjU5MSxQVUI7NWEyMGMzZTY2MTdjNDJjNWFjMmRmYzZlZmYxMzlkZjIsUFVCOzAzNzA2NmMyY2VjZTRjYTk4MzI3ODA0MTIzZWFiMjcyLHR2LXByb3N0dWRpZXMsdHYtY2hhcnRfcGF0dGVybnMsUFVCOzJkZDYyMDBkNmJmNjQ1OTI5MGFiNzJiZDZiODQyMzkxLFBVQjtiM2Y3YzBiY2I0NWQ0MzJjYThkNDc4NDczMGE5YzIyMyx0di12b2x1bWVieXByaWNlLFBVQjszOTVkNjAyYzVlZTI0ODMwYTc1MjZjYWFmN2MyNjI3YyIsIm1heF9zdHVkaWVzIjoyNSwibWF4X2Z1bmRhbWVudGFscyI6MTAsIm1heF9jaGFydHMiOjgsIm1heF9hY3RpdmVfYWxlcnRzIjo0MDAsIm1heF9zdHVkeV9vbl9zdHVkeSI6MjQsImZpZWxkc19wZXJtaXNzaW9ucyI6WyJyZWZib25kcyJdLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6NDAwLCJtYXhfYWN0aXZlX2NvbXBsZXhfYWxlcnRzIjo0MDAsIm1heF9jb25uZWN0aW9ucyI6NTB9.cAWGPm30ohtUEBNo1ryPxzxSgkzEHR_zjk8jS3cDI-ERQl2iv-Cs6x-ozIA4HQm9pwF607wk-XMl7AGWdBpRxCaTstq8COYg1pzCbPYYQDW3MIXLG_sL96PZDATfb-EXN3O4ZIPSffAv38QKeBHvnRuU7KbqS_GKjRp3pSXrtAc'
                data = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=n_bars)

            if data is not None and not data.empty:
                logger.debug("Successfully retrieved and processed data")
                data_json = data.round(2).reset_index().to_json(orient="records")
                return {
                    'statusCode': 200,
                    'body': json.dumps({"symbol": symbol, "data": json.loads(data_json)})
                }
            else:
                logger.warning("No data found")
                return {
                    'statusCode': 404,
                    'body': json.dumps({"error": f"No data found for symbol {symbol} on exchange {exchange}"})
                }

        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'statusCode': 500,
            'body': json.dumps({"error": f"Internal server error: {str(e)}"})
        }

# Simulate query parameters (for testing purposes)
if __name__ == "__main__":
    test_cases = [
        # Test case 1: NSE Futures
        {
            "name": "NSE Futures - BANKNIFTY",
            "params": {
                "symbol": "BANKNIFTY",
                "exchange": "NSE",
                "interval": "in_5_minute",
                "n_bars": "100",
                "fut_contract": "1"
            }
        },
        # Test case 2: MCX Commodities
        {
            "name": "MCX Gold",
            "params": {
                "symbol": "GOLD",
                "exchange": "MCX",
                "interval": "in_5_minute",
                "n_bars": "100",
                "fut_contract": "1"
            }
        },
        # Test case 3: COMEX Futures
        {
            "name": "COMEX Gold Futures",
            "params": {
                "symbol": "GC1!",
                "exchange": "COMEX",
                "interval": "in_5_minute",
                "n_bars": "100"
            }
        },
        # Test case 4: NYMEX Futures
        {
            "name": "NYMEX Crude Oil",
            "params": {
                "symbol": "CL1!",
                "exchange": "NYMEX",
                "interval": "in_5_minute",
                "n_bars": "100"
            }
        },
        # Test case 5: Crypto - Binance
        {
            "name": "Binance Bitcoin/USDT",
            "params": {
                "symbol": "BTCUSDT",
                "exchange": "BINANCE",
                "interval": "in_5_minute",
                "n_bars": "100"
            }
        },
        # Test case 6: Crypto - Coinbase
        {
            "name": "Coinbase Ethereum/USD",
            "params": {
                "symbol": "ETHUSD",
                "exchange": "COINBASE",
                "interval": "in_5_minute",
                "n_bars": "100"
            }
        },
        # Test case 7: Forex
        {
            "name": "Forex EUR/USD",
            "params": {
                "symbol": "EURUSD",
                "exchange": "FX",
                "interval": "in_5_minute",
                "n_bars": "100"
            }
        },
        # Test case 8: MCX Energy
        {
            "name": "MCX Crude Oil",
            "params": {
                "symbol": "CRUDEOIL",
                "exchange": "MCX",
                "interval": "in_5_minute",
                "n_bars": "100",
                "fut_contract": "1"
            }
        }
    ]

    context = {}
    logger.debug("Starting test runs with multiple exchanges")

    for test_case in test_cases:
        try:
            print(f"\nTesting {test_case['name']}...")
            simulated_event = {
                "queryStringParameters": test_case['params']
            }
            response = lambda_handler(simulated_event, context)
            print(f"Response for {test_case['name']}:", response['statusCode'])
            if response['statusCode'] != 200:
                print("Error:", json.loads(response['body'])['error'])
            else:
                data = json.loads(response['body'])['data']
                print(f"Data points retrieved: {len(data)}")
        except Exception as e:
            print(f"Error testing {test_case['name']}: {str(e)}")
