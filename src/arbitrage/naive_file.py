import yaml
from pathlib import Path

# Define the base directory and config directory paths
base_dir = Path(__file__).resolve().parent.parent  # Navigate up to the src directory
config_dir = base_dir / 'config'  # Point to the config directory

# Load Kafka configuration
with open(config_dir / 'kafka_config.yaml', 'r') as file:
    kafka_config = yaml.safe_load(file)

# Load Exchange configuration
with open(config_dir / 'exchanges_config.yaml', 'r') as file:
    exchange_config = yaml.safe_load(file)


# Example usage of the loaded configuration
def print_configs():
    # Kafka configuration
    bootstrap_servers = kafka_config['bootstrap_servers']
    market_data_topic = kafka_config['topics']['market_data_topic']

    # Binance Exchange configuration
    binance_api_key = exchange_config['binance']['api_key']
    binance_secret = exchange_config['binance']['secret']

    # Print loaded configuration values
    print(f"Kafka Bootstrap Servers: {bootstrap_servers}")
    print(f"Market Data Topic: {market_data_topic}")
    print(f"Binance API Key: {binance_api_key}")
    print(f"Binance Secret: {binance_secret}")


if __name__ == "__main__":
    print_configs()
