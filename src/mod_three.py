"""
Mod-Three Implementation using Finite State Machine

This module implements a solution to the mod-three problem using a Finite State Machine (FSM).
The mod-three problem calculates the remainder when a binary number is divided by 3.

Author: FAANG Tech Lead
Date: 2025-05-03
"""

from enum import Enum
import logging
from typing import Dict, Tuple

from src.finite_state_machine import FiniteStateMachine, InvalidInputError

# Configure logging
logger = logging.getLogger(__name__)


class ModThreeState(Enum):
    """
    States for the mod-three FSM.
    
    Each state represents the current remainder when dividing by 3:
    - S0: Remainder 0
    - S1: Remainder 1
    - S2: Remainder 2
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
    - Initial state: S0
    - Final states: All states are final
    - Transition function: As defined in the problem
    """
    
    # Define the transition table as a class constant
    # The transition table is:
    # +------+--------+--------+
    # | State| Input 0| Input 1|
    # +------+--------+--------+
    # |  S0  |   S0   |   S1   |
    # |  S1  |   S2   |   S0   |
    # |  S2  |   S1   |   S2   |
    # +------+--------+--------+
    TRANSITIONS: Dict[Tuple[ModThreeState, str], ModThreeState] = {
        (ModThreeState.S0, '0'): ModThreeState.S0,
        (ModThreeState.S0, '1'): ModThreeState.S1,
        (ModThreeState.S1, '0'): ModThreeState.S2,
        (ModThreeState.S1, '1'): ModThreeState.S0,
        (ModThreeState.S2, '0'): ModThreeState.S1,
        (ModThreeState.S2, '1'): ModThreeState.S2
    }
    
    def __init__(self):
        """Initialize the mod-three FSM."""
        # Define FSM components
        states = set(ModThreeState)
        alphabet = {'0', '1'}
        initial_state = ModThreeState.S0
        final_states = set(ModThreeState)  # All states are final
        
        # Create the FSM using the class-level transition table
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
        """Get the current state of the FSM."""
        return self._fsm.current_state
    
    @property
    def state_history(self) -> list:
        """Get the history of states visited."""
        return self._fsm.state_history
    
    def reset(self):
        """Reset the FSM to its initial state."""
        self._fsm.reset()
    
    def process_single_input(self, input_symbol: str) -> ModThreeState:
        """
        Process a single input symbol and return the new state.
        
        Args:
            input_symbol: A single binary digit ('0' or '1')
            
        Returns:
            The new state after processing the input
            
        Raises:
            ValueError: If the input symbol is not '0' or '1'
        """
        try:
            return self._fsm.process_single_input(input_symbol)
        except InvalidInputError:
            raise ValueError(f"Invalid input symbol: '{input_symbol}'. Must be '0' or '1'.")
    
    def compute_remainder(self, binary_string: str) -> int:
        """
        Compute the remainder when the binary number is divided by 3.
        
        Args:
            binary_string: A string of '0's and '1's representing a binary number
            
        Returns:
            The remainder when the binary number is divided by 3 (0, 1, or 2)
            
        Raises:
            ValueError: If the input string is empty
            InvalidInputError: If the input contains characters other than '0' or '1'
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
        
        Returns:
            A human-readable string showing the current state and remainder
        """
        return f"ModThreeFSM(state={self.current_state.name}, remainder={self.current_state.value})"
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the ModThreeFSM for debugging.
        
        Returns:
            A detailed string representation of the ModThreeFSM
        """
        return f"ModThreeFSM(fsm={self._fsm}, current_remainder={self.current_state.value})"


def mod_three(binary_string: str) -> int:
    """
    Convenience function to compute the remainder when a binary number is divided by 3.
    
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