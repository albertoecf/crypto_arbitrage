from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from the .env file
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

# Retrieve credentials from environment variables
#BINANCE
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET = os.getenv('BINANCE_SECRET')

#KRAKEN
KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_SECRET = os.getenv('KRAKEN_SECRET')
