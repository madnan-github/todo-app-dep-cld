#!/usr/bin/env python3
"""
Comprehensive test suite for TaskFlow application.

This script runs all tests in the test suite and provides a summary of results.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_tests():
    """Run all tests in the test suite."""
    print("Running TaskFlow Application Test Suite")
    print("=" * 50)
    
    # Get the directory containing this script
    tests_dir = Path(__file__).parent
    
    # Find all test files
    test_files = list(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("No test files found!")
        return 1
    
    print(f"Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"  - {test_file.name}")
    print()
    
    # Run each test file individually
    results = []
    for test_file in test_files:
        print(f"Running {test_file.name}...")
        
        # Run the test file with pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(test_file), 
            "-v",  # verbose
            "--tb=short"  # short traceback
        ], capture_output=True, text=True)
        
        results.append({
            'file': test_file.name,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        })
        
        if result.returncode == 0:
            print(f"  ✓ {test_file.name} PASSED")
        else:
            print(f"  ✗ {test_file.name} FAILED")
            # Print stderr if there was an error
            if result.stderr:
                print(f"    Error: {result.stderr[-200:]}...")  # Last 200 chars
        print()
    
    # Print summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['returncode'] == 0)
    failed_tests = total_tests - passed_tests
    
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    
    if failed_tests > 0:
        print("\nFAILED TESTS DETAILS:")
        for result in results:
            if result['returncode'] != 0:
                print(f"\n--- {result['file']} ---")
                print(result['stderr'])
    
    print("\n" + "=" * 50)
    
    return 0 if failed_tests == 0 else 1


def run_tests_with_coverage():
    """Run tests with coverage report."""
    print("Running tests with coverage...")
    
    try:
        import pytest_cov  # Check if pytest-cov is available
    except ImportError:
        print("pytest-cov not available, running tests without coverage...")
        return run_tests()
    
    tests_dir = Path(__file__).parent
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        str(tests_dir),
        "--cov=.",  # Coverage for current directory
        "--cov-report=html",  # HTML report
        "--cov-report=term",  # Terminal report
        "-v"
    ])
    
    return result.returncode


if __name__ == "__main__":
    # Check if --coverage flag is passed
    if "--coverage" in sys.argv:
        exit_code = run_tests_with_coverage()
    else:
        exit_code = run_tests()
    
    sys.exit(exit_code)