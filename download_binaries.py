import os
import urllib.request
import ssl

def download_binaries():
    """
    Downloads pre-built minitouch binaries from the AirtestProject repository.
    This is a highly reliable source as it is actively maintained.
    """
    # AirtestProject provides a comprehensive set of stf-binaries
    base_url = "https://raw.githubusercontent.com/AirtestProject/Airtest/master/airtest/core/android/static/stf_libs"
    
    # Standard ABIs supported
    abis = ["arm64-v8a", "armeabi-v7a", "armeabi", "x86", "x86_64", "mips", "mips64"]
    
    # Target directory inside the package
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_base_dir = os.path.join(script_dir, "airtouch_fast", "binaries")
    
    print("--- Minitouch Binary Downloader ---")
    print(f"Target directory: {target_base_dir}\n")

    # Handle SSL certificate verification issues
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    success_count = 0
    for abi in abis:
        abi_dir = os.path.join(target_base_dir, abi)
        os.makedirs(abi_dir, exist_ok=True)
        
        # Airtest structure: stf_libs/<abi>/minitouch
        url = f"{base_url}/{abi}/minitouch"
        target_path = os.path.join(abi_dir, "minitouch")
        
        print(f"[*] Downloading {abi.ljust(12)} ... ", end="", flush=True)
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            )
            
            with urllib.request.urlopen(req, context=ctx) as response:
                content = response.read()
                if len(content) > 1000:
                    with open(target_path, 'wb') as out_file:
                        out_file.write(content)
                    print("DONE")
                    success_count += 1
                else:
                    print("FAILED (File too small)")
        except Exception as e:
            print(f"FAILED ({e})")

    print(f"\n--- Download Complete: {success_count}/{len(abis)} binaries retrieved ---")
    if success_count == 0:
        print("ERROR: No binaries were downloaded. Please check your internet connection.")
    else:
        print("You can now use MinitouchWrapper in your projects.")

if __name__ == "__main__":
    download_binaries()
