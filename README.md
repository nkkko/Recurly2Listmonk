# Recurly2Listmonk

## Overview

The `Recurly2Listmonk` project is a script designed to process CSV files exported from Recurly, filter and clean the data, and prepare it for import into [Listmonk](https://github.com/knadh/listmonk), a high-performance, self-hosted newsletter and mailing list manager.

This script consolidates multiple CSV files, extracts relevant information, and provides options to split the resulting file into multiple chunks for easier management and import.

## Features

- **CSV File Consolidation**: Merges multiple Recurly export CSV files into a single, cohesive file.
- **Data Cleaning**: Handles edge cases in data, ensuring names are correctly parsed and attribute fields are not inserted with `NaN` values.
- **Progress Tracking**: Implements a progress bar using `tqdm` to track the processing of files.
- **File Splitting**: Optionally splits the resulting CSV into multiple smaller files based on user input.

## Requirements

- Python 3.x
- Pandas
- Tqdm
- Numpy
- Json

Install the required Python libraries using:
```sh
pip install pandas tqdm numpy
```

## File Structure

```
Recurly2Listmonk/
│
├── export/                     # Directory containing input CSV files
│   ├── recurly_export_1.csv
│   ├── recurly_export_2.csv
│   └── ...
├── combined-recurly-export.csv # Output consolidated CSV file (if split is not used)
├── script.py                   # Main script file
└── README.md                   # Project documentation
```

## Usage

1. **Directory Setup**:
    - Ensure your Recurly export CSV files are placed in the `export` directory.

2. **Running the Script**:
    - Navigate to the directory containing `script.py`.
    - Run the script using Python:

    ```sh
    python script.py [--split <number_of_files>]
    ```

    - **Arguments**:
      - `--split`: Optional argument to specify the number of resulting CSV files. If omitted, the script will produce a single consolidated file.

    **Example**:
    ```sh
    python script.py --split 3
    ```

## Script Explanation

### Libraries

- **os**: For directory and path handling.
- **pandas**: For CSV file manipulation.
- **json**: For creating JSON attribute structures.
- **tqdm**: For displaying progress bars.
- **argparse**: For parsing command-line arguments.
- **numpy**: For handling NaN values.

### Key Functions

1. **`clean_name(first_name, last_name)`**:
    - Cleans and combines first and last names.

2. **`generate_attributes(row)`**:
    - Generates a JSON structure for the attributes while excluding any fields that contain `NaN` values.

3. **`split_dataframe(df, num_splits)`**:
    - Splits a DataFrame into the specified number of smaller DataFrames.

4. **`save_splitted_files(dfs, base_filename)`**:
    - Saves the smaller DataFrames into individual CSV files.

5. **`process_files(directory, split=None)`**:
    - Main function to process files in the `export` directory, perform data cleaning, and generate the consolidated CSV file. Handles file splitting if the `split` argument is provided.

## Contributing

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new features'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.