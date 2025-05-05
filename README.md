# Finite State Machine: Mod-Three Implementation

## Overview

This project provides a generic, reusable implementation of a Finite State Machine (FSM) and applies it to solve the mod-three problem: determining the remainder when a binary number is divided by 3 without directly converting it to an integer.


## Problem Description

Given a string of ones and zeros representing an unsigned binary integer, compute the remainder when the represented value is divided by three using a Finite State Machine approach.

Examples:
- Input: '1101' → Output: 1
- Input: '1110' → Output: 2
- Input: '1111' → Output: 0

## Project Structure

```
fsm-mod-three/
├── demos/                      # Demonstration code
│   ├── __init__.py
│   └── mod_three_demo.py       # Demo functions for the mod-three FSM
├── src/                        # Source code
│   ├── __init__.py
│   ├── finite_state_machine.py # Generic FSM implementation
│   └── mod_three.py            # Mod-three specific implementation
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_fsm.py             # Tests for generic FSM
│   └── test_mod_three.py       # Tests for mod-three implementation
├── main.py                     # Application entry point
└── README.md                   # Project documentation
```

## Installation

No external dependencies are required. The project uses standard Python libraries.

Requirements:
- Python 3.6+


## Usage

### Command-Line Interface

```bash
# Run standard demonstrations
python -m src.main

# Run in interactive mode (enter your own binary numbers)
python -m src.main -i

# Process a specific binary number
python -m src.main -b 10110

# Run only examples from the assignment
python -m src.main -e

# Enable verbose logging
python -m src.main -v
```

### API Usage

```python
# Using the convenience function
from src.mod_three import mod_three

result = mod_three('1101')  # Returns 1

# Using the ModThreeFSM class
from src.mod_three import ModThreeFSM

fsm = ModThreeFSM()
remainder = fsm.compute_remainder('1101')  # Returns 1

# Tracking state transitions
fsm.reset()
for digit in '1101':
    current_state = fsm.current_state
    fsm.process_single_input(digit)
    new_state = fsm.current_state
    print(f"Input: {digit}, State: {current_state.name} -> {new_state.name}")

# Using the generic FSM for other applications
from src.finite_state_machine import FiniteStateMachine

# Define your states, alphabet, etc.
states = {'A', 'B', 'C'}
alphabet = {'x', 'y', 'z'}
initial_state = 'A'
final_states = {'C'}
transitions = {
    ('A', 'x'): 'B',
    ('A', 'y'): 'A',
    ('B', 'z'): 'C',
    # ...
}

# Create your custom FSM
custom_fsm = FiniteStateMachine(
    states=states,
    alphabet=alphabet,
    initial_state=initial_state,
    final_states=final_states,
    transition_function=transitions
)

# Process input
result = custom_fsm.process_input('xyz')
```

### Running Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test modules
python -m unittest tests.test_fsm
python -m unittest tests.test_mod_three
```


## Design & Implementation

### Core Components

#### 1. Generic Finite State Machine (`finite_state_machine.py`)

The generic `FiniteStateMachine` class implements the formal definition of a finite automaton as a 5-tuple (Q, Σ, q0, F, δ):

- **States (Q)**: Any hashable objects representing different states
- **Alphabet (Σ)**: Set of valid input symbols
- **Initial State (q0)**: Starting state of the FSM
- **Final States (F)**: Set of accepting/final states
- **Transition Function (δ)**: Maps (state, input) pairs to next states

Key features:
- **Type Safety**: Uses Python's typing module for better IDE support
- **Error Handling**: Custom exception hierarchy for clear error identification:
  - `FSMException`: Base exception class
  - `InvalidStateError`: For invalid state operations
  - `InvalidInputError`: For invalid input symbols
  - `InvalidTransitionError`: For undefined transitions
- **Logging**: Comprehensive logging for debugging and operational insights
- **Flexible Transitions**: Supports both dictionary-based and callable transition functions
- **State History**: Tracks the complete state transition history
- **String Representation**: Human-readable representation for debugging

#### 2. Mod-Three Implementation (`mod_three.py`)

The mod-three solution consists of:

- **ModThreeState Enum**: Defines the three possible states:
  - `S0`: Represents remainder 0
  - `S1`: Represents remainder 1
  - `S2`: Represents remainder 2
  
- **ModThreeFSM Class**: Specialized FSM for the mod-three problem:
  - Uses the generic FSM as its core
  - Implements the specific transition table
  - Provides a clean API for computing remainders
  
- **mod_three Function**: Convenience function for simple usage:
  - Creates a ModThreeFSM instance
  - Computes the remainder
  - Handles validation
  - Returns the result as an integer

Transition table:
| State | Input 0 | Input 1 |
|-------|---------|---------|
| S0    | S0      | S1      |
| S1    | S2      | S0      |
| S2    | S1      | S2      |

### Object-Oriented Design Decisions

The implementation makes several key OOD decisions that shape its architecture and behavior. Here's an analysis of these decisions along with the alternatives that were considered:

#### 1. Generic FSM vs. Problem-Specific Implementation

**Decision:** Create a generic, reusable `FiniteStateMachine` class separate from the mod-three implementation.

**Alternatives:**
- **Single-Class Approach**: Implement the mod-three FSM directly without a generic base.
- **Procedural Approach**: Use functions without classes to implement the FSM logic.

**Rationale:**
- **Reusability**: The generic FSM can be used for other problems beyond mod-three.
- **Separation of Concerns**: Keeps the generic FSM logic separate from problem-specific details.
- **Extensibility**: Makes it easier to implement other FSM-based solutions in the future.
- **Interface Stability**: Changes to the generic FSM implementation won't affect clients as long as the interface remains stable.

#### 2. Composition vs. Inheritance

**Decision:** Use composition in `ModThreeFSM` (contains a `FiniteStateMachine` instance) rather than inheritance.

**Alternatives:**
- **Inheritance**: Extend the `FiniteStateMachine` class to create `ModThreeFSM`.
- **Standalone Implementation**: Create a completely independent implementation.

**Rationale:**
- **Encapsulation**: Provides better encapsulation of the generic FSM's internal details.
- **Interface Control**: Allows `ModThreeFSM` to expose only the methods and properties relevant to the mod-three problem.
- **Delegation**: Can selectively delegate to the contained FSM's methods while adding specific behavior.
- **Flexibility**: Easier to adapt if the generic FSM interface changes.
- **"Has-a" vs. "Is-a"**: A mod-three FSM "has a" finite state machine rather than "is a" finite state machine, making composition more semantically appropriate.

#### 3. State Representation

**Decision:** Use an `Enum` for the states in `ModThreeFSM`.

**Alternatives:**
- **Strings**: Represent states as string literals ('S0', 'S1', 'S2').
- **Integers**: Use integers directly (0, 1, 2) as states.
- **Custom Class**: Create a dedicated `State` class with behavior.

**Rationale:**
- **Type Safety**: Enums provide compile-time type checking and prevent invalid states.
- **Associated Values**: Each enum member has an associated value (the remainder), making the mapping explicit.
- **Self-Documentation**: Enum names make the code more readable and self-documenting.
- **IDE Support**: Better autocomplete and refactoring support in modern IDEs.
- **Debugging**: More meaningful string representations for debugging.

#### 4. Error Handling Strategy

**Decision:** Use a hierarchy of custom exceptions for different error types.

**Alternatives:**
- **Generic Exceptions**: Use Python's built-in exceptions like `ValueError` or `RuntimeError`.
- **Error Codes**: Return error codes or `None` for failure cases.
- **Optional/Maybe Type**: Use Optional or a Maybe-like type to represent potential failure.

**Rationale:**
- **Precise Error Identification**: Custom exceptions allow for more precise identification of error types.
- **Hierarchical Handling**: Enables catching specific exceptions or all FSM-related exceptions at different levels.
- **Rich Error Information**: Can include context-specific information in the exception message.
- **Pythonic Approach**: Following Python's "It's easier to ask forgiveness than permission" (EAFP) style.
- **Client Flexibility**: Allows clients to handle or ignore specific error types as needed.

#### 5. Transition Function Representation

**Decision:** Support both dictionary-based and callable transition functions.

**Alternatives:**
- **Dictionary Only**: Only support a fixed transition table as a dictionary.
- **Function Only**: Only support a function for transitions.
- **Matrix Representation**: Use a 2D matrix/array for the transition table.

**Rationale:**
- **Flexibility**: Different FSM problems may be better suited to different representations.
- **Static vs. Dynamic**: Dictionaries are suitable for static transition tables, while functions can implement dynamic or computed transitions.
- **Simplicity and Performance**: Dictionary lookups are simple and fast for most use cases.
- **Complex Logic**: Functions can implement more complex transition logic when needed.
- **Future-Proofing**: Supports evolving the implementation without breaking the interface.

#### 6. API Design - Functional Interface

**Decision:** Provide both a class-based API (`ModThreeFSM`) and a functional interface (`mod_three`).

**Alternatives:**
- **Class-Only API**: Only expose the `ModThreeFSM` class.
- **Function-Only API**: Only expose the `mod_three` function.

**Rationale:**
- **Usability**: The function provides a simple interface for common use cases.
- **Flexibility**: The class provides access to more advanced features when needed.
- **Progressive Disclosure**: Simple API for simple needs, complex API for complex needs.
- **Different Usage Patterns**: Supports both functional and object-oriented programming styles.
- **Reusability vs. Convenience**: Class for reusable instances, function for one-off calculations.

#### 7. State Tracking and History

**Decision:** Maintain a history of state transitions.

**Alternatives:**
- **Current State Only**: Only track the current state without history.
- **Callback System**: Use callbacks to notify about state changes instead of storing history.

**Rationale:**
- **Debugging**: State history is valuable for debugging and understanding FSM behavior.
- **Auditability**: Provides a record of how the FSM arrived at its current state.
- **Analysis**: Enables post-processing analysis of state transitions.
- **Minimal Overhead**: The storage overhead is minimal for most use cases.
- **Optional Access**: Clients can ignore the history if they don't need it.

### Main Application (`main.py`)

The `main.py` file serves as the entry point for the application with the following functionalities:

1. **Command-Line Interface**: Parses command-line arguments using `argparse`:
   - `--interactive, -i`: Run in interactive mode
   - `--verbose, -v`: Enable verbose logging
   - `--examples-only, -e`: Run only the examples from the assignment
   - `--binary, -b`: Process a specific binary number

2. **Demonstration Modes**:
   - **Examples**: Runs the three examples from the assignment
   - **FSM Usage**: Shows step-by-step operation of the FSM
   - **Interactive Mode**: Allows users to enter their own binary numbers
   - **Single Binary Processing**: Processes a specific binary number

3. **Logging Configuration**: Sets up logging with appropriate level and format

### Demo Module (`mod_three_demo.py`)

Contains demonstration functions that showcase the FSM:

1. **run_examples()**: Runs the three examples from the assignment
2. **demonstrate_fsm_usage()**: Shows detailed state transitions
3. **interactive_mode()**: Provides an interactive prompt for testing
4. **process_single_binary()**: Processes a specific binary number

### Mathematical Basis

The FSM approach for mod-three relies on mathematical properties of binary representation and modular arithmetic:

For a binary number d₍n₎d₍n-1₎...d₍1₎d₍0₎, with value d₍n₎×2ⁿ + d₍n-1₎×2ⁿ⁻¹ + ... + d₍1₎×2¹ + d₍0₎×2⁰:

When calculating modulo 3, we use the property that:
- 2⁰ mod 3 = 1
- 2¹ mod 3 = 2
- 2² mod 3 = 1
- 2³ mod 3 = 2
- ... (the pattern repeats)

This allows processing digits from most to least significant bit while tracking the remainder state according to the transition table.

## Comprehensive Test Suite

The project includes extensive unit tests for both the generic FSM and the mod-three implementation:

### Generic FSM Tests (`test_fsm.py`)

1. **Basic Functionality**:
   - **test_initialization**: Verifies correct initialization
   - **test_process_input**: Tests processing various input sequences
   - **test_process_single_input**: Tests processing single inputs
   - **test_state_history**: Confirms state history tracking
   - **test_reset**: Verifies reset functionality

2. **Error Handling**:
   - **test_initialization_errors**: Tests handling of invalid states
   - **test_error_handling**: Tests handling of invalid inputs

3. **Additional Features**:
   - **test_callable_transition_function**: Tests using a function for transitions
   - **test_string_representations**: Tests string representation methods
   - **test_empty_input**: Tests handling of empty input sequences

### Mod-Three Tests (`test_mod_three.py`)

1. **Basic Functionality**:
   - **test_examples_from_assignment**: Tests the three examples from the assignment
   - **test_single_digits**: Tests single-digit binary numbers
   - **test_two_digits**: Tests all two-digit binary numbers
   - **test_systematic_cases**: Tests binary numbers from 0 to 10
   - **test_all_remainders**: Tests all possible remainders (0, 1, 2)

2. **Edge Cases**:
   - **test_large_numbers**: Tests larger binary numbers
   - **test_leading_zeros**: Tests that leading zeros don't affect results
   - **test_leading_zeros_extensive**: Tests various numbers of leading zeros
   - **test_error_handling**: Tests handling of invalid inputs
   - **test_empty_input**: Tests handling of empty input strings

3. **Special Patterns**:
   - **test_one_zero_alternating_pattern**: Tests alternating 1s and 0s
   - **test_all_ones_pattern**: Tests strings of all 1s
   - **test_all_zeros_with_trailing_one**: Tests powers of 2
   - **test_boundary_values**: Tests powers of 2 and adjacent values

4. **Advanced Testing**:
   - **test_property_based**: Property-based testing with random inputs
   - **test_property_based_function**: Tests the convenience function
   - **test_performance_large_binary**: Tests performance with large inputs






## Author

Muhammad Tariq

