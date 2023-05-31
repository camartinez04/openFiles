# Docker Log Parser

This script parses docker logs and enables you to filter and colorize the log entries based on different criteria.

## Installation

This script requires Python 3 and a few additional packages:

- pandas
- re
- colorama
- argparse

Install these dependencies with pip:

```bash
pip install pandas colorama argparse
```

## Usage


Command line arguments:

`--file`: Path to the log file to process. This argument is required.

`--info`: Display info logs.

`--error`: Display error logs.

`--warning`: Display warning logs.

`--aws`: Display AWS logs.

`--storage`: Display storage logs.

`--cloudsnap`: Display cloudsnap backup logs.

`--all`: Display all logs.

For example, to process the log file at /path/to/log/file, and print info logs, error logs, and AWS logs, use:

```bash
python log_docker.py --file /path/to/log/docker.out --aws
```

This will also create a csv file named 'output.csv' in the current directory containing all the parsed logs.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

You can modify and extend this README.md file according to your project needs. The README file should provide all the necessary information for other developers to understand what your project does, how to install it, and how to use it.

