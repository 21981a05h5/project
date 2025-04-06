import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import numpy as np
import math

# Initialize MediaPipe hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Screen dimensions
screen_width, screen_height = pyautogui.size()  

# Voice command recognizer
recognizer = sr.Recognizer()

# Helper function to recognize voice commands
def recognize_voice_command():
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

# Process hand gestures
def process_gesture(results, frame):
    global screen_width, screen_height

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Drawing hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extracting index and thumb tips
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Convert to screen coordinates
            index_screen_x = int(index_tip.x * screen_width)
            index_screen_y = int(index_tip.y * screen_height)
            thumb_screen_x = int(thumb_tip.x * screen_width)
            thumb_screen_y = int(thumb_tip.y * screen_height)

            # Display cursor circle for index finger
            cv2.circle(frame, (int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])), 10, (0, 255, 0), -1)

            # Control the mouse
            pyautogui.moveTo(index_screen_x, index_screen_y)

            # Detect click gesture (distance between index and thumb tips)
            distance = math.sqrt((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2)
            if distance < 0.03:
                pyautogui.click()
                cv2.putText(frame, "Left Click", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Detect right-click (distance between index and middle fingers)
            distance_middle = math.sqrt((index_tip.x - middle_tip.x) ** 2 + (index_tip.y - middle_tip.y) ** 2)
            if distance_middle < 0.03:
                pyautogui.rightClick()
                cv2.putText(frame, "Right Click", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            # Scrolling gesture (vertical index movement)
            scroll_speed = (index_tip.y - thumb_tip.y) * 50
            if abs(scroll_speed) > 5:
                pyautogui.scroll(-int(scroll_speed))
                cv2.putText(frame, "Scrolling", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

# Main program loop
def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame for a mirrored view
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame for hand gestures
        results = hands.process(frame_rgb)
        process_gesture(results, frame)

        # Add UI text
        cv2.putText(frame, "Press 'v' for voice command or 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Display video feed
        cv2.imshow("Gesture Enabled Virtual Mouse", frame)

        # Handle key inputs
        key = cv2.waitKey(1) & 0xFF
        if key == ord('v'):
            # Process voice command
            command = recognize_voice_command()
            if command:
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
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
