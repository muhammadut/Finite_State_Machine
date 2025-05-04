"""
Unit tests for the Mod-Three FSM implementation.

This module contains comprehensive tests for the ModThreeFSM class and mod_three function.

Author: FAANG Tech Lead
"""

import unittest
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


if __name__ == '__main__':
    unittest.main()