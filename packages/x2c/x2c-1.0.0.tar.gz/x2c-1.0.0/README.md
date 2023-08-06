# x2c - XML to CSV
A simple cli app to convert XML files to CSV, with user-defined columns.

## Usage
It takes three arguments:
```
    -i --infile     input file
    -o --outfile    output file
    -c --column     columns
```

Example:
```
    x2c -i example.xml -o example.csv -c col1,col2,col3
```

The column names must match the xml tags.


## Installation

The script can be installed with `pip`:
```
    pip install x2c
```

Or from source (deprecated):
```
    python -m setup.py install
```

