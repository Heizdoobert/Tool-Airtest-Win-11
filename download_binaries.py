import os
import urllib.request
import ssl

def download_binaries():
    """
    Downloads pre-built minitouch binaries from GitHub.
    Tries multiple organizations, repositories, branches, and paths.
    """
    sources = [
        {"org": "openstf", "repo": "stf-binaries"},
        {"org": "DeviceFarmer", "repo": "stf-binaries"},
        {"org": "openstf", "repo": "minitouch-prebuilt"},
        {"org": "DeviceFarmer", "repo": "minitouch-prebuilt"},
        {"org": "AirtestProject", "repo": "Airtest"},
        {"org": "openstf", "repo": "minitouch"},
        {"org": "DeviceFarmer", "repo": "minitouch"},
        {"org": "stf-binaries", "repo": "stf-binaries"}
    ]
    branches = ["master", "main", "devel", "prebuilt"]
    paths = [
        "node_modules/minitouch-prebuilt/prebuilt/{abi}/bin/minitouch",
        "node_modules/@openstf/minitouch-prebuilt/prebuilt/{abi}/bin/minitouch",
        "prebuilt/{abi}/bin/minitouch",
        "bin/{abi}/minitouch",
        "{abi}/bin/minitouch",
        "libs/{abi}/minitouch",
        "airtest/core/android/static/bin/minitouch/{abi}/minitouch",
        "dist/minitouch/{abi}/minitouch"
    ]
    # Standard ABIs usually available in the prebuilt package
    abis = ["arm64-v8a", "armeabi-v7a", "armeabi", "x86", "x86_64"]
    
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
        target_path = os.path.join(abi_dir, "minitouch")
        
        downloaded = False
        print(f"[*] Downloading {abi.ljust(12)} ... ", end="", flush=True)
        
        for source in sources:
            org = source["org"]
            repo = source["repo"]
            for branch in branches:
                for path_template in paths:
                    path = path_template.format(abi=abi)
                    url = f"https://raw.githubusercontent.com/{org}/{repo}/{branch}/{path}"
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
                                print(f"DONE ({org}/{repo}/{branch})")
                                success_count += 1
                                downloaded = True
                                break
                    except Exception:
                        continue
                if downloaded:
                    break
            if downloaded:
                break
        
        if not downloaded:
            print("FAILED (All variations tried)")

    print(f"\n--- Download Complete: {success_count}/{len(abis)} binaries retrieved ---")
    if success_count == 0:
        print("ERROR: No binaries were downloaded. The repository structure might have changed.")
        print("Please manually download binaries from:")
        print("1. https://github.com/openstf/stf-binaries")
        print("2. https://github.com/DeviceFarmer/stf-binaries")
        print("And place them in airtouch_fast/binaries/<abi>/minitouch")
    else:
        print("You can now use MinitouchWrapper in your projects.")

if __name__ == "__main__":
    download_binaries()
