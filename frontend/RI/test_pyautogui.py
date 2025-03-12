import pyautogui

# Force PyAutoGUI to use macOS's native screencapture tool
pyautogui._pyautogui_osx._screenshot = pyautogui._pyautogui_osx._screenshot_via_screencapture

try:
    pyautogui.screenshot("test_pyautogui.png")
    print("Screenshot saved using macOS native tool!")
except Exception as e:
    print(f"Error: {e}")