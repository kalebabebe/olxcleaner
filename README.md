# OLX Cleaner

[![Build Status](https://github.com/openedx/olxcleaner/actions/workflows/ci.yml/badge.svg)](https://github.com/openedx/olxcleaner/actions/workflows/ci.yaml)
[![Coverage Status](https://codecov.io/gh/jolyonb/olxcleaner/branch/master/graphs/badge.svg)](https://codecov.io/gh/jolyonb/olxcleaner)

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

* [Error Listing](errors.md)
* [Wishlist](wishlist.md)
* [Vision](vision.md)
* [Changelog](changelog.md)
* [License](LICENSE)

## Installation

### Using PyPi

This package requires python 3.11 or later.

```bash
pip install olxcleaner
```

### Using Repository

```bash
git clone https://github.com/openedx/olxcleaner
cd olxcleaner
virtualenv -p python3
make requirements
```

You can run `pytest` to ensure that all tests are passing as expected.

## pretty-edx-cleaner

The `pretty-edx-cleaner` script provides an improved, color-coded output format for the validation results. It requires Python 3.9 or later and depends on the `edx-cleaner` tool being installed.

### Installation

The script is now included in the `olxcleaner` package and can be installed in two ways:

1. Using PyPi:
```bash
pip install olxcleaner
```

2. Using the repository:
```bash
git clone https://github.com/openedx/olxcleaner
cd olxcleaner
virtualenv -p python3
make requirements
```

The script will be available as `pretty-edx-cleaner` after installation.

### Usage

Basic usage:
```bash
cd /path/to/your/course
pretty-edx-cleaner
```

### Command Line Options

* `--major-only`: Show only major issues
* `--minor-only`: Show only minor issues
* `--fyi-only`: Show only FYI issues
* `--no-color`: Disable colored output

### Issue Categories

The script categorizes issues into three severity levels:

#### 🔴 Major Issues
* `GradingPolicyIssue`: Problems with the grading policy that could affect student grades
* `InvalidSetting`: Missing required course settings
* `PolicyNotFound`: Missing policy files essential for course operation

#### 🟡 Minor Issues
* `MissingFile`: Missing static files (images, documents, etc.)
* `DateOrdering`: Dates that are out of sequence
* `MissingDisplayName`: Components missing display names
* `UnexpectedTag`: Tag found in inappropriate location
* `InvalidHTML`: HTML syntax errors (formatting issues)

#### 🔵 FYI Issues
All other issues are considered FYI and will be displayed in the blue section.

### Output Format

The output is color-coded and organized into three sections:

* 🔴 MAJOR ISSUES: Critical problems that need immediate attention
* 🟡 MINOR ISSUES: Less critical problems that should be addressed
* 🔵 FYI: Informational issues that don't affect functionality

Each section groups issues by type and provides full file paths for easy navigation in IDEs.

### Exit Codes

The script uses the same exit codes as `edx-cleaner`:
* 0: No issues found or all issues are below the failure threshold
* 1: Issues found at or above the failure threshold

### Source Code

The script is now part of the `olxcleaner` package and can be found in the `olxcleaner/entries` directory. It's organized into several classes:

* `Issue`: Represents a single validation issue
* `IssueCollector`: Handles collecting and categorizing issues
* `OutputFormatter`: Manages the formatting of the output with colors and emojis

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
* `-i`: Specify a space-separated list of error names to ignore. See [Error Listing](errors.md).

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