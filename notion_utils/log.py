import traceback
from datetime import datetime

RESET = "\033[0m"
RED = "\033[91m"
start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"{RED}{start_timestamp}{RESET}")


def log_print_green(text):
    # Print text in bright green (for success messages)
    GREEN = "\033[92m"  # Bright Green

    print(f"{GREEN}{text}{RESET}")


def log_print_yellow(text):
    # Print text in bright yellow (for warnings or neutral logs)
    YELLOW = "\033[93m"  # Bright Yellow
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
    print(f"{RED}[{timestamp}] [ERROR] {message}{RESET}")
    if exception:
        # Print exception details if provided
        print(f"{RED}[{timestamp}] [DETAIL] {exception}{RESET}")


def log_error_with_traceback(exception):
    """
    Prints a traceback when an exception occurs.
    """
    if exception:
        traceback.print_exception(type(exception), exception, exception.__traceback__)
