import os
import argparse
import logging
from problem1.parser import parse_fixed_width_file
from problem2.anonymizer import anonymize_data

def main():

    # Setting up argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description="Data Engineering Coding Challenge")
    parser.add_argument('problem', type=int, choices=[1, 2], help="Problem number (1 or 2)")
    # parser.add_argument('config', type=str, help="Path to the configuration file")
    parser.add_argument('filename', type=str, help="Name of the file without extensions")
    
    args = parser.parse_args()

    # Setting up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Getting the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if args.problem == 1:
        # Runs Problem 1: Parsing a fixed-width file
        logging.info("Running Problem 1: Fixed Width File Parser")
        config_path = os.path.join(project_root, 'configs/parser_config.yaml')
        parse_fixed_width_file(config_path, args.filename)
    elif args.problem == 2:
        # Runs Problem 2: Anonymizing data
        logging.info("Running Problem 2: Data Anonymizer")
        config_path = os.path.join(project_root, 'configs/anonymization_config.yaml')
        anonymize_data(config_path, args.filename)
    else:
        logging.error("Invalid problem number. Please choose 1 or 2.")

if __name__ == "__main__":
    main()