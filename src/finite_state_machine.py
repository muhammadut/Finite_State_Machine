"""
Finite State Machine Core Implementation

This module provides a generic, reusable implementation of a Finite State Machine (FSM).
The implementation follows formal automaton theory and provides a foundation for
building different types of state machines.

Design Philosophy:
- Generic & Reusable: Implement a core FSM that can be used for various applications
- Type Safety: Use Python's typing module for clear interfaces and better IDE support
- Error Handling: Implement custom exceptions for clear error identification
- Logging: Integrate logging for debugging and operational insights
- Flexibility: Allow both dictionary-based and callable transition functions

Author: Muhammad Tariq
Date: 2025-05-04
"""

from typing import Any, Callable, Dict, Iterable, Optional, Set, Tuple, Union
import logging

# Configure logging with a standard format that includes timestamp, logger name, level, and message
# This helps with debugging and understanding the sequence of operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Get a logger specific to this module, which allows targeted log filtering
logger = logging.getLogger(__name__)


class FSMException(Exception):
    """
    Base exception for all FSM-related errors.
    
    Using a hierarchy of exceptions allows for more granular exception handling:
    - Catch FSMException for any FSM-related error
    - Catch specific subclasses for targeted error handling
    """
    pass


class InvalidStateError(FSMException):
    """
    Raised when an invalid state is encountered.
    
    Examples:
    - Initial state not in the set of states
    - Final state not in the set of states
    - Transition to a state not in the set of states
    """
    pass


class InvalidInputError(FSMException):
    """
    Raised when an invalid input symbol is encountered.
    
    Examples:
    - Input symbol not in the alphabet
    - Transition with an input not in the alphabet
    """
    pass


class InvalidTransitionError(FSMException):
    """
    Raised when an invalid transition is attempted.
    
    Examples:
    - No transition defined for a given state and input
    - Transition function returns None or an invalid state
    """
    pass


class FiniteStateMachine:
    """
    A generic implementation of a Finite State Machine.
    
    A Finite State Machine (FSM) is defined by:
    - A set of states (Q)
    - An input alphabet (Σ)
    - An initial state (q0)
    - A set of final/accepting states (F)
    - A transition function (δ: Q×Σ→Q)
    
    This class provides a flexible, reusable implementation that can be used
    for various FSM applications. The implementation supports:
    
    1. Any hashable object as states and input symbols
    2. Both dictionary-based and callable transition functions
    3. Comprehensive error checking and validation
    4. Tracking of state history for debugging
    5. Integration with Python's logging system
    
    The FSM is designed to be used either directly or as a base for more specific FSMs.
    """
    
    def __init__(
        self,
        states: Set[Any],                       # Set of all possible states
        alphabet: Set[Any],                     # Set of all possible input symbols
        initial_state: Any,                     # The starting state
        final_states: Set[Any],                 # Set of final/accepting states
        transition_function: Union[Dict[Tuple[Any, Any], Any], Callable[[Any, Any], Any]]  # The transition function
    ):
        """
        Initialize the FSM with its components.
        
        The implementation follows the formal definition of a finite automaton as a 5-tuple
        (Q, Σ, q0, F, δ) where:
        - Q: Set of states
        - Σ: Input alphabet
        - q0: Initial state
        - F: Set of final/accepting states
        - δ: Transition function
        
        Args:
            states: Set of all possible states (Q in the formal definition)
            alphabet: Set of all possible input symbols (Σ in the formal definition)
            initial_state: The starting state (q0 in the formal definition)
            final_states: Set of final/accepting states (F in the formal definition)
            transition_function: Either a dictionary mapping (state, input) -> next_state,
                               or a function that takes (state, input) and returns next_state
                               (δ in the formal definition)
        
        Raises:
            TypeError: If the arguments are not of the expected types (important for static analysis)
            InvalidStateError: If initial_state or any final_state is not in states
            InvalidInputError: If the transition function uses inputs not in the alphabet
        """
        # Validate input types - this improves type safety and provides clear error messages
        if not isinstance(states, set):
            raise TypeError("States must be provided as a set")
        if not isinstance(alphabet, set):
            raise TypeError("Alphabet must be provided as a set")
        if not isinstance(final_states, set):
            raise TypeError("Final states must be provided as a set")
            
        # Validate states - these checks ensure the FSM is well-formed from the start
        if initial_state not in states:
            raise InvalidStateError(f"Initial state '{initial_state}' is not in the set of states")
        
        if not final_states.issubset(states):
            invalid_finals = final_states - states
            raise InvalidStateError(f"Some final states {invalid_finals} are not in the set of states")
            
        # Store the FSM components as instance variables
        self._states = states                   # Store all possible states
        self._alphabet = alphabet               # Store all possible input symbols
        self._initial_state = initial_state     # Store the initial state
        self._final_states = final_states       # Store the final/accepting states
        self._current_state = initial_state     # Initialize current state to initial state
        self._history = [initial_state]         # Track state history for debugging and analysis
        
        # Store transition function - handle both callable and dictionary-based transition functions
        if callable(transition_function):
            # If a function is provided, use it directly
            self._transition_func = transition_function
        else:
            # If a dictionary is provided, create a function that uses the dictionary for lookups
            # Using a lambda function here allows for a uniform interface regardless of how
            # the transition function was defined
            self._transition_func = lambda state, input_symbol: transition_function.get((state, input_symbol))
            
        # Validate transition function if it's a dictionary - ensures the transition function is valid
        if isinstance(transition_function, dict):
            for (state, input_symbol), next_state in transition_function.items():
                # Check that all states used in transitions are valid
                if state not in states:
                    raise InvalidStateError(f"Transition from invalid state '{state}'")
                # Check that all input symbols used in transitions are valid
                if input_symbol not in alphabet:
                    raise InvalidInputError(f"Transition with invalid input '{input_symbol}'")
                # Check that all destination states are valid
                if next_state not in states:
                    raise InvalidStateError(f"Transition to invalid state '{next_state}'")
        
        # Log initialization for debugging and operational visibility
        logger.info(f"Initialized FSM with {len(states)} states and {len(alphabet)} input symbols")
    
    @property
    def current_state(self) -> Any:
        """
        Get the current state of the FSM.
        
        This is implemented as a property to:
        1. Provide read-only access to the current state
        2. Allow for future enhancement (e.g., logging state access)
        3. Provide a clean interface
        
        Returns:
            The current state of the FSM
        """
        return self._current_state
    
    @property
    def is_in_final_state(self) -> bool:
        """
        Check if the FSM is currently in a final/accepting state.
        
        This is a convenience method that simplifies checking the acceptance condition.
        
        Returns:
            True if the current state is a final/accepting state, False otherwise
        """
        return self._current_state in self._final_states
    
    @property
    def state_history(self) -> list:
        """
        Get the history of states visited.
        
        This is useful for:
        1. Debugging: Seeing how the FSM got to its current state
        2. Analysis: Understanding the path taken through the state space
        3. Visualization: Creating diagrams of state transitions
        
        Returns:
            A copy of the history list to prevent external modification
        """
        return self._history.copy()  # Return a copy to prevent external modification
    
    def reset(self) -> None:
        """
        Reset the FSM to its initial state.
        
        This method is essential for:
        1. Reusing the same FSM instance for multiple inputs
        2. Testing different input sequences on the same FSM
        3. Recovering from errors or invalid inputs
        
        The method resets both the current state and the state history.
        """
        self._current_state = self._initial_state
        self._history = [self._initial_state]
        logger.debug("FSM reset to initial state")  # Log the reset for debugging
    
    def process_input(self, input_sequence: Iterable) -> Any:
        """
        Process a sequence of input symbols and return the final state.
        
        This is the core method of the FSM that:
        1. Takes a sequence of input symbols
        2. Applies the transition function to each input
        3. Updates the current state accordingly
        4. Tracks the state history for debugging
        5. Returns the final state after processing all inputs
        
        Args:
            input_sequence: Sequence of input symbols (e.g., string, list, tuple)
            
        Returns:
            The final state after processing all inputs
            
        Raises:
            InvalidInputError: If any input symbol is not in the alphabet
            InvalidStateError: If any transition leads to an invalid state
            InvalidTransitionError: If a transition is undefined
        """
        for i, input_symbol in enumerate(input_sequence):
            # Validate that the input symbol is in the alphabet
            if input_symbol not in self._alphabet:
                raise InvalidInputError(f"Invalid input symbol '{input_symbol}' at position {i}")
                
            # Apply the transition function to get the next state
            next_state = self._transition_func(self._current_state, input_symbol)
            
            # Check if the transition is defined
            if next_state is None:
                raise InvalidTransitionError(
                    f"No transition defined for state '{self._current_state}' and input '{input_symbol}'"
                )
            
            # Validate that the next state is in the set of states
            if next_state not in self._states:
                raise InvalidStateError(f"Transition to invalid state '{next_state}'")
                
            # Log the transition for debugging
            logger.debug(f"Transition: {self._current_state} --({input_symbol})--> {next_state}")
            
            # Update the current state and history
            self._current_state = next_state
            self._history.append(next_state)
        
        # Return the final state after processing all inputs
        return self._current_state
    
    def process_single_input(self, input_symbol: Any) -> Any:
        """
        Process a single input symbol and return the new state.
        
        This is a convenience method that:
        1. Wraps the input symbol in a list
        2. Calls the process_input method
        3. Returns the result
        
        This simplifies processing a single input symbol without creating a list.
        
        Args:
            input_symbol: A single input symbol
            
        Returns:
            The new state after processing the input
            
        Raises:
            InvalidInputError: If the input symbol is not in the alphabet
            InvalidStateError: If the transition leads to an invalid state
            InvalidTransitionError: If the transition is undefined
        """
        return self.process_input([input_symbol])
    
    def __str__(self) -> str:
        """
        Return a string representation of the FSM, showing its current state.
        
        This method provides a human-readable representation of the FSM's current status,
        which is useful for debugging and logging. It shows:
        1. The current state
        2. Whether the current state is an accepting state
        3. The total number of states
        
        Returns:
            A human-readable string representing the FSM's current status
        """
        status = "accepting" if self.is_in_final_state else "non-accepting"
        return f"FSM(state={self._current_state}, {status}, states={len(self._states)})"
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the FSM for debugging.
        
        This method provides a more detailed representation of the FSM,
        which is useful for debugging and introspection. It shows all components
        of the FSM: states, alphabet, initial state, final states, and current state.
        
        Returns:
            A detailed string representation of the FSM
        """
        return (f"FiniteStateMachine(states={self._states}, "
                f"alphabet={self._alphabet}, "
                f"initial_state={self._initial_state}, "
                f"final_states={self._final_states}, "
                f"current_state={self._current_state})")