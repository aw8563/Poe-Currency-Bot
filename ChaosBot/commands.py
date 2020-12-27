import pyautogui
import win32clipboard

# closes ingame window with esc
def closeWindow():
    pyautogui.press('esc')

# moves mouse to area and clicks
def click(x, y, ctrl=False, double=False):
    if ctrl:
        pyautogui.keyDown('ctrl')

    pyautogui.moveTo(x, y)
    pyautogui.click()
    if double:
        pyautogui.click()

    if ctrl:
        pyautogui.keyUp('ctrl')

def readItem(x, y):
    # clear previous copied value
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()

    # copy the value
    pyautogui.moveTo(x, y)
    pyautogui.hotkey('ctrl', 'c')

    # return the copied value
    win32clipboard.OpenClipboard()
    return win32clipboard.GetClipboardData() \
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT) else ""
