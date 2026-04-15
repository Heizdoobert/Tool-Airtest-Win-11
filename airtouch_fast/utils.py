import subprocess
import os
import re
import time

# Global ADB path, can be overridden by the user
ADB_PATH = "adb"

ADB_ERROR_SOLUTIONS = {
    "unauthorized": "Device unauthorized. Please check the 'Allow USB debugging' dialog on your device.",
    "offline": "Device is offline. Try reconnecting the USB cable or restarting the emulator.",
    "device not found": "Device not found. Ensure the device is connected and 'adb devices' shows it.",
    "no devices": "No devices found. Ensure your device is connected and USB debugging is enabled.",
    "multiple devices": "Multiple devices connected. Please specify a serial number using the 'serial' parameter.",
    "more than one": "Multiple devices connected. Please specify a serial number using the 'serial' parameter.",
    "permission denied": "Permission denied. Ensure you have the necessary permissions to execute commands on the device.",
    "protocol fault": "ADB protocol fault. This is often a transient issue, retrying...",
}

def set_adb_path(path):
    """Sets the path to the adb executable."""
    global ADB_PATH
    ADB_PATH = path

def run_adb_command(cmd, serial=None, retries=3, delay=1):
    """Executes an ADB command with automatic retries and enhanced error handling."""
    adb_cmd = [ADB_PATH]
    if serial:
        adb_cmd.extend(["-s", serial])
    
    if isinstance(cmd, str):
        adb_cmd.extend(cmd.split())
    else:
        adb_cmd.extend(cmd)
    
    last_error = ""
    for attempt in range(retries):
        try:
            result = subprocess.run(adb_cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except FileNotFoundError:
            raise RuntimeError(f"ADB executable not found at '{ADB_PATH}'. Please ensure ADB is installed and in your PATH, or set it using set_adb_path().")
        except subprocess.CalledProcessError as e:
            last_error = e.stderr.lower()
            
            # Check for specific known errors that don't benefit from retries
            # Note: 'protocol fault' is in the list but we might want to retry it, 
            # so we handle it specially if needed.
            for error_key, solution in ADB_ERROR_SOLUTIONS.items():
                if error_key in last_error:
                    if error_key == "protocol fault":
                        # This one is worth retrying
                        break
                    raise RuntimeError(f"ADB Error: {solution}\n(Raw error: {e.stderr.strip()})")
            
            # If it's the last attempt, raise the error
            if attempt == retries - 1:
                raise RuntimeError(f"ADB command failed after {retries} attempts: {' '.join(adb_cmd)}\nError: {e.stderr.strip()}")
            
            # Wait before retrying for transient issues
            time.sleep(delay)
    
    return ""

def get_devices():
    """Returns a list of connected device serials."""
    output = run_adb_command("devices")
    devices = []
    for line in output.splitlines():
        if line.endswith("\tdevice"):
            devices.append(line.split("\t")[0])
    return devices

def get_abi(serial=None):
    """Detects the device CPU ABI."""
    return run_adb_command("shell getprop ro.product.cpu.abi", serial)

def get_display_info(serial=None):
    """Gets the display resolution using wm size."""
    output = run_adb_command("shell wm size", serial)
    match = re.search(r"(\d+)x(\d+)", output)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def push_file(local_path, remote_path, serial=None):
    """Pushes a file to the device."""
    run_adb_command(["push", local_path, remote_path], serial)

def chmod(remote_path, mode="755", serial=None):
    """Changes file permissions on the device."""
    run_adb_command(["shell", "chmod", mode, remote_path], serial)

def is_process_running(process_name, serial=None):
    """Checks if a process is running on the device."""
    try:
        output = run_adb_command(["shell", "ps", "-A"], serial)
        return process_name in output
    except:
        return False
