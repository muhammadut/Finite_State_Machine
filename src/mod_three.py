"""
Mod-Three Implementation using Finite State Machine

This module implements a solution to the mod-three problem using a Finite State Machine (FSM).
The problem requires computing the remainder when a binary number is divided by 3.

Key Features:
- Uses a Finite State Machine approach rather than direct conversion to integer
- Can handle binary strings of arbitrary length without integer overflow
- Follows Object-Oriented Design principles for clean, maintainable code
- Provides comprehensive error handling and validation
- Includes both a class-based API and a convenience function

Mathematical Basis:
The Mod-Three problem can be elegantly solved using a Finite State Machine because of 
mathematical properties related to base-2 representation and modular arithmetic:

For a number in binary form: d₍n₎d₍n-1₎...d₍1₎d₍0₎ (where d₍i₎ is either 0 or 1), 
the value is: d₍n₎×2ⁿ + d₍n-1₎×2ⁿ⁻¹ + ... + d₍1₎×2¹ + d₍0₎×2⁰

When calculating modulo 3, we can use the property:
(a × b) mod m = ((a mod m) × (b mod m)) mod m

Since 2⁰ mod 3 = 1
      2¹ mod 3 = 2
      2² mod 3 = 1
      2³ mod 3 = 2
      ... (this pattern repeats)

We can process the digits from left to right, tracking the remainder state.

Author: Muhammad Tariq
Date: 2025-05-04
"""

from enum import Enum  # Used for creating strongly typed states with associated values
import logging
from typing import Dict, Tuple  # Type hints for better IDE support and code clarity

from src.finite_state_machine import FiniteStateMachine, InvalidInputError

# Configure logging for this module
logger = logging.getLogger(__name__)


class ModThreeState(Enum):
    """
    States for the mod-three FSM.
    
    Each state represents the current remainder when dividing by 3:
    - S0: Remainder 0
    - S1: Remainder 1
    - S2: Remainder 2
    
    Using an Enum provides:
    1. Type safety - only valid states can be used
    2. Meaningful names - S0, S1, S2 are descriptive
    3. Associated values - each state has its remainder value
    4. String representation - useful for debugging and logging
    """
    S0 = 0  # Remainder 0
    S1 = 1  # Remainder 1
    S2 = 2  # Remainder 2


class ModThreeFSM:
    """
    Implementation of a Finite State Machine to compute the remainder
    when a binary number is divided by 3.
    
    This implementation follows the FSM design specified in the problem statement:
    - States: S0, S1, S2 (representing remainders 0, 1, 2)
    - Alphabet: '0', '1' (binary digits)
    - Initial state: S0 (remainder 0)
    - Final states: All states are final (any state can be the final state)
    - Transition function: As defined in the problem statement
    
    The FSM processes binary digits from left to right (most significant bit first),
    tracking the remainder state according to the transition table.
    """
    
    # Define the transition table as a class constant
    # The transition table is derived from mathematical analysis of how binary
    # digit position affects the remainder when divided by 3
    # +------+--------+--------+
    # | State| Input 0| Input 1|
    # +------+--------+--------+
    # |  S0  |   S0   |   S1   |
    # |  S1  |   S2   |   S0   |
    # |  S2  |   S1   |   S2   |
    # +------+--------+--------+
    TRANSITIONS: Dict[Tuple[ModThreeState, str], ModThreeState] = {
        (ModThreeState.S0, '0'): ModThreeState.S0,  # 0 * 2^n + r0 ≡ 0 (mod 3)
        (ModThreeState.S0, '1'): ModThreeState.S1,  # 1 * 2^n + r0 ≡ 1 (mod 3)
        (ModThreeState.S1, '0'): ModThreeState.S2,  # 0 * 2^n + r1 ≡ 2 (mod 3)
        (ModThreeState.S1, '1'): ModThreeState.S0,  # 1 * 2^n + r1 ≡ 0 (mod 3)
        (ModThreeState.S2, '0'): ModThreeState.S1,  # 0 * 2^n + r2 ≡ 1 (mod 3)
        (ModThreeState.S2, '1'): ModThreeState.S2   # 1 * 2^n + r2 ≡ 2 (mod 3)
    }
    
    def __init__(self):
        """
        Initialize the mod-three FSM.
        
        This constructor:
        1. Defines the components of the FSM (states, alphabet, etc.)
        2. Creates an instance of the generic FiniteStateMachine
        3. Logs the initialization
        
        No parameters are needed as the FSM configuration is fixed
        for the mod-three problem.
        """
        # Define FSM components based on the formal definition
        states = set(ModThreeState)  # All states in the enum
        alphabet = {'0', '1'}        # Binary digits only
        initial_state = ModThreeState.S0  # Start with remainder 0
        final_states = set(ModThreeState)  # All states are final
        
        # Create the FSM using the class-level transition table
        # Using the generic FiniteStateMachine class leverages code reuse
        # and separation of concerns
        self._fsm = FiniteStateMachine(
            states=states,
            alphabet=alphabet,
            initial_state=initial_state,
            final_states=final_states,
            transition_function=self.TRANSITIONS
        )
        
        logger.info("Initialized Mod-Three FSM")
    
    @property
    def current_state(self) -> ModThreeState:
        """
        Get the current state of the FSM.
        
        This property provides access to the current state while maintaining
        encapsulation of the underlying FSM. It is used for:
        1. Testing and debugging
        2. Demonstrating the FSM operation
        3. Accessing the current remainder
        
        Returns:
            The current state as a ModThreeState enum value
        """
        return self._fsm.current_state
    
    @property
    def state_history(self) -> list:
        """
        Get the history of states visited.
        
        This property provides access to the state history while maintaining
        encapsulation of the underlying FSM. It is used for:
        1. Debugging
        2. Demonstrating the FSM operation step by step
        3. Understanding how the FSM arrived at its result
        
        Returns:
            A list of ModThreeState enum values representing the state history
        """
        return self._fsm.state_history
    
    def reset(self):
        """
        Reset the FSM to its initial state.
        
        This method delegates to the underlying FSM's reset method,
        maintaining proper encapsulation while providing the necessary
        functionality. It is used to reuse the same FSM instance for
        multiple inputs.
        """
        self._fsm.reset()
    
    def process_single_input(self, input_symbol: str) -> ModThreeState:
        """
        Process a single input symbol and return the new state.
        
        This method delegates to the underlying FSM's process_single_input method,
        adding specific error handling for the mod-three context.
        
        Args:
            input_symbol: A single binary digit ('0' or '1')
            
        Returns:
            The new state after processing the input
            
        Raises:
            ValueError: If the input symbol is not '0' or '1'
        """
        try:
            # Delegate to the generic FSM
            return self._fsm.process_single_input(input_symbol)
        except InvalidInputError:
            # Convert the generic error to a more specific one for this context
            raise ValueError(f"Invalid input symbol: '{input_symbol}'. Must be '0' or '1'.")
    
    def compute_remainder(self, binary_string: str) -> int:
        """
        Compute the remainder when the binary number is divided by 3.
        
        This method:
        1. Validates the input
        2. Resets the FSM to its initial state
        3. Processes each digit in the binary string
        4. Returns the remainder based on the final state
        
        The method leverages the FSM to determine the remainder without
        converting the binary string to an integer, allowing it to handle
        binary strings of arbitrary length.
        
        Args:
            binary_string: A string of '0's and '1's representing a binary number
            
        Returns:
            The remainder when the binary number is divided by 3 (0, 1, or 2)
            
        Raises:
            ValueError: If the input string is empty or contains invalid characters
        """
        if not binary_string:
            raise ValueError("Input binary string cannot be empty")
            
        try:
            # Reset the FSM to its initial state
            self._fsm.reset()
            
            # Process each digit in the binary string
            final_state = self._fsm.process_input(binary_string)
            
            # The value of the final state is the remainder
            return final_state.value
            
        except InvalidInputError:
            # Convert the generic FSM error to a more specific error for this context
            raise ValueError("Input must contain only '0's and '1's")
    
    def __str__(self) -> str:
        """
        Return a string representation of the ModThreeFSM.
        
        This method provides a human-readable representation of the FSM's current status,
        which is useful for debugging and logging.
        
        Returns:
            A human-readable string showing the current state and remainder
        """
        return f"ModThreeFSM(state={self.current_state.name}, remainder={self.current_state.value})"
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the ModThreeFSM for debugging.
        
        This method provides a more detailed representation for debugging and introspection.
        
        Returns:
            A detailed string representation of the ModThreeFSM
        """
        return f"ModThreeFSM(fsm={self._fsm}, current_remainder={self.current_state.value})"


def mod_three(binary_string: str) -> int:
    """
    Convenience function to compute the remainder when a binary number is divided by 3.
    
    This function provides a simple interface to the ModThreeFSM class:
    1. It validates the input
    2. Creates a ModThreeFSM instance
    3. Computes the remainder
    4. Returns the result
    
    This simplifies the most common use case without requiring the user
    to create and manage a ModThreeFSM instance.
    
    Args:
        binary_string: A string of '0's and '1's representing a binary number
        
    Returns:
        The remainder when the binary number is divided by 3 (0, 1, or 2)
        
    Raises:
        ValueError: If the input is empty or contains invalid characters
    """
    if not binary_string:
        raise ValueError("Input binary string cannot be empty")
        
    if not all(bit in '01' for bit in binary_string):
        raise ValueError("Input must contain only '0's and '1's")
        
    fsm = ModThreeFSM()
    return fsm.compute_remainder(binary_string)