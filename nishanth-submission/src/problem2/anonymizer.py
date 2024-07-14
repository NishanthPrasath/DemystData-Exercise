import logging
import os
import pandas as pd
import hashlib
from .utils import load_config

def anonymize_data(config_path, filename):
    """Anonymize data based on the provided configuration and filename"""

    # Loading configuration
    config = load_config(config_path)
    logging.info("Configuration loaded successfully")

    try:
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Construct input file path
        input_file_path = os.path.join(project_root, config['input_csv_path'], f"{filename}.csv")
        logging.info(f"Input file path: {input_file_path}")

        # Checking if file exists in the path
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"Input file not found: {input_file_path}")
        
        # Read input CSV file
        df = pd.read_csv(input_file_path)
        logging.info(f"Input CSV loaded from {input_file_path}")
        logging.debug(f"Input DataFrame shape: {df.shape}")

        # Anonymize specified columns in the config
        df = anonymize_columns(df, config['anonymization_spec'])
        logging.info("Data anonymization completed")

        # Construct output file path
        output_file_path = os.path.join(project_root, config['output_csv_dir'], f"anonymized_{filename}.csv")
        
        # Writing the anonymized data to output directory
        df.to_csv(output_file_path, index=False)
        logging.info(f"Anonymized data written to {output_file_path}")

    except Exception as e:
        logging.error(f"Error during data anonymization: {str(e)}")
        raise

def anonymize_columns(df: pd.DataFrame, anonymization_spec: list) -> pd.DataFrame:
    """Anonymize specified columns in the DataFrame"""
    for column_spec in anonymization_spec:
        column_name = column_spec['column']
        if column_name in df.columns:
            df[column_name] = df[column_name].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
            logging.debug(f"Column '{column_name}' anonymized")
        else:
            logging.warning(f"Column '{column_name}' not found in the DataFrame")
    
    return df