import json
import yaml
from faker import Faker
import argparse
import logging
import os

# current_dir = os.path.dirname(os.path.abspath(__file__))
# config_path = os.path.join(current_dir, '..', 'configs', 'data_generator_config.yaml')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path):
    """Loads and returns the YAML configuration file"""
    try:
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        raise

def load_spec(spec_path):
    """Loads and returns the JSON specification file"""
    try:
        with open(spec_path, 'r') as spec_file:
            return json.load(spec_file)
    except FileNotFoundError:
        logger.error(f"Spec file not found: {spec_path}")
        raise

def generate_mock_data(num_records):
    """Generates mock data using Faker"""
    fake = Faker()
    data = []
    
    for _ in range(num_records):
        record = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'address': fake.address().replace('\n', ', '),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
        }
        data.append(record)
    
    logger.info(f"Generated {num_records} mock records")
    return data

def create_fixed_width_file(data, spec, output_path):
    """Creates a fixed-width file based on the provided spec and data"""
    column_names = spec['ColumnNames']
    offsets = [int(offset) for offset in spec['Offsets']]
    encoding = spec['FixedWidthEncoding']
    include_header = spec['IncludeHeader'].lower() == 'true'

    try:
        with open(output_path, 'w', encoding=encoding) as f:
            if not include_header:
                header = ''.join(name.ljust(offset) for name, offset in zip(column_names, offsets))
                f.write(header + '\n')
            
            for record in data:
                line = ''
                for column, offset in zip(column_names, offsets):
                    value = str(record[column])[:offset]
                    line += value.ljust(offset)
                f.write(line + '\n')
        
        logger.info(f"Successfully created fixed-width file: {output_path}")
    except IOError as e:
        logger.error(f"Error writing to file {output_path}: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Generate fixed-width data file.')
    parser.add_argument('filename', help='Name of the file to save without extensions')
    args = parser.parse_args()

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, 'configs/data_generator_config.yaml')

        config = load_config(config_path)
        spec_path = os.path.join(project_root, config['spec_path'], f"{args.filename}_spec.json")
        output_dir = os.path.join(project_root, config['output_dir'])
        num_records = config['num_records']

        output_path = os.path.join(output_dir, f"{args.filename}.txt")

        spec = load_spec(spec_path)
        data = generate_mock_data(num_records)
        create_fixed_width_file(data, spec, output_path)

        # print("Process completed")
        logger.info(f"Process completed")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == '__main__':
    main()