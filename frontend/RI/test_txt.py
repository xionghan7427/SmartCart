import subprocess

try:
    # Use macOS's native screenshot tool
    subprocess.run(["screencapture", "test.png"], check=True)
    print("Screenshot saved via macOS CLI!")
except Exception as e:
    print(f"CLI Error: {e}")