import subprocess
import os
import re

def run_adb_command(cmd, serial=None):
    """Executes an ADB command and returns the output."""
    adb_cmd = ["adb"]
    if serial:
        adb_cmd.extend(["-s", serial])
    
    if isinstance(cmd, str):
        adb_cmd.extend(cmd.split())
    else:
        adb_cmd.extend(cmd)
    
    try:
        result = subprocess.run(adb_cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ADB command failed: {' '.join(adb_cmd)}\nError: {e.stderr}")

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
