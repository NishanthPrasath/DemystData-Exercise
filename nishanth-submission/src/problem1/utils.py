import json
import yaml
import logging

#Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path):
    """Load and parse the configuration file"""
    try:
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        raise

def parse_spec(spec_path):
    """Parses the specification file extracting relevant information and returns it"""
    try:
        with open(spec_path, 'r') as spec_file:
            spec = json.load(spec_file)
            
        column_names = spec['ColumnNames']
        field_widths = [int(width) for width in spec['Offsets']]
        fixed_width_encoding = spec['FixedWidthEncoding']
        delimited_encoding = spec['DelimitedEncoding']
        include_header = spec['IncludeHeader'].lower() == 'true'
        
        return column_names, field_widths, fixed_width_encoding, delimited_encoding, include_header
    except Exception as e:
        logger.error(f"Error parsing specification file: {e}")
        raise

def split_line(line, field_widths):
    """Splits a fixed-width line into fields based on the provided field widths"""
    result = []
    start = 0
    for width in field_widths:
        field = line[start:start + width].strip()
        # print(field)
        logger.debug(f"Current field: {field}")

        result.append(field if field else '_')
        start += width
            
    logging.debug(f"Final: {result}")
    
    return result