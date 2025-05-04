#!/usr/bin/env python3
"""
Main module to demonstrate the Mod-Three FSM solution.

This script provides a command-line interface for demonstrating and using
the ModThreeFSM class and mod_three function.

Author: FAANG Tech Lead
"""

import argparse
import logging
import sys

from src.mod_three import ModThreeFSM, mod_three
from demos.mod_three_demo import run_examples, demonstrate_fsm_usage, interactive_mode


def configure_logging(verbose=False):
    """
    Configure logging for the application.
    
    Sets up the logging format and level for consistent log output across the application.
    
    Args:
        verbose: Whether to enable verbose logging (DEBUG level)
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def run_examples():
    """
    Run the examples provided in the assignment to demonstrate the mod-three solution.
    
    This function processes the three example binary strings from the assignment:
    - '1101' (decimal 13) → remainder 1
    - '1110' (decimal 14) → remainder 2
    - '1111' (decimal 15) → remainder 0
    
    The function also verifies the results using assertions to ensure correctness.
    """
    print("\n=== Examples from Assignment ===")
    examples = [
        ('1101', 1),  # Example 1: 13 ÷ 3 = 4 remainder 1
        ('1110', 2),  # Example 2: 14 ÷ 3 = 4 remainder 2
        ('1111', 0),  # Example 3: 15 ÷ 3 = 5 remainder 0
    ]
    
    for binary, expected in examples:
        decimal = int(binary, 2)
        result = mod_three(binary)
        print(f"Binary: {binary} | Decimal: {decimal} | Remainder mod 3: {result}")
        assert result == expected, f"Expected {expected}, got {result}"


def demonstrate_fsm_usage():
    """
    Demonstrate using the ModThreeFSM class directly with detailed state transitions.
    
    This function shows the step-by-step operation of the FSM by:
    1. Processing each digit of the binary string '1101' one at a time
    2. Tracking the state before and after each transition
    3. Displaying a table of state transitions
    4. Showing the final state and the remainder
    
    This provides a clear visualization of how the FSM processes binary input
    and arrives at the correct remainder when divided by 3.
    """
    print("\n=== Using ModThreeFSM Class ===")
    fsm = ModThreeFSM()
    
    # Process a binary string step by step
    binary = '1101'
    print(f"Processing binary string: {binary}")
    
    fsm.reset()
    states = []
    
    # Process each digit and track states
    for i, digit in enumerate(binary):
        state_before = fsm.current_state
        fsm.process_single_input(digit)
        state_after = fsm.current_state
        states.append((i, digit, state_before, state_after))
    
    # Print state transitions
    print("\nState Transitions:")
    print("Step | Input | State Before | State After")
    print("-" * 45)
    for step, digit, before, after in states:
        print(f"{step:4} | {digit:5} | {before.name:12} | {after.name:10}")
    
    remainder = fsm.current_state.value
    print(f"\nFinal state: {fsm.current_state.name}")
    print(f"Remainder when {binary} (decimal {int(binary, 2)}) is divided by 3: {remainder}")


def interactive_mode():
    """
    Run the application in interactive mode, allowing users to enter their own binary numbers.
    
    This function:
    1. Prompts the user to enter binary numbers
    2. Computes the remainder when divided by 3
    3. Displays both the decimal equivalent and the remainder
    4. Handles errors gracefully with informative messages
    5. Continues until the user enters 'exit', 'quit', or 'q'
    
    This mode is useful for testing with custom inputs and exploring the FSM behavior.
    """
    print("\n=== Interactive Mode ===")
    print("Enter binary numbers to compute their remainder mod 3 (or 'exit' to quit)")
    
    while True:
        binary = input("\nEnter a binary number: ")
        if binary.lower() in ('exit', 'quit', 'q'):
            break
            
        try:
            result = mod_three(binary)
            decimal = int(binary, 2)
            print(f"Binary: {binary} | Decimal: {decimal} | Remainder mod 3: {result}")
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Demonstration of the Mod-Three FSM solution',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode after demonstrations'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--examples-only', '-e',
        action='store_true',
        help='Run only the examples from the assignment'
    )
    
    parser.add_argument(
        '--binary', '-b',
        type=str,
        help='Process a specific binary number and exit'
    )
    
    return parser.parse_args()


def main():
    """
    Main entry point for the Mod-Three FSM demonstration application.
    
    This function coordinates the overall flow of the demonstration:
    1. Parses command-line arguments
    2. Configures logging for the application
    3. Displays an introduction message
    4. Runs the examples from the assignment
    5. Demonstrates the step-by-step FSM operation
    6. Enters interactive mode if requested
    
    Command-line arguments:
        --interactive, -i: Run the application in interactive mode after the demonstrations
        --verbose, -v: Enable verbose logging
        --examples-only, -e: Run only the examples from the assignment
        --binary, -b: Process a specific binary number and exit
    
    Example usage:
        python main.py                   # Run the standard demonstrations
        python main.py -i                # Run demonstrations and enter interactive mode
        python main.py -v                # Run with verbose logging
        python main.py -e                # Run only the examples
        python main.py -b 1101           # Process a specific binary number
    """
    args = parse_arguments()
    
    # Configure logging based on verbosity
    configure_logging(args.verbose)
    
    print("=== Mod-Three FSM Demonstration ===")
    print("This program demonstrates computing the remainder when a binary number is divided by 3.")
    
    # Process a specific binary number if provided
    if args.binary:
        try:
            result = mod_three(args.binary)
            decimal = int(args.binary, 2)
            print(f"\nBinary: {args.binary} | Decimal: {decimal} | Remainder mod 3: {result}")
            return
        except ValueError as e:
            print(f"Error: {str(e)}")
            return
    
    # Run examples
    run_examples()
    
    # If examples-only flag is set, return after running examples
    if args.examples_only:
        return
    
    # Demonstrate FSM usage
    demonstrate_fsm_usage()
    
    # Enter interactive mode if requested
    if args.interactive:
        interactive_mode()
    else:
        print("\nRun with --interactive (-i) to enter interactive mode.")


if __name__ == "__main__":
    main()