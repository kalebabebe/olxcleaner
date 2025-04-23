# pretty-edx-cleaner Documentation

## Overview

The `pretty-edx-cleaner` script is a wrapper for the standard `edx-cleaner` tool that provides better organization and visualization of course validation issues. It categorizes and formats the output to make it easier to identify and fix problems in your edX course XML files.

## Requirements and Installation

* Python 3.9 or later
* Terminal with color support (optional)
* Install directly from the fork: `pip3 install --user git+https://github.com/kalebabebe/olxcleaner.git`

After installation, verify the script is available:
```bash
which pretty-edx-cleaner
```

If the script is not found, you may need to add the Python scripts directory to your PATH:
```bash
# For user installs (pip install --user)
export PATH="$HOME/.local/bin:$PATH"

# For system installs
export PATH="/usr/local/bin:$PATH"
```

For development installation:
```bash
git clone https://github.com/kalebabebe/olxcleaner
cd olxcleaner
virtualenv -p python3
make requirements
pip3 install -e .  # Install in development mode
```

The script is included in the `olxcleaner` package and will be available after installation.

## Usage

Basic usage:
```bash
cd /path/to/your/course
pretty-edx-cleaner [options]
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--major-only` | Show only major issues |
| `--minor-only` | Show only minor issues |
| `--fyi-only` | Show only FYI issues |
| `--no-color` | Disable colored output |

## Issue Categories

### 🔴 Major Issues
Critical problems that need immediate attention:
* `GradingPolicyIssue`: Problems with the grading policy that could affect student grades
* `InvalidSetting`: Missing required course settings
* `PolicyNotFound`: Missing policy files essential for course operation

### 🟡 Minor Issues
Issues that may affect appearance or cause minor functionality issues:
* `MissingFile`: Missing static files (images, documents, etc.)
* `DateOrdering`: Dates that are out of sequence
* `MissingDisplayName`: Components missing display names
* `UnexpectedTag`: Tag found in inappropriate location
* `InvalidHTML`: HTML syntax errors (formatting issues)

### 🔵 FYI Issues
Informational issues that typically don't affect functionality:
* `EmptyTag`: Tags that are unexpectedly empty
* `SettingOverride`: Settings being overridden in policy files
* `MissingURLName`: Components missing URL names
* Other misc. warnings

## Output Format

The output is organized hierarchically with color coding:
* 🔴 Red: Major issues that need immediate attention
* 🟡 Yellow: Minor issues that should be addressed
* 🔵 Blue: Informational issues

Special features:
* Full file paths for easy IDE navigation
* HTML source paths for static file issues
* Issue grouping by type and severity
* Summary statistics

### Example Output
```
===== EDX CLEANER REPORT =====

🔴 MAJOR ISSUES
==================================================
▶ InvalidSetting (2 issues)
  📄 course/2023_Summer.xml:
    ❌ The tag <course url_name='2023_Summer'> does not have 'course_image'.

🟡 MINOR ISSUES
==================================================
▶ MissingFile (1 issue)
  📄 html/intro.xml:
    ⚠️ Missing static file: image.jpg [HTML source: html/intro.html]

===== SUMMARY =====
🔴 Major issues: 2
🟡 Minor issues: 1
🔵 FYI: 0
Total files with issues: 2
```

## Best Practices

1. Run in course root directory
2. Address major issues first
3. Use filtering options to focus on specific issues
4. Re-run after making changes
5. Use HTML source paths to locate missing files

## Technical Details

The script is organized in `olxcleaner/entries/pretty_edx_cleaner.py` with three main classes:
* `Issue`: Represents a single validation issue
* `IssueCollector`: Handles issue collection and categorization
* `OutputFormatter`: Manages output formatting

Exit codes match `edx-cleaner`:
* 0: No issues or all below failure threshold
* 1: Issues at or above failure threshold 
