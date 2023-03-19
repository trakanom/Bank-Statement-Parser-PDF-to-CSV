# Bank Statement Parsing Tool

This bank statement parsing tool is designed to efficiently and accurately parse PDF bank statements from multiple banks, extract transaction data, and export the results to a CSV file.

## Features

- Supports multiple banks with customizable parsing configurations
- Classifies statements based on bank-specific identification rules
- Extracts transaction data from bank statements
- Cleans and validates extracted data
- Exports parsed transaction data to a CSV file

## Getting Started

### Prerequisites

To use this tool, you'll need to have the following installed:

- Python 3.7 or higher
- [pandas](https://pandas.pydata.org/)
- [tabula-py](https://pypi.org/project/tabula-py/)
- [numpy](https://numpy.org/)

### Installation

1. Clone the repository or download the project files.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Setting up a virtual environment (Optional)

Using a virtual environment is recommended to avoid conflicts with other Python projects or system-wide packages. Follow these steps to set up a virtual environment using `virtualenv`:

1. Install `virtualenv` if you haven't already:

```bash
pip install virtualenv
```

2. Navigate to the project directory and create a new virtual environment:

```bash
cd /path/to/bank-statement-parsing-tool
virtualenv venv
```

This will create a new folder named `venv` in your project directory. This folder contains the virtual environment's Python interpreter and packages.

3. Activate the virtual environment:

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

Once the virtual environment is activated, your command prompt should show the environment's name, like this: `(venv)`.

4. Install the required dependencies inside the virtual environment:

```bash
pip install -r requirements.txt
```

5. Now you can run the bank statement parsing tool within the virtual environment.

To deactivate the virtual environment when you're done, simply run:

```bash
deactivate
```


### Usage

1. Place your PDF bank statements in the `input` folder within the working directory (e.g., `test_data/input/`).
2. Update the `CONFIG.py` file to include the necessary configuration settings for your specific banks. (Refer to the provided example for guidance.)
3. Modify the `app.py` file to include the bank configurations you want to use.
4. Run `app.py`:

```bash
python app.py
```

5. The parsed transaction data will be exported to a CSV file in the `output` directory (e.g., `output/results.csv`).

## Customizing Bank Configurations

To add support for a new bank or modify an existing bank's configuration, update the `CONFIG.py` file with the required parameters:

- `columns`: Column names for the transaction data
- `checksum_cols`: Columns used for data validation
- `col_dims`: Column dimensions for parsing the PDF
- `dims`: Table dimensions for parsing the PDF
- `extra_pages`: Boundaries for extracting tables from the PDF
- `account_check`: Function to identify the account type
- `account_match`: Expected account type string for identification
- `account_number`: Function to extract the account number
- `statement_period`: Function to extract the statement date range (optional)

Refer to the provided example in `CONFIG.py` for guidance on setting these parameters.

## Contributing

If you'd like to contribute to this project, feel free to submit a pull request with your changes.

## License

This project is released under the MIT License. See `LICENSE` for more information.

## Disclaimer

This tool is for educational purposes only. Always ensure you have permission to access and process the bank statements you are working with. The author is not responsible for any misuse of this tool or any damages that may result from its use.
