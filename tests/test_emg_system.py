#!/usr/bin/env python3
"""
Unit tests for EMG Robotic Arm System
"""

import sys
import os
import unittest
import time

# Add the parent directory to the path to import the modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Python'))

from emg_robotic_arm import EMGSignal, Joint, Gesture, EMGProcessor, RoboticArm, EMGSimulator

class TestEMGSignal(unittest.TestCase):
    """Test EMG Signal functionality"""
    
    def test_emg_signal_creation(self):
        """Test EMG signal creation"""
        signal = EMGSignal(0.5, 30.0)
        self.assertEqual(signal.amplitude, 0.5)
        self.assertEqual(signal.frequency, 30.0)
        self.assertIsInstance(signal.timestamp, float)

if __name__ == '__main__':
    unittest.main()
