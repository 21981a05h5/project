import pyautogui
import speech_recognition as sr

recognizer = sr.Recognizer()

def recognize_voice_command():
    """
    Recognizes voice commands using the microphone.
    Returns:
        command (str): Recognized command as a string.
    """
    with sr.Microphone() as source:
        print("Listening for voice commands...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"Voice command recognized: {command}")
            return command
        except Exception as e:
            print(f"Error recognizing command: {e}")
    return None

def execute_command(command):
    """
    Executes actions based on the voice command.
    
    Args:
        command (str): The voice command to execute.
    """
    if "notepad" in command:
        pyautogui.hotkey("win", "r")
        pyautogui.typewrite("notepad")
        pyautogui.press("enter")
    elif "chrome" in command:
        pyautogui.hotkey("win", "r")
        pyautogui.typewrite("chrome")
        pyautogui.press("enter")
    elif "calculator" in command:
        pyautogui.hotkey("win", "r")
        pyautogui.typewrite("calc")
        pyautogui.press("enter")
    elif "volume up" in command:
        pyautogui.press("volumeup", presses=5)
    elif "volume down" in command:
        pyautogui.press("volumedown", presses=5)
    elif "mute" in command:
        pyautogui.press("volumemute")
    elif "close" in command:
        pyautogui.hotkey("alt", "f4")
    else:
        print(f"Unknown command: {command}")
