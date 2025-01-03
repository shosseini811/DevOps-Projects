#!/usr/bin/env python3
import subprocess
import sys
import os
import argparse

def run_unit_tests():
    """Run the unit tests"""
    print("Running unit tests...")
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    return result.returncode

def run_load_tests(host="http://localhost:5001"):
    """Run the load tests"""
    print(f"Starting load tests against {host}")
    print("Access the Locust web interface at http://localhost:8089")
    result = subprocess.run(["locust", "-f", "tests/test_load.py", "--host", host], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    return result.returncode

def main():
    parser = argparse.ArgumentParser(description="Run tests for User Management System")
    parser.add_argument("--type", choices=["unit", "load", "all"], default="all",
                      help="Type of tests to run (unit, load, or all)")
    parser.add_argument("--host", default="http://localhost:5001",
                      help="Host to run load tests against")
    
    args = parser.parse_args()
    
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    exit_code = 0
    
    if args.type in ["unit", "all"]:
        unit_result = run_unit_tests()
        if unit_result != 0:
            exit_code = unit_result
    
    if args.type in ["load", "all"]:
        load_result = run_load_tests(args.host)
        if load_result != 0:
            exit_code = load_result
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 