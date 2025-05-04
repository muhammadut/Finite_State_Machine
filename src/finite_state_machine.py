"""
Finite State Machine Core Implementation

This module provides a generic, reusable implementation of a Finite State Machine (FSM).
The implementation follows formal automaton theory and provides a foundation for
building different types of state machines.

Author: Muhammad Tariq
Date: 2025-05-03
"""

from typing import Any, Callable, Dict, Iterable, Optional, Set, Tuple, Union
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FSMException(Exception):
    """Base exception for all FSM-related errors."""
    pass


class InvalidStateError(FSMException):
    """Raised when an invalid state is encountered."""
    pass


class InvalidInputError(FSMException):
    """Raised when an invalid input symbol is encountered."""
    pass


class InvalidTransitionError(FSMException):
    """Raised when an invalid transition is attempted."""
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
    for various FSM applications.
    """
    
    def __init__(
        self,
        states: Set[Any],
        alphabet: Set[Any],
        initial_state: Any,
        final_states: Set[Any],
        transition_function: Union[Dict[Tuple[Any, Any], Any], Callable[[Any, Any], Any]]
    ):
        """
        Initialize the FSM with its components.
        
        Args:
            states: Set of all possible states
            alphabet: Set of all possible input symbols
            initial_state: The starting state
            final_states: Set of final/accepting states
            transition_function: Either a dictionary mapping (state, input) -> next_state,
                               or a function that takes (state, input) and returns next_state
        
        Raises:
            TypeError: If the arguments are not of the expected types
            InvalidStateError: If initial_state or any final_state is not in states
        """
        # Validate input types
        if not isinstance(states, set):
            raise TypeError("States must be provided as a set")
        if not isinstance(alphabet, set):
            raise TypeError("Alphabet must be provided as a set")
        if not isinstance(final_states, set):
            raise TypeError("Final states must be provided as a set")
            
        # Validate states
        if initial_state not in states:
            raise InvalidStateError(f"Initial state '{initial_state}' is not in the set of states")
        
        if not final_states.issubset(states):
            invalid_finals = final_states - states
            raise InvalidStateError(f"Some final states {invalid_finals} are not in the set of states")
            
        self._states = states
        self._alphabet = alphabet
        self._initial_state = initial_state
        self._final_states = final_states
        self._current_state = initial_state
        self._history = [initial_state]  # Track state history for debugging
        
        # Store transition function
        if callable(transition_function):
            self._transition_func = transition_function
        else:
            # Create a function that uses the dictionary for lookups
            self._transition_func = lambda state, input_symbol: transition_function.get((state, input_symbol))
            
        # Validate transition function if it's a dictionary
        if isinstance(transition_function, dict):
            for (state, input_symbol), next_state in transition_function.items():
                if state not in states:
                    raise InvalidStateError(f"Transition from invalid state '{state}'")
                if input_symbol not in alphabet:
                    raise InvalidInputError(f"Transition with invalid input '{input_symbol}'")
                if next_state not in states:
                    raise InvalidStateError(f"Transition to invalid state '{next_state}'")
        
        logger.info(f"Initialized FSM with {len(states)} states and {len(alphabet)} input symbols")
    
    @property
    def current_state(self) -> Any:
        """Get the current state of the FSM."""
        return self._current_state
    
    @property
    def is_in_final_state(self) -> bool:
        """Check if the FSM is currently in a final/accepting state."""
        return self._current_state in self._final_states
    
    @property
    def state_history(self) -> list:
        """Get the history of states visited."""
        return self._history.copy()
    
    def reset(self) -> None:
        """Reset the FSM to its initial state."""
        self._current_state = self._initial_state
        self._history = [self._initial_state]
        logger.debug("FSM reset to initial state")
    
    def process_input(self, input_sequence: Iterable) -> Any:
        """
        Process a sequence of input symbols and return the final state.
        
        Args:
            input_sequence: Sequence of input symbols
            
        Returns:
            The final state after processing all inputs
            
        Raises:
            InvalidInputError: If any input symbol is not in the alphabet
            InvalidStateError: If any transition leads to an invalid state
            InvalidTransitionError: If a transition is undefined
        """
        for i, input_symbol in enumerate(input_sequence):
            if input_symbol not in self._alphabet:
                raise InvalidInputError(f"Invalid input symbol '{input_symbol}' at position {i}")
                
            next_state = self._transition_func(self._current_state, input_symbol)
            
            if next_state is None:
                raise InvalidTransitionError(
                    f"No transition defined for state '{self._current_state}' and input '{input_symbol}'"
                )
            
            if next_state not in self._states:
                raise InvalidStateError(f"Transition to invalid state '{next_state}'")
                
            logger.debug(f"Transition: {self._current_state} --({input_symbol})--> {next_state}")
            self._current_state = next_state
            self._history.append(next_state)
        
        return self._current_state
    
    def process_single_input(self, input_symbol: Any) -> Any:
        """
        Process a single input symbol and return the new state.
        
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
        
        Returns:
            A human-readable string representing the FSM's current status
        """
        status = "accepting" if self.is_in_final_state else "non-accepting"
        return f"FSM(state={self._current_state}, {status}, states={len(self._states)})"
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the FSM for debugging.
        
        Returns:
            A detailed string representation of the FSM
        """
        return (f"FiniteStateMachine(states={self._states}, "
                f"alphabet={self._alphabet}, "
                f"initial_state={self._initial_state}, "
                f"final_states={self._final_states}, "
                f"current_state={self._current_state})")