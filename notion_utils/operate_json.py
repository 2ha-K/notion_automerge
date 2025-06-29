"""
notion_utils/json_output_utils.py

Purpose:
    Provides utility functions for printing and exporting Python dictionaries as JSON.
    Used for debugging, logging API responses, and exporting structured data in a human-readable format.

Features:
    - Pretty-printing JSON to terminal with indentation
    - Output JSON to specified file path or default file (`result.jason`)
    - Handles UTF-8 encoding and ensures file safety with context managers
    - Unified error logging through `log_error`

Used in:
    - Debugging Notion API responses
    - Manual inspection of intermediate data structures
    - CLI or GUI output during data sync/testing

Functions:
    - print_dict(): Pretty-prints a dictionary to the terminal
    - output_dict_to_path(): Saves a dictionary to a specified file path
    - output_dict(): Saves to a default file ('result.jason') in the working directory
"""

import json
import os

from notion_utils.log import log_error


def print_dict(response):
    """
    Print a dictionary as pretty-formatted JSON to the terminal.

    Args:
        response (dict): The dictionary to print.
    """
    try:
        # Output the dictionary to console in indented, sorted JSON format
        print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))
    except Exception as e:
        log_error("Failed to print JSON to terminal", e)


def output_dict_to_path(response, json_file_path):
    """
    Save a dictionary as a JSON file to a specified path.

    Args:
        response (dict): The data to save.
        json_file_path (str): The full path to write the JSON file.
    """
    try:
        print("Saving to:", json_file_path)
        # Write JSON data to file using UTF-8 encoding
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=4)  # open file as f
        # "with" ensures file is properly closed after writing
        # "w" creates file if it doesn't exist, or overwrites if it does
    except Exception as e:
        log_error(f"Failed to write JSON to path: {json_file_path}", e)


def output_dict(response):
    """
    Save a dictionary as a JSON file named 'result.json' in the current working directory.

    Args:
        response (dict): The data to save.
    """
    try:
        print("Current working directory:", os.getcwd())
        # Save to fixed file name in working dir (typo fixed from .jason to .json)
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=4)
    except Exception as e:
        log_error("Failed to write JSON to 'result.json'", e)
