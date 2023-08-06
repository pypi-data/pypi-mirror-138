# Hofund - Proto Recommendor

Python based tool which recommends the common proto messages/fields that can be used as replacements for clevertap fields.

## Requirements

- python 3.9
- pip3.9

## Installation

### Using pip

To install latest version of hofund
```
pip install hofund
```

### Using brew

WIP

## Usage

To check the usage
```
hofund --help
```

Example
```
hofund --f <csv_file> --col <property_column_name> --ctx-col <context_keys_column_name>
```

Context keys should be comma seperated keys that are to be searched
