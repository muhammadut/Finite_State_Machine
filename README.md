<<<<<<< HEAD
# Finite_State_Machine
FSM Implementation
=======
# Finite State Machine (FSM) Implementation

## Overview

This project provides a production-grade, object-oriented implementation of a Finite State Machine (FSM), along with a specific implementation for solving the mod-three problem. The mod-three problem calculates the remainder when a binary number is divided by 3 using FSM principles.

## Features

- Generic, reusable Finite State Machine implementation
- Flexible state and input representation
- Comprehensive error handling and validation
- Detailed logging for debugging and monitoring
- Complete test coverage
- Production-ready code quality

## Installation

### Prerequisites

- Python 3.8 or higher
- No external dependencies required for the core functionality

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/fsm-implementation.git
   cd fsm-implementation
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Usage

### Basic FSM Usage

```python
from fsm_implementation import FiniteStateMachine

# Define FSM components
states = {'q0', 'q1'}
alphabet = {'0', '1'}
initial_state = 'q0'
final_states = {'q1'}
transition_function = {
    ('q0', '0'): 'q0',
    ('q0', '1'): 'q1',
    ('q1', '0'): 'q0',
    ('q1', '1'): 'q1'
}

# Create FSM
fsm = FiniteStateMachine(
    states=states,
    alphabet=alphabet,
    initial_state=initial_state,
    final_states=final_states,
    transition_function=transition_function
)

# Process input
final_state = fsm.process_input('1101')
print(f"Final state: {final_state}")
print(f"Is in final state: {fsm.is_in_final_state}")
print(f"State history: {fsm.state_history}")
```

### Using the Mod-Three FSM

```python
from fsm_implementation import ModThreeFSM

# Create the mod-three FSM
mod_three_fsm = ModThreeFSM()

# Calculate remainder when binary number is divided by 3
binary_string = '1101'
remainder = mod_three_fsm.compute_remainder(binary_string)
print(f"The remainder when {binary_string} is divided by 3 is {remainder}")
```

### Using the Convenience Function

```python
from fsm_implementation import mod_three

# Calculate remainder directly
binary_string = '1101'
remainder = mod_three(binary_string)
print(f"The remainder when {binary_string} is divided by 3 is {remainder}")
```

## Implementation Details

### FiniteStateMachine Class

The `FiniteStateMachine` class implements a generic FSM based on the formal definition:

- A set of states (Q)
- An input alphabet (Σ)
- An initial state (q0)
- A set of final/accepting states (F)
- A transition function (δ: Q×Σ→Q)

Key features:

- **Flexible State Representation**: States can be any hashable Python objects (strings, numbers, custom objects)
- **Transition Function Options**: Support for both dictionary-based and callable transition functions
- **State History Tracking**: Maintains a history of state transitions for debugging
- **Comprehensive Validation**: Validates states, inputs, and transitions during initialization and execution

### ModThreeFSM Class

The `ModThreeFSM` class implements the specific FSM for the mod-three problem:

- States: S0, S1, S2 (representing remainders 0, 1, 2)
- Alphabet: '0', '1'
- Initial state: S0
- Final states: All states are final
- Transition function: As defined in the problem statement

### Error Handling

The implementation includes custom exception classes for different error conditions:

- `FSMException`: Base exception for all FSM-related errors
- `InvalidStateError`: Raised when an invalid state is encountered
- `InvalidInputError`: Raised when an invalid input symbol is encountered
- `InvalidTransitionError`: Raised when an invalid transition is attempted

### Logging

The implementation includes detailed logging to help with debugging and monitoring:

- Initialization information
- State transitions
- Error conditions

## Testing

Comprehensive unit tests are provided for all functionality:

```bash
python -m unittest discover
```

### Test Coverage

The test suite covers:

- Basic FSM functionality
- Edge cases and error conditions
- ModThreeFSM implementation details
- Convenience function behavior

The tests ensure 100% code coverage of the core functionality.

## Performance Considerations

The FSM implementation is designed to be efficient:

- Time complexity for processing input: O(n), where n is the length of the input sequence
- Space complexity: O(n) for state history, O(1) if state history tracking is disabled
- Transition lookup: O(1) using dictionary-based transitions

## Extensibility

The design allows for easy extension:

1. **Creating Custom FSMs**: Extend FiniteStateMachine or create a wrapper class like ModThreeFSM
2. **Custom State Types**: Use enum classes or custom objects for more complex state behavior
3. **Advanced Transition Logic**: Replace the simple transition function with more complex logic

## Project Structure

```
finite-state-machine/
├── src/
│   ├── __init__.py
│   ├── fsm_implementation.py  # Core FSM implementation
│   └── mod_three.py           # Mod-three specific implementation
├── tests/
│   ├── __init__.py
│   ├── test_fsm.py            # Tests for generic FSM
│   └── test_mod_three.py      # Tests for mod-three implementation
├── examples/
│   ├── basic_usage.py         # Basic FSM usage examples
│   └── mod_three_example.py   # Mod-three usage examples
├── README.md                  # This file
├── LICENSE                    # License information
└── setup.py                   # Package installation setup
```

## Running the Examples

```bash
# Basic FSM example
python examples/basic_usage.py

# Mod-three example
python examples/mod_three_example.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This implementation is based on the formal definition of Finite State Machines
- Inspired by the mod-three problem as described in the technical assignment
>>>>>>> 7e420ef (first commit)
