# pretty-edx-cleaner Documentation

## Overview

The `pretty-edx-cleaner` script is a wrapper for the standard `edx-cleaner` tool that provides better organization and visualization of course validation issues. It categorizes and formats the output to make it easier to identify and fix problems in your edX course XML files.

## Features

* Categorizing issues by severity (Major, Minor, FYI)
* Grouping similar issue types together
* Providing full file paths for easier navigation in IDEs
* Adding additional context for specific issue types
* Using visual indicators and colors for quick scanning

## Requirements

* Python 3.9 or later
* `edx-cleaner` installed and functioning
* Terminal with color support (optional)

## Installation

The script is now included in the `olxcleaner` package and can be installed in two ways:

### Method 1: Using PyPi

```bash
pip install olxcleaner
```

### Method 2: Using Repository

```bash
git clone https://github.com/openedx/olxcleaner
cd olxcleaner
virtualenv -p python3
make requirements
```

The script will be available as `pretty-edx-cleaner` after installation.

## Source Code Organization

The script is organized in the `olxcleaner/entries` directory with the following structure:

* `pretty_edx_cleaner.py`: Main script file containing:
  * `Issue`: Class representing a single validation issue
  * `IssueCollector`: Class handling issue collection and categorization
  * `OutputFormatter`: Class managing output formatting with colors and emojis

## Usage

### Basic Usage

Navigate to your course directory and run:
```bash
cd /path/to/your/course
pretty-edx-cleaner
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--major-only` | Show only major issues |
| `--minor-only` | Show only minor issues |
| `--fyi-only` | Show only FYI issues |
| `--no-color` | Disable colored output |

### Examples

1. View all issues:
```bash
pretty-edx-cleaner
```

2. View only major issues:
```bash
pretty-edx-cleaner --major-only
```

3. View only minor issues:
```bash
pretty-edx-cleaner --minor-only
```

4. View only FYI issues:
```bash
pretty-edx-cleaner --fyi-only
```

5. Disable colored output:
```bash
pretty-edx-cleaner --no-color
```

## Issue Categories

### 🔴 Major Issues

These issues could significantly impact course functionality and student experience, and should be addressed immediately:

* `GradingPolicyIssue`: Problems with the grading policy that could affect student grades
* `InvalidSetting`: Missing required course settings
* `PolicyNotFound`: Missing policy files essential for course operation

### 🟡 Minor Issues

These issues may affect the visual appearance or cause minor functionality issues, but don't break core course functionality:

* `MissingFile`: Missing static files (images, documents, etc.)
* `DateOrdering`: Dates that are out of sequence
* `MissingDisplayName`: Components missing display names
* `UnexpectedTag`: Tag found in inappropriate location
* `InvalidHTML`: HTML syntax errors (formatting issues)

### 🔵 FYI Issues

These are informational issues that typically don't affect course functionality:

* `EmptyTag`: Tags that are unexpectedly empty
* `SettingOverride`: Settings being overridden in policy files
* `MissingURLName`: Components missing URL names
* Other misc. warnings

## Understanding the Output

The output is organized hierarchically:

1. **Severity sections** (Major, Minor, FYI)
2. Within each severity, **issue types** are grouped together
3. Within each issue type, **files** with those issues are listed

### Example Output

```
===== EDX CLEANER REPORT =====

🔴 MAJOR ISSUES
==================================================

▶ InvalidSetting (2 issues)
----------------------------------------
  📄 /Users/username/course/course/2023_Summer.xml:
    ❌ The tag <course url_name='2023_Summer' display_name='Course Title'> does not have the required setting 'course_image'.

🟡 MINOR ISSUES
==================================================

▶ MissingFile (4 issues)
----------------------------------------
  📄 /Users/username/course/html/27e31235b70540558b55ba21c24ba304.xml:
    ⚠️ The <html url_name='27e31235b70540558b55ba21c24ba304'> tag contains a reference to a missing static file: /static/Symphony_No.6__1st_movement_.mp3 [HTML source: /Users/username/course/html/27e31235b70540558b55ba21c24ba304.html]

🔵 FYI
==================================================

▶ EmptyTag (16 issues)
----------------------------------------
  📄 /Users/username/course/vertical/2c80e9c51bee4f8d860a2ae7539861ef.xml:
    ℹ️ The <vertical url_name='2c80e9c51bee4f8d860a2ae7539861ef' display_name='7.3.1)  Sample Content'> tag is unexpectedly empty

===== SUMMARY =====
🔴 Major issues: 5
🟡 Minor issues: 15
🔵 FYI: 26
Total files with issues: 37
```

### Special Features

1. **HTML Source Paths**: For HTML issues with missing static files, the script shows the path to the corresponding HTML file:
   ```
   [HTML source: /path/to/html/file.html]
   ```

2. **Color Coding**:
   - 🔴 Red: Major issues
   - 🟡 Yellow: Minor issues
   - 🔵 Blue: FYI issues

3. **File Navigation**: Full file paths are provided for easy navigation in IDEs

## Workflow: Fixing Course Issues

1. **Run the tool**:
   ```bash
   cd /path/to/your/course
   pretty-edx-cleaner
   ```

2. **Address Major Issues first**:
   * Focus on the 🔴 Major Issues section
   * Fix one issue type at a time
   * Use the full file paths to open files directly in your IDE

3. **Run the tool again** to verify your fixes

4. **Address Minor Issues next**:
   * Focus on the 🟡 Minor Issues section
   * For MissingFile issues, use the additional HTML source path

5. **Review FYI Issues**:
   * These typically don't require immediate attention
   * Fix them for better course quality and maintainability

## Exit Codes

The script uses the same exit codes as `edx-cleaner`:
* 0: No issues found or all issues are below the failure threshold
* 1: Issues found at or above the failure threshold

## Best Practices

1. Run the tool in the root directory of your edX course
2. Use the color-coded output to quickly identify issue severity
3. Start by addressing major issues first
4. Use the filtering options to focus on specific types of issues
5. Always re-run the tool after making changes
6. Use the HTML source paths to quickly locate files with missing static content 
