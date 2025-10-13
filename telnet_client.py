#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Telnet Client for Windows
Alternative to telnet command when not available
Created by Echo for Daddy's convenience!

GitHub Repository: https://github.com/KT-Society/projekt_echo
"""

import socket
import sys
import time
import codecs

# Fix Unicode encoding on Windows
if sys.platform.startswith('win'):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def telnet_connect(host, port, timeout=5):
    """
    Simple telnet-like connection test
    Returns True if connection successful, False otherwise
    """
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Try to connect
        result = sock.connect_ex((host, port))
        sock.close()
        
        return result == 0
        
    except Exception as e:
        return False

def main():
    """Main function for command line usage"""
    if len(sys.argv) != 3:
        print("Usage: python telnet_client.py <host> <port>")
        print("Example: python telnet_client.py 127.0.0.1 5000")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    print(f"Testing connection to {host}:{port}...")
    
    if telnet_connect(host, port):
        print(f"✅ Connection to {host}:{port} successful!")
        sys.exit(0)
    else:
        print(f"❌ Connection to {host}:{port} failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()