import os
import urllib.request
import ssl

def download_binaries():
    """
    Downloads pre-built minitouch binaries from DeviceFarmer's stf-binaries repository.
    This repository is the standard source for pre-built minitouch binaries used by STF.
    """
    # Source: https://github.com/openstf/stf-binaries
    base_url = "https://github.com/openstf/stf-binaries/raw/master/node_modules/minitouch-prebuilt/prebuilt"
    
    # Comprehensive list of ABIs supported by minitouch-prebuilt
    abis = [
        "arm64-v8a", 
        "armeabi-v7a", 
        "armeabi", 
        "mips", 
        "mips64", 
        "x86", 
        "x86_64"
    ]
    
    # Target directory inside the package
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_base_dir = os.path.join(script_dir, "airtouch_fast", "binaries")
    
    print("--- Minitouch Binary Downloader ---")
    print(f"Target directory: {target_base_dir}\n")

    # Handle SSL certificate verification issues that sometimes occur on Windows
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    success_count = 0
    for abi in abis:
        abi_dir = os.path.join(target_base_dir, abi)
        os.makedirs(abi_dir, exist_ok=True)
        
        url = f"{base_url}/{abi}/bin/minitouch"
        target_path = os.path.join(abi_dir, "minitouch")
        
        print(f"[*] Downloading {abi.ljust(12)} ... ", end="", flush=True)
        try:
            # Using a custom opener to handle potential SSL issues
            with urllib.request.urlopen(url, context=ctx) as response, open(target_path, 'wb') as out_file:
                out_file.write(response.read())
            
            # Ensure the file has a reasonable size (not a 404 page)
            if os.path.getsize(target_path) < 1000:
                print("FAILED (File too small, possibly invalid)")
                os.remove(target_path)
            else:
                print("DONE")
                success_count += 1
        except Exception as e:
            print(f"FAILED ({type(e).__name__})")
            # Clean up empty/failed files
            if os.path.exists(target_path):
                os.remove(target_path)

    print(f"\n--- Download Complete: {success_count}/{len(abis)} binaries retrieved ---")
    if success_count == 0:
        print("ERROR: No binaries were downloaded. Please check your internet connection.")
    else:
        print("You can now use MinitouchWrapper in your projects.")

if __name__ == "__main__":
    download_binaries()
