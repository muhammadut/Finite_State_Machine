"""
Demonstration module for the Mod-Three FSM solution.

This module contains demonstration functions for the ModThreeFSM and mod_three implementations.

Author: Muhammad Tariq
"""

import logging
from src.mod_three import ModThreeFSM, mod_three

# Get logger for this module
logger = logging.getLogger(__name__)


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
    
    # Show string representation
    print(f"\nString representation: {fsm}")


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