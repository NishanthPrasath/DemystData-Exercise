# DemystData Coding Exercise

## Problem 1 - Data Parsing

- Implemented a flexible parser that can handle fixed-width files based on a provided JSON specification.
- The parser reads the specification to determine column names, field widths, and encoding details.
- Incorporated encoding handling to support various character encodings for both input and output files.
- The processed data is then written to a CSV file.

## Problem 2 - Data Anonymization

- Developed a solution to anonymize specific columns (first_name, last_name, and address) in CSV files.
- Implemented using Python and pandas for smaller datasets.
- For larger datasets (2GB+), provided an alternative solution using PySpark on Databricks to demonstrate scalability.
- Used SHA-256 hashing for anonymization to ensure data privacy.

## Steps to Setup and Run the Code

1. Clone this repository to your local machine.

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. Adjust the data generation settings (optional):
   - Open `configs/data_generator_config.yaml`
   - Modify the `num_records` value to change the number of records generated:
     ```yaml
     spec_path: 'configs'
     output_dir: 'data/raw'
     num_records: 10000
     ```

4. Generate sample data:
   ```
   python data_generator.py personal_info
   ```
   This will generate a txt file in the `data/raw` folder.
  > [!NOTE]  
  > The current implementation generates fake data for first_name, last_name, address, and date_of_birth, compatible with the provided `personal_info_spec.json` in the configs folder.

5. For custom fixed-width files:
   - Place the file in the `data/raw` folder
   - Provide a corresponding spec file in the `configs` folder, named `<filename>_spec.json`
   - The spec file should follow this structure:
     ```json
     {
         "ColumnNames": ["first_name", "last_name", "address", "date_of_birth"],
         "Offsets": ["20", "20", "70", "10"],
         "FixedWidthEncoding": "windows-1252",
         "IncludeHeader": "True",
         "DelimitedEncoding": "utf-8"
     }
     ```

6. Run Problem 1 (Data Parsing):
   ```
   python main.py 1 <filename without extension>
   ```
   This will generate a CSV file in the `data/processed` folder.

7. For Problem 2 (Data Anonymization):
   - Adjust the columns to anonymize in `configs/anonymization_config.yaml`:
     ```yaml
     input_csv_path: "data/processed"
     anonymization_spec:
       - column: "first_name"
       - column: "last_name"
       - column: "address"
     output_csv_dir: "data/anonymized"
     ```
   - Run the anonymization:
     ```
     python main.py 2 <filename without extension>
     ```
   - The anonymized file will be created in the `data/anonymized` folder.

8. For processing larger files with PySpark:
   - Check the `problem2_data_processing_spark.ipynb` file in the `notebooks` folder.
   - You can also view it on Databricks: [Spark Notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/3503351804964356/637932950494222/4546680964800526/latest.html)

9. To run tests:
   ```
   pytest tests/test_problem1.py
   pytest tests/test_problem2.py
   ```

## Docker Setup

To build and run the application using Docker:

1. Build the Docker image:
   ```
   docker build -t data-processing-app .
   ```

2. Run the container:
   ```
   docker run -v $(pwd)/data:/app/data data-processing-app
   ```

3. To run specific parts of the application:
   ```
   # Generate data
   docker run -v $(pwd)/data:/app/data data-processing-app src/data_generator.py personal_info

   # Run problem 1
   docker run -v $(pwd)/data:/app/data data-processing-app src/main.py 1 personal_info

   # Run problem 2
   docker run -v $(pwd)/data:/app/data data-processing-app src/main.py 2 personal_info
   ```
