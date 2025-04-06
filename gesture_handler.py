import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize Mediapipe Hands solution
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Get screen dimensions for cursor control
screen_width, screen_height = pyautogui.size()

def process_gesture(frame_rgb, frame):
    """
    Processes hand gestures from the given video frame.

    Args:
        frame_rgb: RGB frame from the video feed.
        frame: Original frame for annotation.

    Returns:
        results: Gesture recognition results.
        frame: Annotated frame with UI feedback.
    """
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the landmarks for index and thumb tips
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Convert landmarks to screen coordinates
            index_screen_x = int(index_tip.x * screen_width)
            index_screen_y = int(index_tip.y * screen_height)

            # Display a cursor circle for the index finger
            cv2.circle(frame, (int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])),
                       10, (0, 255, 0), -1)

            # Move the mouse to the index finger position
            pyautogui.moveTo(index_screen_x, index_screen_y)

            # Detect left-click gesture (index-thumb pinch)
            distance = math.sqrt((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2)
            if distance < 0.03:  # Adjust threshold as needed
                pyautogui.click()
                cv2.putText(frame, "Left Click", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Detect right-click gesture (index-middle pinch)
            distance_middle = math.sqrt((index_tip.x - middle_tip.x) ** 2 + (index_tip.y - middle_tip.y) ** 2)
            if distance_middle < 0.03:  # Adjust threshold as needed
                pyautogui.rightClick()
                cv2.putText(frame, "Right Click", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            # Scrolling gesture (three finger up - scroll down and three finger down - scroll up )
            scroll_speed = (index_tip.y - thumb_tip.y) * 50
            if abs(scroll_speed) > 5:  # Sensitivity for scroll detection
                pyautogui.scroll(-int(scroll_speed))
                cv2.putText(frame, "Scrolling", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    return results, frame
