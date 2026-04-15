import unittest
import time
import os
import sys
from airtouch_fast import MinitouchWrapper, set_adb_path
from airtouch_fast.utils import get_devices, run_adb_command

class TestAirtouchFast(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure ADB is accessible
        try:
            run_adb_command("version")
        except Exception as e:
            print(f"Error: ADB not found. {e}")
            sys.exit(1)
            
        # Check for connected devices
        cls.devices = get_devices()
        if not cls.devices:
            print("Warning: No Android devices connected. Skipping functional tests.")
            cls.skip_functional = True
        else:
            cls.skip_functional = False
            cls.serial = cls.devices[0]
            print(f"Testing with device: {cls.serial}")

    def test_01_device_detection(self):
        """Test if devices can be detected."""
        devices = get_devices()
        self.assertIsInstance(devices, list)
        print(f"Detected devices: {devices}")

    def test_02_wrapper_initialization(self):
        """Test wrapper init and binary detection."""
        if self.skip_functional:
            self.skipTest("No device connected")
            
        mt = MinitouchWrapper(serial=self.serial)
        self.assertEqual(mt.serial, self.serial)
        
        # Check if we can get ABI
        from airtouch_fast.utils import get_abi
        abi = get_abi(self.serial)
        self.assertIsNotNone(abi)
        print(f"Device ABI: {abi}")

    def test_03_full_lifecycle(self):
        """Test start, touch, and stop lifecycle."""
        if self.skip_functional:
            self.skipTest("No device connected")
            
        mt = MinitouchWrapper(serial=self.serial)
        try:
            print("Starting minitouch daemon...")
            mt.start()
            self.assertTrue(mt._running)
            self.assertIsNotNone(mt.max_x)
            
            print(f"Performing test tap at (500, 500) on {self.serial}...")
            mt.touch(500, 500)
            
            print("Performing test swipe...")
            mt.swipe((100, 100), (800, 800), duration=0.3)
            
            print("Stopping minitouch...")
            mt.stop()
            self.assertFalse(mt._running)
        except Exception as e:
            mt.stop()
            self.fail(f"Lifecycle test failed: {e}")

if __name__ == "__main__":
    unittest.main()
