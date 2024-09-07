from src.models.UnifiedMarketData import UnifiedMarketData
from pydantic import ValidationError
import datetime


def translate_message(raw_message):
    exchange_id = raw_message['exchange']
    symbol = raw_message['symbol']
    raw_data = raw_message['data']

    # Initialize translated data
    translated_data = None

    # Translation logic for Binance
    if exchange_id == 'binance':
        translated_data = {
            "exchange": exchange_id,
            "symbol": symbol,
            "price": raw_data['last'],
            "bid": raw_data['bid'],
            "ask": raw_data['ask'],
            "timestamp": datetime.datetime.utcfromtimestamp(raw_data['timestamp'] / 1000) if raw_data[
                'timestamp'] else None
        }

    # Translation logic for Kraken
    elif exchange_id == 'kraken':
        # Access nested fields in the 'info' section of Kraken's response
        kraken_info = raw_data['info']

        # Check if the necessary fields exist in the nested 'info' section
        if 'c' in kraken_info and 'b' in kraken_info and 'a' in kraken_info:
            translated_data = {
                "exchange": exchange_id,
                "symbol": symbol,
                "price": float(kraken_info['c'][0]),  # Kraken's 'c' field is the last trade price
                "bid": float(kraken_info['b'][0]),  # Kraken's 'b' field is the current highest bid
                "ask": float(kraken_info['a'][0]),  # Kraken's 'a' field is the current lowest ask
                "timestamp": datetime.datetime.utcnow().isoformat()  # Use the current UTC time for Kraken
            }
        else:
            print(f"Error: Missing expected fields in Kraken's 'info' response for {symbol}")
            print(f"Kraken raw data: {raw_data}")  # Log the raw data for debugging
            return None

    # Validate and parse the translated data using the Pydantic model
    try:
        validated_data = UnifiedMarketData(**translated_data)
        return validated_data.dict()
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return None
