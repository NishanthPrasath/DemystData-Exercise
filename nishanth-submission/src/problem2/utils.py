import yaml
import logging

def load_config(config_path):
    """Loads the YAML configuration file and returns it"""
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        logging.debug(f"Configuration loaded successfully from {config_path}")
        return config
    except Exception as e:
        logging.error(f"Error loading configuration: {str(e)}")
        raise