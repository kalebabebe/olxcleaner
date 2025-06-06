# OLX Cleaner

[![Build Status](https://github.com/kalebabebe/olxcleaner/actions/workflows/ci.yml/badge.svg)](https://github.com/kalebabebe/olxcleaner/actions/workflows/ci.yml)
[![Coverage Status](https://codecov.io/gh/kalebabebe/olxcleaner/branch/master/graphs/badge.svg)](https://codecov.io/gh/kalebabebe/olxcleaner)

This library aims to perform two functions:

* Parse the XML code for an Open edX course, loading it into python objects.
* Validate the objects for errors.

Based on this, two scripts are provided that leverage the library:

* `edx-cleaner` constructs an error report, course tree and course statistics
* `edx-reporter` constructs a LaTeX file representation of the course structure
* `pretty-edx-cleaner` provides an improved, color-coded output format for validation results

Copyright (C) 2018-2019 Jolyon Bloomfield

Copyright (C) 2020-2024 Axim, Inc. and Contributors

## Links

* [Error Listing](docs/errors.md)
* [Wishlist](docs/wishlist.md)
* [Vision](docs/vision.md)
* [Changelog](CHANGELOG.md)
* [License](LICENSE)

## Installation

### Using PyPi

This package requires python 3.9 or later.

Install directly from the fork:
```bash
pip3 install --user git+https://github.com/kalebabebe/olxcleaner.git
```

After installation, verify the scripts are available:
```bash
which edx-cleaner
which pretty-edx-cleaner
```

### Using Repository

```bash
git clone https://github.com/kalebabebe/olxcleaner
cd olxcleaner
virtualenv -p python3
make requirements

# Install the package in development mode
pip3 install -e .

# Verify the scripts are installed
which edx-cleaner
which pretty-edx-cleaner
```

You can run `pytest` to ensure that all tests are passing as expected.

## pretty-edx-cleaner

The `pretty-edx-cleaner` script provides an improved, color-coded output format for the validation results. It requires Python 3.9 or later and depends on the `edx-cleaner` tool being installed.

### Installation

The script is included in the `olxcleaner` package and will be available after installation.

### Usage

Basic usage:
```bash
cd /path/to/your/course
pretty-edx-cleaner
```

Command line options:
* `--major-only`: Show only major issues
* `--minor-only`: Show only minor issues
* `--fyi-only`: Show only FYI issues
* `--no-color`: Disable colored output

For detailed documentation, including issue categories, output format, and best practices, see [pretty-edx-cleaner documentation](docs/pretty-edx-cleaner.md).

## edx-cleaner Usage

Used to validate OLX (edX XML) code. This is a very light wrapper around the olxcleaner library but exposes all of the functionality thereof.

Basic usage: run `edx-cleaner` in the directory of the course you want to validate.

Command-line options:

```text
edx-cleaner [-h]
            [-c COURSE]
            [-p {1,2,3,4,5,6,7,8}]
            [-t TREE] [-l {0,1,2,3,4}]
            [-q] [-e] [-s] [-S]
            [-f {0,1,2,3,4}]
            [-i IGNORE [IGNORE ...]]
```

* `-h`: Display help.
* `-c`: Specify the course file to analyze. If not specified, looks for `course.xml` in the current directory. If given a directory, looks for `course.xml` in that directory.
* `-p`: Specify the validation level you wish to analyze the course at:
  * 1: Load the course
  * 2: Load the policy and grading policy
  * 3: Validate url_names
  * 4: Merge policy data with the course, ensuring that all references are valid
  * 5: Validate the grading policy
  * 6: Have every object validate itself
  * 7: Parse the course for global errors
  * 8: Parse the course for detailed global errors (default)
* `-t TREE`: Specify a file to output the tree structure to.
* `-l`: Specify the depth level to output the tree structure to. Only used if the `-t` option is set. 0 = Course, 1 = Chapter, 2 = Sequential, 3 = Vertical, 4 = Content.
* `-q`: Quiet mode. Does not output anything to the screen.
* `-e`: Suppress error listing. Implied by `-q`.
* `-s`: Suppress summary of errors. Implied by `-q`.
* `-S`: Display course statistics (off by default). Overridden by `-q`.
* `-f`: Select the error level at which to exit with an error code. 0 = DEBUG, 1 = INFO, 2 = WARNING, 3 = ERROR (default), 4 = NEVER. The exit code is set to `1` if an error at the specified level or higher is present.
* `-i`: Specify a space-separated list of error names to ignore. See [Error Listing](docs/errors.md).

## edx-reporter Usage

The olxcleaner library includes modules that parse a course into Python objects. This can be useful if you want to scan a course to generate a report. We exploit this in `edx-reporter` to generate a LaTeX report of course structure.

Basic usage: run `edx-reporter` in the directory of the course you want to generate a report about.

Command-line options:

```text
edx-reporter.py [-h]
                [-c COURSE]
                [-u]
                [> latexfile.tex]
```

* `-h`: Display help.
* `-c`: Specify the course file to analyze. If not specified, looks for `course.xml` in the current directory. If given a directory, looks for `course.xml` in that directory.
* `-u`: Include url_names for verticals.
* `> latexfile.tex`: Output the report to a file.

If you get an error like ``Character cannot be encoded into LaTeX: U+FEFF - `'``, then you have some bad unicode in your `display_name` entries. Look through the LaTeX output for `{\bfseries ?}`, which is what that character is converted into.

Once you have generated a latex file, you can compile it into a PDF file by running `pdflatex latexfile.tex`. Note that the latex file can be modified with any text editor; its format should be self-explanatory.

## Library usage

The workhorse of the library is `olxcleaner.validate`, which validates a course in a number of steps.

```python
olxcleaner.validate(filename, steps=8, ignore=None, allowed_xblocks=None)
```

* `filename`: Pass in either the course directory or the path of `course.xml`
