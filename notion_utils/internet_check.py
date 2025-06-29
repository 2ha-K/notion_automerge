"""
notion_utils/network/check_internet_connection.py

Purpose:
    Provides a simple utility to check whether an internet connection is available.
    It attempts to connect to a well-known DNS server (default: 8.8.8.8) over TCP port 53.

Use Cases:
    - Before making API requests to Notion or other cloud services
    - To provide user-friendly error handling when offline
    - As a lightweight pre-flight check in CLI or GUI applications

Function:
    - check_internet_connection(): Returns True if an outbound connection can be established; otherwise False
"""

import socket


def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Check if there is an active internet connection by trying to connect to a known host.

    Args:
        host (str): The IP address to connect to. Default is Google's public DNS server (8.8.8.8).
        port (int): The port number to use for the connection. Default is 53 (DNS service).
        timeout (int): The number of seconds to wait before giving up the connection attempt.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
