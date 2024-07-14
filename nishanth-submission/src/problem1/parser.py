import csv
import logging
import os

from .utils import load_config, parse_spec, split_line

def parse_fixed_width_file(config_path, filename):
    """Parses a fixed-width file and generates a CSV file based on the provided configuration and filename"""

    # Setting up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Loading configuration
        config = load_config(config_path)

        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        spec_file_path = os.path.join(project_root, config['spec_file_path'], f"{filename}_spec.json")
        fixed_width_file_path = os.path.join(project_root, config['fixed_width_file_path'], f"{filename}.txt")
        output_csv_dir = os.path.join(project_root, config['output_csv_dir'])

        # Parse specification
        column_names, field_widths, fixed_width_encoding, delimited_encoding, include_header = parse_spec(spec_file_path)

        # os.makedirs(output_csv_dir, exist_ok=True)

        # Define output CSV file path
        output_csv_path = os.path.join(output_csv_dir, f"{filename}.csv")

        # Process fixed-width file and write to CSV
        with open(fixed_width_file_path, 'r', encoding=fixed_width_encoding) as input_file, \
             open(output_csv_path, 'w', newline='', encoding=delimited_encoding) as output_file:

            csv_writer = csv.writer(output_file)

            if include_header:
                csv_writer.writerow(column_names)

            for line_number, line in enumerate(input_file, start=1):
                try:
                    fields = split_line(line.rstrip('\n'), field_widths)
                    csv_writer.writerow(fields)
                except Exception as e:
                    logging.error(f"Error processing line {line_number}: {e}")

        logging.info(f"Parsing complete. Output saved to {output_csv_path}")

    except Exception as e:
        logging.error(f"An error occurred during parsing: {e}")
        raise