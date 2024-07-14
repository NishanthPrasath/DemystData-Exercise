import pytest
import yaml
import json
from io import StringIO
from unittest.mock import mock_open, patch, MagicMock
from src.problem1.utils import load_config, parse_spec, split_line
from src.problem1.parser import parse_fixed_width_file

# Mock data
test_config = {
    "spec_file_path": "configs",
    "fixed_width_file_path": "data/raw",
    "output_csv_dir": "data/processed"
}

test_spec_json = {
    "ColumnNames": ["first_name", "last_name", "address", "date_of_birth"],
    "Offsets": ["20", "20", "70", "10"],
    "FixedWidthEncoding": "windows-1252",
    "IncludeHeader": "True",
    "DelimitedEncoding": "utf-8"
}

fixed_width_data = """Peter               Gomez               299 Mueller Square Suite 053, Lake Johnfort, NC 63073                 1976-06-15
Derrick             Webster             0042 White Station, South Jameshaven, VT 44792                        1992-01-25
"""

def test_load_config():
    mock_open_function = mock_open(read_data=yaml.dump(test_config))
    with patch("builtins.open", mock_open_function):
        config = load_config("dummy_path")
        assert config == test_config

def test_parse_spec():
    mock_open_function = mock_open(read_data=json.dumps(test_spec_json))
    with patch("builtins.open", mock_open_function):
        column_names, field_widths, fixed_width_encoding, delimited_encoding, include_header = parse_spec("dummy_path")
        assert column_names == ["first_name", "last_name", "address", "date_of_birth"]
        assert field_widths == [20, 20, 70, 10]
        assert fixed_width_encoding == "windows-1252"
        assert delimited_encoding == "utf-8"
        assert include_header is True

def test_split_line():
    line = "Peter               Gomez               299 Mueller Square Suite 053, Lake Johnfort, NC 63073                 1976-06-15"
    field_widths = [20, 20, 70, 10]
    fields = split_line(line, field_widths)
    assert fields == ["Peter", "Gomez", "299 Mueller Square Suite 053, Lake Johnfort, NC 63073", "1976-06-15"]

def test_split_line_with_empty_fields():
    line = "Peter                                   299 Mueller Square Suite 053, Lake Johnfort, NC 63073                 1976-06-15"
    field_widths = [20, 20, 70, 10]
    assert split_line(line, field_widths) == ["Peter", "_", "299 Mueller Square Suite 053, Lake Johnfort, NC 63073", "1976-06-15"]

def test_split_line_with_extra_spaces():
    line = "Peter               Gomez               299 Mueller Square Suite 053, Lake Johnfort, NC 63073                            1976-06-15"
    field_widths = [20, 20, 70, 10]
    fields = split_line(line, field_widths)
    assert fields == ["Peter", "Gomez", "299 Mueller Square Suite 053, Lake Johnfort, NC 63073", "_"]

def test_parse_fixed_width_file():
    # Using StringIO to simulate file reading and writing
    with patch("builtins.open", side_effect=[
        StringIO(yaml.dump(test_config)),
        StringIO(json.dumps(test_spec_json)),
        StringIO(fixed_width_data),
        StringIO()
    ]):
        with patch("csv.writer") as mock_csv_writer:
            parse_fixed_width_file("dummy_config_path", "test_personal_info")

            # Check if the the writer was called with expected rows
            mock_csv_writer.return_value.writerow.assert_any_call(["first_name", "last_name", "address", "date_of_birth"])
            mock_csv_writer.return_value.writerow.assert_any_call(["Peter", "Gomez", "299 Mueller Square Suite 053, Lake Johnfort, NC 63073", "1976-06-15"])
            mock_csv_writer.return_value.writerow.assert_any_call(["Derrick", "Webster", "0042 White Station, South Jameshaven, VT 44792", "1992-01-25"])

if __name__ == "__main__":
    pytest.main([__file__])