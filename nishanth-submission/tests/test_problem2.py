import pytest
import pandas as pd
import yaml
from src.problem2.anonymizer import anonymize_data, anonymize_columns

# Creates a temporary config file and returns it
def create_temp_config(tmp_path, input_path, output_path):
    config = {
        'input_csv_path': str(input_path),
        'anonymization_spec': [
            {'column': 'first_name'},
            {'column': 'last_name'},
            {'column': 'address'}
        ],
        'output_csv_dir': str(output_path)
    }
    config_path = tmp_path / "test_config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
    return config_path

# Creates a sample CSV file and returns
@pytest.fixture
def sample_csv(tmp_path):
    data = {
        'first_name': ['John', 'Jane', 'Bob'],
        'last_name': ['Doe', 'Smith', 'Johnson'],
        'address': ['123 Main St', '456 Elm St', '789 Oak St'],
        'age': [30, 25, 40]
    }
    df = pd.DataFrame(data)
    input_path = tmp_path / "input"
    input_path.mkdir()
    file_path = input_path / "sample.csv"
    df.to_csv(file_path, index=False)
    return file_path

# Testng the anonymize_data function
def test_anonymize_data(tmp_path, sample_csv):
    output_path = tmp_path / "output"
    output_path.mkdir()
    config_path = create_temp_config(tmp_path, sample_csv.parent, output_path)
    
    anonymize_data(str(config_path), "sample")
    
    # Checking if the output file exists
    output_file = output_path / "anonymized_sample.csv"
    assert output_file.exists()
    
    # Reading the output file and check its contents
    df = pd.read_csv(output_file)
    assert 'first_name' in df.columns
    assert 'last_name' in df.columns
    assert 'address' in df.columns
    assert 'age' in df.columns
    
    # Checking if the anonymized columns contain hashed values
    assert df['first_name'].nunique() == 3
    assert df['last_name'].nunique() == 3
    assert df['address'].nunique() == 3

    # Age is not anonymized
    assert df['age'].dtype == 'int64'

# Testing the anonymize_columns function
def test_anonymize_columns():
    data = {
        'first_name': ['John', 'Jane', 'Bob'],
        'last_name': ['Doe', 'Smith', 'Johnson'],
        'age': [30, 25, 40]
    }
    df = pd.DataFrame(data)
    
    anonymization_spec = [
        {'column': 'first_name'},
        {'column': 'last_name'}
    ]
    
    result = anonymize_columns(df, anonymization_spec)
    
    # Checking if specified columns are anonymized
    assert result['first_name'].nunique() == 3
    assert result['last_name'].nunique() == 3
    assert (result['age'] == [30, 25, 40]).all()

# Testing handling of non-existent columns
def test_anonymize_non_existent_column(caplog):
    data = {'name': ['John', 'Jane', 'Bob']}
    df = pd.DataFrame(data)
    
    anonymization_spec = [{'column': 'non_existent'}]
    
    result = anonymize_columns(df, anonymization_spec)
    
    assert "Column 'non_existent' not found in the DataFrame" in caplog.text
    
    pd.testing.assert_frame_equal(df, result)

# Testing with empty DataFrame
def test_anonymize_empty_dataframe():
    df = pd.DataFrame()
    anonymization_spec = [{'column': 'first_name'}]
    
    result = anonymize_columns(df, anonymization_spec)
    
    assert result.empty