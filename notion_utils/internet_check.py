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
