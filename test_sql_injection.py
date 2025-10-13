#!/usr/bin/env python3
"""
Test script for SQL Injection in Hacking Game
"""

import sys
import os
sys.path.append('.')

from hacking_game import HackingGame

def test_sql_injection():
    """Test SQL injection functionality"""
    print("🔍 Testing SQL Injection in Hacking Game...")
    
    # Create game instance
    game = HackingGame()
    
    # Test curl command
    curl_cmd = 'curl -X POST -d "username=admin\' UNION SELECT 1,2,3,4,5,6-- &password=test" http://127.0.0.1:5000/login'
    print(f"Testing: {curl_cmd}")
    
    # Debug: Test the regex parsing
    import re
    data_match = re.search(r'-d\s+[\'"]([^\'"]*(?:\\.[^\'"]*)*)[\'"]', curl_cmd)
    if data_match:
        data = data_match.group(1)
        data = data.replace('\\"', '"').replace("\\'", "'")
        print(f"Parsed data: {data}")
        
        # Test URL parsing
        import urllib.parse
        parsed_data = urllib.parse.parse_qs(data, keep_blank_values=True)
        print(f"Parsed query: {parsed_data}")
    
    # Execute curl command
    result = game.execute_curl_command(curl_cmd)
    print(f"Server response: {result}")
    
    # Check if it's successful
    success = game.check_level_success(3, result or "", curl_cmd)
    print(f"Success: {success}")
    
    return success

if __name__ == "__main__":
    test_sql_injection()
