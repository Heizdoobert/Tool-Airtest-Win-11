import os
import urllib.request
import zipfile
import shutil

def download_binaries():
    """Downloads pre-built minitouch binaries from DeviceFarmer's GitHub."""
    # Note: DeviceFarmer doesn't provide a single zip of all binaries in a simple way 
    # that matches our structure directly, but we can fetch them.
    # For this implementation, we'll guide the user or provide a helper.
    
    base_url = "https://github.com/openstf/stf-binaries/raw/master/node_modules/minitouch-prebuilt/prebuilt"
    abis = ["arm64-v8a", "armeabi-v7a", "x86", "x86_64"]
    
    target_dir = os.path.join(os.path.dirname(__file__), "airtouch_fast", "binaries")
    
    for abi in abis:
        abi_dir = os.path.join(target_dir, abi)
        os.makedirs(abi_dir, exist_ok=True)
        
        url = f"{base_url}/{abi}/bin/minitouch"
        target_path = os.path.join(abi_dir, "minitouch")
        
        print(f"Downloading {abi} binary...")
        try:
            urllib.request.urlretrieve(url, target_path)
            print(f"Successfully downloaded to {target_path}")
        except Exception as e:
            print(f"Failed to download {abi}: {e}")

if __name__ == "__main__":
    download_binaries()
