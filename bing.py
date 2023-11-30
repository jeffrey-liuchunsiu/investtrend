import pyautogui
import time

while True:
    # Delay before executing the click and keystrokes
    time.sleep(10)

    # Simulate a mouse click
    pyautogui.click()

    # Simulate typing "a" and press Enter
    pyautogui.typewrite('a')
    pyautogui.press('enter')
    