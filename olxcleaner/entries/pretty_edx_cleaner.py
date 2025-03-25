#!/usr/bin/env python3.9
"""
pretty_edx_cleaner.py

A wrapper for edx-cleaner that provides improved organization and visualization
of course validation issues. It categorizes and formats the output to make it
easier to identify and fix problems in edX course XML files.
"""

import subprocess
import re
import os
import argparse
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

# Define issue severity categories
MAJOR_ISSUES = [
    'GradingPolicyIssue',  # Affects grading
    'InvalidSetting',      # Missing required course settings
    'PolicyNotFound'       # Missing policy file - critical issue
]

MINOR_ISSUES = [
    'MissingFile',         # Missing static files 
    'DateOrdering',        # Date ordering issues
    'MissingDisplayName',  # Missing display names (visual issue)
    'UnexpectedTag',       # Tag found in inappropriate location
    'InvalidHTML'          # HTML syntax errors (formatting issues)
]

# All other issues are considered FYI

class Issue:
    """Represents a single validation issue."""
    def __init__(self, severity: str, issue_type: str, file_path: str, message: str, extra_info: str = ""):
        self.severity = severity
        self.issue_type = issue_type
        self.file_path = file_path
        self.message = message
        self.extra_info = extra_info

    def __str__(self) -> str:
        return f"{self.severity} {self.issue_type} ({self.file_path}): {self.message}{self.extra_info}"

class IssueCollector:
    """Collects and categorizes validation issues."""
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.issues_by_file: Dict[str, List[Issue]] = defaultdict(list)

    def add_issue(self, severity: str, issue_type: str, file_path: str, message: str, extra_info: str = "") -> None:
        """Add a new issue to the collector."""
        full_path = os.path.join(self.base_path, file_path)
        
        # Handle policy files separately
        if file_path in ['policy.json', 'grading_policy.json']:
            full_path = self._find_policy_file(file_path)
        
        # Extract additional navigation info for html files
        if "html" in file_path and issue_type == "MissingFile":
            extra_info = self._get_html_source_info(file_path, message)
        
        issue = Issue(severity, issue_type, full_path, message, extra_info)
        self.issues_by_file[full_path].append(issue)

    def _find_policy_file(self, file_path: str) -> str:
        """Find policy file in the policies directory."""
        for root, _, files in os.walk(os.path.join(self.base_path, 'policies')):
            if file_path in files:
                return os.path.join(root, file_path)
        return os.path.join(self.base_path, file_path)

    def _get_html_source_info(self, file_path: str, message: str) -> str:
        """Get HTML source file information for missing file issues."""
        url_name_match = re.search(r"url_name='([^']+)'", message)
        if url_name_match:
            url_name = url_name_match.group(1)
            file_type = file_path.split('/')[-2]  # Gets 'html' from the path
            html_file = f"{file_type}/{url_name}.html"
            potential_html_path = os.path.join(self.base_path, html_file)
            if os.path.exists(potential_html_path):
                return f" [HTML source: {potential_html_path}]"
        return ""

    def get_issues_by_level(self, level: str) -> Dict[str, List[Issue]]:
        """Get issues grouped by type within a severity level."""
        result = defaultdict(list)
        for file_path, issues in self.issues_by_file.items():
            for issue in issues:
                if self.get_issue_level(issue) == level:
                    result[issue.issue_type].append(issue)
        return result

    @staticmethod
    def get_issue_level(issue: Issue) -> str:
        """Determine the severity level of an issue."""
        if issue.issue_type in MAJOR_ISSUES:
            return 'MAJOR'
        elif issue.issue_type in MINOR_ISSUES:
            return 'MINOR'
        elif issue.severity == 'ERROR':
            return 'MAJOR'
        elif issue.severity == 'WARNING':
            return 'MINOR'
        else:
            return 'FYI'

class OutputFormatter:
    """Formats the output with colors and emojis."""
    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors
        if use_colors:
            self.RED = '\033[91m'
            self.YELLOW = '\033[93m'
            self.BLUE = '\033[94m'
            self.BOLD = '\033[1m'
            self.RESET = '\033[0m'
        else:
            self.RED = self.YELLOW = self.BLUE = self.BOLD = self.RESET = ''

    def format_header(self) -> str:
        """Format the report header."""
        return f"\n{self.BOLD}===== EDX CLEANER REPORT ====={self.RESET}\n"

    def format_section_header(self, level: str) -> str:
        """Format a section header."""
        color = {'MAJOR': self.RED, 'MINOR': self.YELLOW, 'FYI': self.BLUE}[level]
        emoji = {'MAJOR': '🔴', 'MINOR': '🟡', 'FYI': '🔵'}[level]
        return f"\n{color}{emoji} {level} ISSUES{self.RESET}\n" + "="*50

    def format_issue_type_header(self, issue_type: str, count: int, level: str) -> str:
        """Format an issue type header."""
        color = {'MAJOR': self.RED, 'MINOR': self.YELLOW, 'FYI': self.BLUE}[level]
        return f"\n{color}▶ {issue_type}{self.RESET} ({count} issues)\n" + "-"*40

    def format_issue(self, file_path: str, message: str, extra_info: str, level: str) -> str:
        """Format a single issue."""
        color = {'MAJOR': self.RED, 'MINOR': self.YELLOW, 'FYI': self.BLUE}[level]
        icon = {'MAJOR': '❌', 'MINOR': '⚠️', 'FYI': 'ℹ️'}[level]
        return f"  📄 {file_path}:\n    {icon} {message}{extra_info}\n"

    def format_summary(self, major_count: int, minor_count: int, fyi_count: int, total_files: int) -> str:
        """Format the summary section."""
        return (
            f"\n{self.BOLD}===== SUMMARY ====={self.RESET}\n"
            f"{self.RED}🔴 Major issues: {major_count}{self.RESET}\n"
            f"{self.YELLOW}🟡 Minor issues: {minor_count}{self.RESET}\n"
            f"{self.BLUE}🔵 FYI: {fyi_count}{self.RESET}\n"
            f"Total files with issues: {total_files}"
        )

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Improved edX course validator output formatter')
    parser.add_argument('--major-only', action='store_true', help='Show only major issues')
    parser.add_argument('--minor-only', action='store_true', help='Show only minor issues')
    parser.add_argument('--fyi-only', action='store_true', help='Show only FYI issues')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    return parser.parse_args()

def main() -> int:
    """Main entry point for the script."""
    args = parse_arguments()
    formatter = OutputFormatter(use_colors=not args.no_color)
    collector = IssueCollector(os.getcwd())

    # Run edx-cleaner and capture output
    result = subprocess.run(['edx-cleaner'], capture_output=True, text=True)
    output = result.stdout

    # Parse the output
    pattern = r'(WARNING|ERROR) (\w+) \((.*?)\): (.*)'
    for line in output.split('\n'):
        match = re.match(pattern, line)
        if match:
            severity, issue_type, file_path, message = match.groups()
            collector.add_issue(severity, issue_type, file_path, message)

    # Print report
    print(formatter.format_header())

    # Count issues
    major_count = 0
    minor_count = 0
    fyi_count = 0

    # Print major issues
    if not args.minor_only and not args.fyi_only:
        print(formatter.format_section_header('MAJOR'))
        major_issues = collector.get_issues_by_level('MAJOR')
        if not major_issues:
            print("  No major issues found.")
        else:
            for issue_type, issues in sorted(major_issues.items()):
                print(formatter.format_issue_type_header(issue_type, len(issues), 'MAJOR'))
                for issue in sorted(issues, key=lambda x: os.path.basename(x.file_path)):
                    major_count += 1
                    print(formatter.format_issue(issue.file_path, issue.message, issue.extra_info, 'MAJOR'))

    # Print minor issues
    if not args.major_only and not args.fyi_only:
        print(formatter.format_section_header('MINOR'))
        minor_issues = collector.get_issues_by_level('MINOR')
        if not minor_issues:
            print("  No minor issues found.")
        else:
            for issue_type, issues in sorted(minor_issues.items()):
                print(formatter.format_issue_type_header(issue_type, len(issues), 'MINOR'))
                for issue in sorted(issues, key=lambda x: os.path.basename(x.file_path)):
                    minor_count += 1
                    print(formatter.format_issue(issue.file_path, issue.message, issue.extra_info, 'MINOR'))

    # Print FYI issues
    if not args.major_only and not args.minor_only:
        print(formatter.format_section_header('FYI'))
        fyi_issues = collector.get_issues_by_level('FYI')
        if not fyi_issues:
            print("  No informational issues found.")
        else:
            for issue_type, issues in sorted(fyi_issues.items()):
                print(formatter.format_issue_type_header(issue_type, len(issues), 'FYI'))
                for issue in sorted(issues, key=lambda x: os.path.basename(x.file_path)):
                    fyi_count += 1
                    print(formatter.format_issue(issue.file_path, issue.message, issue.extra_info, 'FYI'))

    # Print summary
    print(formatter.format_summary(major_count, minor_count, fyi_count, len(collector.issues_by_file)))

    return result.returncode

if __name__ == '__main__':
    exit(main()) 