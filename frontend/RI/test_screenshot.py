import pyautogui
import os
print("Current directory:", os.getcwd())

try:
    screenshot = pyautogui.screenshot("test_pyautogui.png")
    print("Screenshot saved using PyAutoGUI!")
except Exception as e:
    print(f"Error: {e}")