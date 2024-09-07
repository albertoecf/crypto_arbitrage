# config_reader.py

import yaml
from pathlib import Path

def load_exchange_config(config_path='config/exchanges_config.yaml'):
    """
    Loads the exchange configuration from a YAML file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: A dictionary containing exchanges and their trading pairs.
    """
    base_dir = Path(__file__).resolve().parent.parent
    config_dir = base_dir / config_path

    with open(config_dir, 'r') as file:
        exchange_config = yaml.safe_load(file)

    return exchange_config