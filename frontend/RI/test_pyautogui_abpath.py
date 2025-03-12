import pyautogui

# Replace "your_username" with your macOS username (e.g., "john")
screenshot_path = "/Users/aaronxiong/Desktop/test_pyautogui.png"

try:
    pyautogui.screenshot(screenshot_path)
    print(f"Screenshot saved to Desktop: {screenshot_path}")
except Exception as e:
    print(f"Error: {e}")