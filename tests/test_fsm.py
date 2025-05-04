"""
Unit tests for the generic Finite State Machine implementation.

This module contains comprehensive tests for the FiniteStateMachine class, testing various
configurations, transitions, and error handling scenarios to ensure the class works correctly.

Author: Muhammad Tariq
Date: 2025-05-04
"""

import unittest
from typing import Dict, Tuple, Any

from src.finite_state_machine import (
    FiniteStateMachine,
    InvalidStateError,
    InvalidInputError,
    InvalidTransitionError
)


class SimpleState:
    """Simple state class for testing."""
    def __init__(self, name):
        self.name = name
        
    def __eq__(self, other):
        if not isinstance(other, SimpleState):
            return False
        return self.name == other.name
        
    def __hash__(self):
        return hash(self.name)
        
    def __repr__(self):
        return f"SimpleState({self.name})"


class TestFiniteStateMachine(unittest.TestCase):
    """Test cases for the generic FiniteStateMachine implementation."""
    
    def setUp(self):
        """Set up a simple FSM for testing."""
        # Define a simple FSM that accepts binary strings ending with '1'
        
        # Define states
        self.state_a = SimpleState("A")  # Initial state
        self.state_b = SimpleState("B")  # Final state (accepting)
        
        # Define components for the FSM
        self.states = {self.state_a, self.state_b}
        self.alphabet = {'0', '1'}
        self.initial_state = self.state_a
        self.final_states = {self.state_b}
        
        # Define transition function as a dictionary
        self.transitions: Dict[Tuple[Any, Any], Any] = {
            (self.state_a, '0'): self.state_a,
            (self.state_a, '1'): self.state_b,
            (self.state_b, '0'): self.state_a,
            (self.state_b, '1'): self.state_b
        }
        
        # Create the FSM
        self.fsm = FiniteStateMachine(
            states=self.states,
            alphabet=self.alphabet,
            initial_state=self.initial_state,
            final_states=self.final_states,
            transition_function=self.transitions
        )
    
    def test_initialization(self):
        """Test that the FSM initializes correctly."""
        # Initial state should be set correctly
        self.assertEqual(self.fsm.current_state, self.state_a)
        
        # Initially not in a final state
        self.assertFalse(self.fsm.is_in_final_state)
        
        # State history should contain only the initial state
        self.assertEqual(self.fsm.state_history, [self.state_a])

    def test_initialization_errors(self):
        """Test that initialization errors are raised correctly."""
        # Test with initial state not in states
        invalid_state = SimpleState("Invalid")
        with self.assertRaises(InvalidStateError):
            FiniteStateMachine(
                states=self.states,
                alphabet=self.alphabet,
                initial_state=invalid_state,  # Invalid state
                final_states=self.final_states,
                transition_function=self.transitions
            )
        
        # Test with a final state not in states
        with self.assertRaises(InvalidStateError):
            FiniteStateMachine(
                states=self.states,
                alphabet=self.alphabet,
                initial_state=self.initial_state,
                final_states={invalid_state},  # Invalid final state
                transition_function=self.transitions
            )
        
        # Test with invalid transition
        invalid_transitions = self.transitions.copy()
        invalid_transitions[(invalid_state, '0')] = self.state_a
        with self.assertRaises(InvalidStateError):
            FiniteStateMachine(
                states=self.states,
                alphabet=self.alphabet,
                initial_state=self.initial_state,
                final_states=self.final_states,
                transition_function=invalid_transitions  # Invalid transition
            )
    
    def test_process_input(self):
        """Test processing input sequences."""
        # Process '0' - should stay in state A
        self.fsm.reset()
        result = self.fsm.process_input('0')
        self.assertEqual(result, self.state_a)
        self.assertFalse(self.fsm.is_in_final_state)
        
        # Process '1' - should transition to state B
        self.fsm.reset()
        result = self.fsm.process_input('1')
        self.assertEqual(result, self.state_b)
        self.assertTrue(self.fsm.is_in_final_state)
        
        # Process '01' - should end in state B
        self.fsm.reset()
        result = self.fsm.process_input('01')
        self.assertEqual(result, self.state_b)
        self.assertTrue(self.fsm.is_in_final_state)
        
        # Process '00' - should end in state A
        self.fsm.reset()
        result = self.fsm.process_input('00')
        self.assertEqual(result, self.state_a)
        self.assertFalse(self.fsm.is_in_final_state)
        
        # Process '011' - should end in state B
        self.fsm.reset()
        result = self.fsm.process_input('011')
        self.assertEqual(result, self.state_b)
        self.assertTrue(self.fsm.is_in_final_state)
    
    def test_process_single_input(self):
        """Test processing a single input."""
        # Process '0' - should stay in state A
        self.fsm.reset()
        result = self.fsm.process_single_input('0')
        self.assertEqual(result, self.state_a)
        
        # Process '1' - should transition to state B
        self.fsm.reset()
        result = self.fsm.process_single_input('1')
        self.assertEqual(result, self.state_b)
    
    def test_state_history(self):
        """Test that state history is tracked correctly."""
        # Process '010' and check history
        self.fsm.reset()
        self.fsm.process_input('010')
        
        expected_history = [
            self.state_a,  # Initial state
            self.state_a,  # After '0'
            self.state_b,  # After '1'
            self.state_a   # After '0'
        ]
        
        self.assertEqual(self.fsm.state_history, expected_history)
    
    def test_reset(self):
        """Test resetting the FSM."""
        # Change state first
        self.fsm.process_input('1')
        self.assertEqual(self.fsm.current_state, self.state_b)
        
        # Reset and check state
        self.fsm.reset()
        self.assertEqual(self.fsm.current_state, self.state_a)
        self.assertEqual(self.fsm.state_history, [self.state_a])
    
    def test_error_handling(self):
        """Test error handling for invalid inputs and transitions."""
        # Test with invalid input character
        with self.assertRaises(InvalidInputError):
            self.fsm.process_input('2')
        
        # Test with invalid input character in a sequence
        with self.assertRaises(InvalidInputError):
            self.fsm.process_input('01A')
    
    def test_callable_transition_function(self):
        """Test using a callable as the transition function."""
        # Define a callable transition function
        def transition_func(state, input_symbol):
            if state == self.state_a and input_symbol == '0':
                return self.state_a
            elif state == self.state_a and input_symbol == '1':
                return self.state_b
            elif state == self.state_b and input_symbol == '0':
                return self.state_a
            elif state == self.state_b and input_symbol == '1':
                return self.state_b
            return None
        
        # Create a new FSM with the callable
        fsm_callable = FiniteStateMachine(
            states=self.states,
            alphabet=self.alphabet,
            initial_state=self.initial_state,
            final_states=self.final_states,
            transition_function=transition_func
        )
        
        # Test transitions
        fsm_callable.process_input('01')
        self.assertEqual(fsm_callable.current_state, self.state_b)
        
        fsm_callable.reset()
        fsm_callable.process_input('00')
        self.assertEqual(fsm_callable.current_state, self.state_a)
    
    def test_string_representations(self):
        """Test string representation methods."""
        # Test __str__
        expected_str = "FSM(state=A, non-accepting, states=2)"
        self.assertTrue(str(self.fsm).startswith("FSM(state="))
        
        # Test __repr__
        self.assertTrue(repr(self.fsm).startswith("FiniteStateMachine("))
        
        # Test with FSM in final state
        self.fsm.process_input('1')
        self.assertTrue("accepting" in str(self.fsm))
    
    def test_empty_input(self):
        """Test that processing an empty input sequence returns the initial state."""
        # Reset the FSM to initial state
        self.fsm.reset()
        
        # Process empty input
        result = self.fsm.process_input("")
        
        # The result should be the initial state
        self.assertEqual(result, self.state_a)
        self.assertEqual(self.fsm.current_state, self.state_a)
        
        # History should only contain the initial state
        self.assertEqual(self.fsm.state_history, [self.state_a])


if __name__ == '__main__':
    unittest.main()