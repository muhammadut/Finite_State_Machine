"""
Unit tests for the Mod-Three FSM implementation.

This module contains comprehensive tests for the ModThreeFSM class and mod_three function.

Author: Muhammad Tariq
Date: 2025-05-04
"""

import unittest
import time
import random
from src.mod_three import ModThreeFSM, mod_three


class TestModThreeFSM(unittest.TestCase):
    """Test cases for the ModThreeFSM implementation."""
    
    def setUp(self):
        """Set up a ModThreeFSM instance for each test."""
        self.fsm = ModThreeFSM()
    
    def test_examples_from_assignment(self):
        """Test the examples provided in the assignment."""
        # Example 1: '1101' -> 1
        self.assertEqual(self.fsm.compute_remainder('1101'), 1)
        
        # Example 2: '1110' -> 2
        self.fsm.reset()
        self.assertEqual(self.fsm.compute_remainder('1110'), 2)
        
        # Example 3: '1111' -> 0
        self.fsm.reset()
        self.assertEqual(self.fsm.compute_remainder('1111'), 0)
    
    def test_single_digits(self):
        """Test single-digit binary numbers."""
        # '0' = 0 in decimal, 0 mod 3 = 0
        self.assertEqual(self.fsm.compute_remainder('0'), 0)
        
        # '1' = 1 in decimal, 1 mod 3 = 1
        self.fsm.reset()
        self.assertEqual(self.fsm.compute_remainder('1'), 1)
    
    def test_two_digits(self):
        """Test two-digit binary numbers."""
        # '00' = 0 in decimal, 0 mod 3 = 0
        self.assertEqual(self.fsm.compute_remainder('00'), 0)
        
        # '01' = 1 in decimal, 1 mod 3 = 1
        self.fsm.reset()
        self.assertEqual(self.fsm.compute_remainder('01'), 1)
        
        # '10' = 2 in decimal, 2 mod 3 = 2
        self.fsm.reset()
        self.assertEqual(self.fsm.compute_remainder('10'), 2)
        
        # '11' = 3 in decimal, 3 mod 3 = 0
        self.fsm.reset()
        self.assertEqual(self.fsm.compute_remainder('11'), 0)
    
    def test_systematic_cases(self):
        """Test all binary numbers from 0 to 10."""
        test_cases = [
            ('0', 0),     # 0 mod 3 = 0
            ('1', 1),     # 1 mod 3 = 1
            ('10', 2),    # 2 mod 3 = 2
            ('11', 0),    # 3 mod 3 = 0
            ('100', 1),   # 4 mod 3 = 1
            ('101', 2),   # 5 mod 3 = 2
            ('110', 0),   # 6 mod 3 = 0
            ('111', 1),   # 7 mod 3 = 1
            ('1000', 2),  # 8 mod 3 = 2
            ('1001', 0),  # 9 mod 3 = 0
            ('1010', 1),  # 10 mod 3 = 1
        ]
        
        for binary, expected in test_cases:
            self.fsm.reset()
            self.assertEqual(
                self.fsm.compute_remainder(binary), 
                expected, 
                f"Failed for {binary} (decimal {int(binary, 2)})"
            )
    
    def test_large_numbers(self):
        """Test larger binary numbers."""
        # 1023 (all 1's) = 0 mod 3
        self.assertEqual(self.fsm.compute_remainder('1111111111'), 0)
        
        # 1024 (power of 2) = 1 mod 3
        self.fsm.reset()
        self.assertEqual(self.fsm.compute_remainder('10000000000'), 1)
        
        # A large number that should have remainder 2
        self.fsm.reset()
        self.assertEqual(self.fsm.compute_remainder('10000000001'), 2)
    
    def test_leading_zeros(self):
        """Test that leading zeros don't affect the result."""
        # Without leading zeros
        remainder = self.fsm.compute_remainder('101')
        
        # With leading zeros
        self.fsm.reset()
        remainder_with_zeros = self.fsm.compute_remainder('000101')
        
        self.assertEqual(remainder, remainder_with_zeros)
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Empty string
        with self.assertRaises(ValueError):
            self.fsm.compute_remainder('')
        
        # Invalid characters
        with self.assertRaises(ValueError):
            self.fsm.compute_remainder('1201')
            
        with self.assertRaises(ValueError):
            self.fsm.compute_remainder('abc')
    
    def test_property_based(self):
        """
        Property-based test: For any binary number, the FSM result should match 
        the decimal value mod 3.
        
        This test generates random binary strings and verifies that the FSM 
        result matches the traditional modulo operation on the decimal value.
        """
        # Number of test cases to generate
        num_tests = 100
        
        # Maximum length of binary strings to test
        max_length = 30
        
        for _ in range(num_tests):
            # Generate a random binary string
            length = random.randint(1, max_length)
            binary = ''.join(random.choice('01') for _ in range(length))
            
            # Calculate expected result using traditional modulo
            decimal = int(binary, 2)
            expected = decimal % 3
            
            # Calculate result using FSM
            self.fsm.reset()
            fsm_result = self.fsm.compute_remainder(binary)
            
            # Verify the implementation matches the expected result
            self.assertEqual(
                fsm_result, 
                expected, 
                f"Failed for {binary} (decimal {decimal}): FSM result {fsm_result} != expected {expected}"
            )
    
    def test_leading_zeros_extensive(self):
        """
        More extensive testing for leading zeros to ensure they don't affect results.
        Tests with various numbers of leading zeros.
        """
        test_cases = [
            ('101', 2),      # Base value
            ('0101', 2),     # One leading zero
            ('00101', 2),    # Two leading zeros
            ('000101', 2),   # Three leading zeros
            ('0000000101', 2)  # Many leading zeros
        ]
        
        for binary, expected in test_cases:
            self.fsm.reset()
            result = self.fsm.compute_remainder(binary)
            self.assertEqual(
                result, 
                expected, 
                f"Failed for {binary}: expected {expected}, got {result}"
            )
    
    def test_performance_large_binary(self):
        """
        Test performance with very large binary strings.
        
        This test ensures the FSM approach remains efficient for large inputs.
        It also verifies correctness for large values.
        """
        # Test with binary strings of increasing length
        lengths = [100, 1000]
        
        for length in lengths:
            # Generate a random binary string of the specified length
            binary = ''.join(random.choice('01') for _ in range(length))
            
            # Time the FSM computation
            start_time = time.time()
            fsm_result = mod_three(binary)
            fsm_time = time.time() - start_time
            
            # Calculate modulo 3 using the built-in int function for verification
            decimal = int(binary, 2)
            expected = decimal % 3
            
            # Verify correctness
            self.assertEqual(
                fsm_result, 
                expected, 
                f"Failed for binary string of length {length}"
            )
            
            # Log performance information
            print(f"Length {length}: Processed in {fsm_time:.6f} seconds")
            
            # Performance assertion - should be reasonably fast even for large strings
            self.assertLess(fsm_time, 1.0, f"Processing a {length}-digit binary took too long: {fsm_time:.6f}s")
    
    def test_one_zero_alternating_pattern(self):
        """
        Test binary strings with alternating 1s and 0s.
        
        This pattern can be tricky for some FSM implementations because
        it maximizes state transitions.
        """
        test_cases = [
            ('10', 2),         # 2 in decimal
            ('1010', 10),      # 10 in decimal
            ('101010', 42),    # 42 in decimal
            ('10101010', 170)  # 170 in decimal
        ]
        
        for binary, decimal in test_cases:
            self.fsm.reset()
            result = self.fsm.compute_remainder(binary)
            expected = decimal % 3
            self.assertEqual(
                result, 
                expected, 
                f"Failed for {binary} (decimal {decimal}): expected {expected}, got {result}"
            )
    
    def test_all_ones_pattern(self):
        """
        Test binary strings of all 1s of different lengths.
        
        For all 1s, the pattern of remainders when divided by 3 follows
        a cycle: 1, 3, 7, 15, 31, ... which mod 3 gives: 1, 0, 1, 0, ...
        """
        # Generate strings of all 1s with different lengths
        for length in range(1, 20):
            binary = '1' * length
            decimal = int(binary, 2)
            expected = decimal % 3
            
            self.fsm.reset()
            result = self.fsm.compute_remainder(binary)
            
            self.assertEqual(
                result, 
                expected, 
                f"Failed for {binary} (decimal {decimal}): expected {expected}, got {result}"
            )
    
    def test_all_zeros_with_trailing_one(self):
        """
        Test binary strings with many zeros followed by a single 1.
        
        These represent powers of 2, and the pattern of remainders when 
        divided by 3 follows a cycle: 1, 2, 1, 2, ...
        """
        for zeros in range(10):
            binary = '0' * zeros + '1'
            decimal = int(binary, 2)
            expected = decimal % 3
            
            self.fsm.reset()
            result = self.fsm.compute_remainder(binary)
            
            self.assertEqual(
                result, 
                expected, 
                f"Failed for {binary} (decimal {decimal}): expected {expected}, got {result}"
            )
    
    def test_boundary_values(self):
        """
        Test boundary values that might be problematic.
        
        These include powers of 2 and values close to powers of 2.
        """
        # Powers of 2
        for power in range(20):
            decimal = 2 ** power
            binary = bin(decimal)[2:]  # Convert to binary without '0b' prefix
            expected = decimal % 3
            
            self.fsm.reset()
            result = self.fsm.compute_remainder(binary)
            
            self.assertEqual(
                result, 
                expected, 
                f"Failed for 2^{power} = {decimal} (binary {binary}): expected {expected}, got {result}"
            )
            
        # Powers of 2 minus 1 (all 1s up to a certain length)
        for power in range(1, 20):
            decimal = 2 ** power - 1
            binary = bin(decimal)[2:]  # Convert to binary without '0b' prefix
            expected = decimal % 3
            
            self.fsm.reset()
            result = self.fsm.compute_remainder(binary)
            
            self.assertEqual(
                result, 
                expected, 
                f"Failed for 2^{power}-1 = {decimal} (binary {binary}): expected {expected}, got {result}"
            )
            
        # Powers of 2 plus 1
        for power in range(20):
            decimal = 2 ** power + 1
            binary = bin(decimal)[2:]  # Convert to binary without '0b' prefix
            expected = decimal % 3
            
            self.fsm.reset()
            result = self.fsm.compute_remainder(binary)
            
            self.assertEqual(
                result, 
                expected, 
                f"Failed for 2^{power}+1 = {decimal} (binary {binary}): expected {expected}, got {result}"
            )


class TestModThreeFunction(unittest.TestCase):
    """Test cases for the convenience function mod_three."""
    
    def test_examples_from_assignment(self):
        """Test the examples provided in the assignment."""
        self.assertEqual(mod_three('1101'), 1)
        self.assertEqual(mod_three('1110'), 2)
        self.assertEqual(mod_three('1111'), 0)
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Empty string
        with self.assertRaises(ValueError):
            mod_three('')
        
        # Invalid characters
        with self.assertRaises(ValueError):
            mod_three('1201')
            
        with self.assertRaises(ValueError):
            mod_three('abc')
    
    def test_all_remainders(self):
        """Test that we get all possible remainders (0, 1, 2)."""
        self.assertEqual(mod_three('11'), 0)   # 3 mod 3 = 0
        self.assertEqual(mod_three('1'), 1)    # 1 mod 3 = 1
        self.assertEqual(mod_three('10'), 2)   # 2 mod 3 = 2
        
    def test_property_based_function(self):
        """
        Property-based test for the mod_three function.
        
        Generates random binary strings and verifies that the function result
        matches the expected modulo 3 value.
        """
        # Number of test cases to generate
        num_tests = 50
        
        # Maximum length of binary strings to test
        max_length = 20
        
        for _ in range(num_tests):
            # Generate a random binary string
            length = random.randint(1, max_length)
            binary = ''.join(random.choice('01') for _ in range(length))
            
            # Calculate expected result using traditional modulo
            decimal = int(binary, 2)
            expected = decimal % 3
            
            # Calculate result using the convenience function
            result = mod_three(binary)
            
            # Verify the implementation matches the expected result
            self.assertEqual(
                result, 
                expected, 
                f"Failed for {binary} (decimal {decimal}): mod_three() result {result} != expected {expected}"
            )


if __name__ == '__main__':
    unittest.main()