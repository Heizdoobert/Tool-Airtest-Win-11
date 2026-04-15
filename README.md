# airtouch-fast 🚀

A high-performance, low-latency touch injection wrapper for Android devices and emulators. Specifically optimized for **Windows 11** and **Airtest** integration, it replaces the default (and often buggy) `minitouch` implementations found in many automation frameworks.

---

## 📋 Table of Contents
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Airtest Integration](#-airtest-integration)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features
- **Ultra-Low Latency**: Direct socket communication with the `minitouch` daemon.
- **Auto-ABI Detection**: Automatically detects device architecture (`x86`, `arm64`, etc.) and pushes the correct binary.
- **Multi-Touch Support**: Full support for multi-finger gestures (pinch, zoom, etc.).
- **Windows Optimized**: Built to handle the specific quirks of ADB and emulators (LDPlayer, Nox, etc.) on Windows 11.
- **Robust Lifecycle**: Automatic ADB port forwarding management and daemon cleanup.

---

## 🛠 Requirements
- **Python**: 3.10 or higher.
- **ADB**: `adb.exe` must be in your system's `PATH`.
- **Android Device**: Physical device or emulator with Developer Options and USB Debugging enabled.

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/airtouch-fast.git
   cd airtouch-fast
   ```

2. **Install the package**:
   ```bash
   pip install -e .
   ```

3. **Download Minitouch Binaries**:
   Minitouch requires architecture-specific binaries. Run the included script to fetch them automatically from the official STF repository:
   ```bash
   python download_binaries.py
   ```

---

## 🚀 Quick Start

```python
from airtouch_fast import MinitouchWrapper

# 1. Initialize (serial is optional if only one device is connected)
mt = MinitouchWrapper(serial="emulator-5554")

# 2. Start the daemon and establish connection
mt.start()

# 3. Perform actions
mt.touch(500, 500)  # Simple tap
mt.swipe((100, 100), (800, 800), duration=0.5)  # Smooth swipe
mt.pinch(center=(500, 500), radius_start=50, radius_end=200)  # Zoom in

# 4. Cleanup
mt.stop()
```

---

## 📖 API Reference

### `MinitouchWrapper(serial=None, bin_path=None)`
- `serial`: The ADB serial of the target device.
- `bin_path`: Custom path to minitouch binaries (defaults to internal `binaries/` folder).

### `.start()`
Pushes the binary, starts the daemon on the device, sets up ADB forwarding, and connects the socket.

### `.stop()`
Closes the socket, removes ADB forwarding, and kills the daemon process on the device.

### `.touch(x, y, pressure=50, duration=None)`
- `x, y`: Coordinates in display pixels.
- `pressure`: Touch pressure (0-100).
- `duration`: If provided, holds the touch for `n` seconds before releasing.

### `.swipe(start_pt, end_pt, duration=0.5, steps=20, pressure=50)`
- `start_pt, end_pt`: `(x, y)` tuples.
- `steps`: Number of intermediate points for the movement.

### `.pinch(center, radius_start, radius_end, duration=0.5, steps=20)`
- `center`: `(x, y)` tuple for the center of the gesture.
- `radius_start`: Initial distance of fingers from center.
- `radius_end`: Final distance of fingers from center (Zoom in if `end > start`).

---

## 🔗 Airtest Integration

To use `airtouch-fast` as a high-performance replacement for Airtest's default touch:

```python
from airtest.core.api import *
from airtouch_fast import MinitouchWrapper

# Connect to device via Airtest
auto_setup(__file__)
dev = device()

# Initialize and start Minitouch
mt = MinitouchWrapper(dev.serialno)
mt.start()

# Replace standard touch calls
# Instead of touch((500, 500)), use:
mt.touch(500, 500)
```

---

## ⚙️ Technical Details

### Coordinate Mapping
Minitouch often uses a different coordinate space than the display resolution (e.g., `0-32767` vs `0-1080`). This wrapper automatically:
1. Queries the device resolution using `wm size`.
2. Parses the minitouch header for its max coordinate values.
3. Maps your pixel-based inputs to the minitouch space accurately.

### Protocol Implementation
The wrapper communicates via the standard minitouch text protocol:
- `d <contact> <x> <y> <pressure>`: Down
- `m <contact> <x> <y> <pressure>`: Move
- `u <contact>`: Up
- `c`: Commit (executes the queued commands)

---

## ❓ Troubleshooting

- **"Minitouch binary not found"**: Ensure you have run `python download_binaries.py`.
- **"ADB command failed"**: Check if your device is connected (`adb devices`) and that `adb.exe` is in your PATH.
- **Permission Denied**: The wrapper attempts to `chmod 755` the binary. On some highly secured devices, you may need to push to a different directory than `/data/local/tmp`.
- **Coordinates Offset**: If touches are hitting the wrong spot, verify if your emulator has "High DPI" settings enabled, which can sometimes interfere with `wm size` reporting.

---

## 📜 License
Apache-2.0
