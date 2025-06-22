import os
import traceback
from datetime import datetime

# Color control code
RESET = "\033[0m"
RED = "\033[91m"

# Setting log path
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

INFO_LOG_PATH = os.path.join(LOG_DIR, "info.log")
ERROR_LOG_PATH = os.path.join(LOG_DIR, "error.log")


def log_print_green(text):
    # Print text in bright green (for success messages)
    GREEN = "\033[92m"  # Bright Green
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _write_to_file(INFO_LOG_PATH, f"[{timestamp}] [INFO] {text}")
    print(f"{GREEN}{text}{RESET}")


def log_print_yellow(text):
    # Print text in bright yellow (for warnings or neutral logs)
    YELLOW = "\033[93m"  # Bright Yellow
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _write_to_file(INFO_LOG_PATH, f"[{timestamp}] [INFO] {text}")
    print(f"{YELLOW}{text}{RESET}")


def log_error(message, exception=None):
    """
    Logs an error message with a timestamp to the console.

    Args:
        message (str): Short description of the error.
        exception (Exception, optional): Optional exception object for detailed output.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Print main error message with red color
    _write_to_file(ERROR_LOG_PATH, f"[{timestamp}] [ERROR] {message}")
    print(f"{RED}[{timestamp}{RESET}] [ERROR] {message}")
    if exception:
        # Print exception details if provided
        _write_to_file(ERROR_LOG_PATH, f"[{timestamp}] [DETAIL] {exception}")
        print(f"{RED}[{timestamp}{RESET}] [DETAIL] {exception}")


def log_error_with_traceback(exception):
    """
    Prints a traceback when an exception occurs.
    """
    if exception:
        traceback_str = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        print(f"{RED}{traceback_str}{RESET}")
        _write_to_file(ERROR_LOG_PATH, traceback_str)


def _write_to_file(filepath, text):
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def write_log_header():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    separator = "=" * 50
    header = f"\n{separator}\nNew Run at {now}\n{separator}"
    _write_to_file(INFO_LOG_PATH, header)
    _write_to_file(ERROR_LOG_PATH, header)
    print(f"{RED}{header}{RESET}")
