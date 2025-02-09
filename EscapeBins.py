#!/usr/bin/python3

import argparse
import json
import os
import datetime
from string import Template
from jinja2 import Template as JinjaTemplate

from colorama import Fore, Style
from pygments import highlight, formatters, lexers

version = "6.0.0"

# Banner for the script
banner = f'''
{Fore.RED + Style.BRIGHT}   ____                      {Style.RESET_ALL + Fore.LIGHTBLACK_EX}___  _        
{Fore.RED + Style.BRIGHT}  / __/__ _______ ____  ___ {Style.RESET_ALL + Fore.LIGHTBLACK_EX}/ _ )(_)__  ___
{Fore.RED + Style.BRIGHT} / _/(_-</ __/ _ `/ _ \/ -_){Style.RESET_ALL + Fore.LIGHTBLACK_EX} _  / / _ \(_-<
{Fore.RED + Style.BRIGHT}/___/___/\__/\_,_/ .__/\__/{Style.RESET_ALL + Fore.LIGHTBLACK_EX}____/_/_//_/___/    {version}
{Fore.RED + Style.BRIGHT}                /_/                        
'''

# Path to the JSON file
data_file = "bins_json/test.json"

# Templates for styled output
info = Template(Style.BRIGHT + '[ ' + Fore.GREEN + '*' + Fore.RESET + ' ] ' + Style.RESET_ALL + '$text')
fail = Template(Style.BRIGHT + '[ ' + Fore.RED + '-' + Fore.RESET + ' ] ' + Style.RESET_ALL + '$text')
title = Template(
    '\n' + Style.BRIGHT + Fore.LIGHTBLACK_EX + '---------- [ ' + Fore.RED + '$title' + Fore.LIGHTBLACK_EX + ' ] ----------' + Style.RESET_ALL + '\n'
)
description = Template(Style.DIM + '# ' + '$description' + Style.RESET_ALL)
divider = '\n' + Style.BRIGHT + ' - ' * 10 + Style.RESET_ALL + '\n'

class GTFOBinsReport:
    def __init__(self):
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stats = {}

    def generate_statistics(self, binary_results):
        """
        Generate statistics from analysis results
        """
        total_binaries = len(binary_results)
        categories = {}
        total_functions = 0

        for binary, data in binary_results.items():
            for category, functions in data['functions'].items():
                categories[category] = categories.get(category, 0) + len(functions)
                total_functions += len(functions)

        self.stats = {
            'total_binaries': total_binaries,
            'total_functions': total_functions,
            'categories': categories
        }

        return self.stats

    def generate_markdown_report(self, binary_results):
        """
        Generate a Markdown report
        """
        stats = self.generate_statistics(binary_results)

        md_content = f"""# GTFOBins Analysis Report
Generated on: {self.current_time}

## Statistics
- Total Binaries: {stats['total_binaries']}
- Total Functions: {stats['total_functions']}
- Categories: {len(stats['categories'])}

## Category Distribution
{', '.join(f'{k}: {v}' for k, v in stats['categories'].items())}

## Detailed Analysis
"""

        for binary, data in binary_results.items():
            md_content += f"\n### Binary: {binary}\n"
            if 'description' in data:
                md_content += f"_{data['description']}_\n"

            for category, functions in data['functions'].items():
                md_content += f"\n#### {category.upper()}\n"
                for func in functions:
                    if 'description' in func:
                        md_content += f"\n_{func['description']}_\n"
                    md_content += f"\n```bash\n{func['code']}\n```\n"

        return md_content

class CustomHelpFormatter(argparse.HelpFormatter):
    def format_help(self):
        help_text = super().format_help()

        # Convert sections to uppercase
        help_text = help_text.replace("usage: ", "Usage: ")
        help_text = help_text.replace("positional arguments:", "Positional Arguments:")
        help_text = help_text.replace("options:", "Options:")
        help_text = help_text.replace("show this help message and exit", "Show this help message and exit\n")
        help_text += "\n"

        return help_text

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        usage="python3 gtfo.py [binary]",
        description="Command-line tool for searching and displaying GTFOBins entries.",
        formatter_class=CustomHelpFormatter
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0',
        help="Show program's version number and exit"
    )

    parser.add_argument(
        'binary',
        metavar='[binary]',
        action='store',
        nargs='?',
        help='Specifies the binary file to search for'
    )

    parser.add_argument(
        '-l', '--list',
        nargs='?',
        const='all',
        help='List all available binaries. Optionally specify a letter to filter binaries'
    )

    parser.add_argument(
        '-r', '--report',
        nargs='+',
        help='Generate a markdown report for specified binaries'
    )

    parser.add_argument(
        '--output', '-o',
        default='gtfobins_report.md',
        help='Output filename for the report'
    )

    return parser.parse_args()

def list_available_binaries(filter_char=None):
    """
    List all available binaries grouped alphabetically.
    Filter by starting character if filter_char is provided.
    """
    if os.path.isfile(data_file):
        with open(data_file) as source:
            data = json.load(source)

        binaries = sorted(data.keys())

        # Group binaries by their first character
        grouped_binaries = {}

        # Handle numbers (0-9)
        numbers = [b for b in binaries if b[0].isdigit()]
        if numbers:
            grouped_binaries['0-9'] = numbers

        # Handle letters (a-z)
        for binary in binaries:
            if binary[0].isalpha():
                first_char = binary[0].lower()
                if first_char not in grouped_binaries:
                    grouped_binaries[first_char] = []
                grouped_binaries[first_char].append(binary)

        # If filter_char is provided, only show binaries starting with that character
        if filter_char:
            filter_char = filter_char.lower()
            if filter_char.isdigit():
                filter_char = '0-9'
            if filter_char in grouped_binaries:
                total_binaries = len(grouped_binaries[filter_char])
                print(info.safe_substitute(text=f"Available binaries starting with '{filter_char}' {Fore.LIGHTBLACK_EX + Style.BRIGHT}({Fore.RED + Style.BRIGHT}{total_binaries}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX + Style.BRIGHT}){Style.RESET_ALL}:\n"))

                # Calculate column width for the filtered group
                column_width = max(len(b) for b in grouped_binaries[filter_char]) + 2
                max_columns = min(4, max(1, os.get_terminal_size().columns // column_width))

                # Print group header
                if filter_char == '0-9':
                    print(f"{Style.BRIGHT}{Fore.LIGHTBLACK_EX}({Style.BRIGHT}{Fore.RED}0-9{Style.BRIGHT}{Fore.LIGHTBLACK_EX}):{Style.RESET_ALL}\n")
                else:
                    print(f"{Style.BRIGHT}{Fore.LIGHTBLACK_EX}({Style.BRIGHT}{Fore.RED}{filter_char}{Style.BRIGHT}{Fore.LIGHTBLACK_EX}):{Style.RESET_ALL}\n")

                # Print binaries in columns
                group_binaries = grouped_binaries[filter_char]
                for i in range(0, len(group_binaries), max_columns):
                    row = group_binaries[i:i + max_columns]
                    print('  ' + '  '.join(f"{b:<{column_width}}" for b in row))
                print()
            else:
                print(fail.safe_substitute(text=f"No binaries found starting with '{filter_char}'"))
        else:
            # Original behavior for listing all binaries
            total_binaries = len(binaries)
            print(info.safe_substitute(text=f"Available binaries {Fore.LIGHTBLACK_EX + Style.BRIGHT}({Fore.RED + Style.BRIGHT}{total_binaries}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX + Style.BRIGHT}){Style.RESET_ALL}:\n"))

            # Calculate column width
            column_width = max(len(b) for b in binaries) + 2
            max_columns = min(4, max(1, os.get_terminal_size().columns // column_width))

            # Print all groups
            for group in sorted(grouped_binaries.keys()):
                if group == '0-9':
                    print(f"{Style.BRIGHT}{Fore.LIGHTBLACK_EX}({Style.BRIGHT}{Fore.RED}0-9{Style.BRIGHT}{Fore.LIGHTBLACK_EX}):{Style.RESET_ALL}")
                else:
                    print(f"{Style.BRIGHT}{Fore.LIGHTBLACK_EX}({Style.BRIGHT}{Fore.RED}{group}{Style.BRIGHT}{Fore.LIGHTBLACK_EX}):{Style.RESET_ALL}")

                group_binaries = grouped_binaries[group]
                print()

                for i in range(0, len(group_binaries), max_columns):
                    row = group_binaries[i:i + max_columns]
                    print('  ' + '  '.join(f"{b:<{column_width}}" for b in row))
                print()

        print(info.safe_substitute(text="Bad SUIDs, good exploits.\n"))
    else:
        print(fail.safe_substitute(text="Data file not found."))

def generate_markdown_report(args):
    """
    Generate a markdown report for specified binaries.
    """
    report_generator = GTFOBinsReport()

    if os.path.isfile(data_file):
        with open(data_file) as source:
            data = json.load(source)

        results = {}
        for binary in args.report:
            if binary in data:
                results[binary] = data[binary]
            else:
                print(fail.safe_substitute(text=f"Binary not found: {binary}"))

        if results:
            output = report_generator.generate_markdown_report(results)
            output_file = args.output if args.output.endswith('.md') else f"{args.output}.md"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)

            print(info.safe_substitute(text=f"Markdown report generated: {output_file}"))
    else:
        print(fail.safe_substitute(text="Data file not found."))

def main(binary):
    """
    Main function to load and display information about the specified binary.
    """
    if os.path.isfile(data_file):
        print(info.safe_substitute(text="Supplied binary: " + binary))
        print(info.safe_substitute(text="Please wait, loading data ... "))

        with open(data_file) as source:
            data = json.load(source)

        if binary in data:
            json_data = data[binary]
            if 'description' in json_data:
                print('\n' + description.safe_substitute(description=json_data['description']))

            for category, functions in json_data['functions'].items():
                print(title.safe_substitute(title=category.upper()))
                index = 0
                for function in functions:
                    index = index + 1
                    if 'description' in function:
                        print(description.safe_substitute(description=function['description']) + '\n')
                    print(highlight(function['code'], lexers.BashLexer(),
                                    formatters.TerminalTrueColorFormatter(style='igor')).strip())
                    if index != len(functions):
                        print(divider)

            print('\n' + info.safe_substitute(text="Bad SUIDs, good exploits.\n"))
        else:
            print(fail.safe_substitute(text="Sorry, couldn't find anything for " + binary + "\n"))
    else:
        print(fail.safe_substitute(text="Data file not found."))

if __name__ == '__main__':
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print the banner in bold and light black color
    print(Style.BRIGHT + Fore.LIGHTBLACK_EX + banner + Style.RESET_ALL)

    # Parse command-line arguments
    args = parse_args()

    # If the list option is provided
    if args.list is not None:
        if args.list == 'all':
            list_available_binaries()
        else:
            list_available_binaries(args.list)
    # If report generation is requested
    elif args.report:
        generate_markdown_report(args)
    # Otherwise if a binary is provided, proceed with main function
    elif args.binary:
        main(binary=args.binary)
    # If no arguments are provided, show help
    else:
        parser = argparse.ArgumentParser(
            usage="python3 gtfo.py [binary]",
            description="Command-line tool for searching and displaying GTFOBins entries.",
            formatter_class=CustomHelpFormatter
        )
        parser.print_help()