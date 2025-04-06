import cv2
import numpy as np

def add_ui_effects(frame, fps=None, gesture_text=None):
    """
    Add subtle UI animations and effects to the video frame.

    Args:
        frame: Original video frame.
        fps: Frames per second to display (optional).
        gesture_text: Gesture feedback to display (optional).

    Returns:
        frame: Annotated video frame with UI effects.
    """
    height, width, _ = frame.shape

    # Add a semi-transparent overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (width, 50), (0, 0, 0), -1)  # Top bar
    cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

    # Display FPS
    if fps is not None:
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Add gesture text animation
    if gesture_text:
        # Create a pulsating effect for gesture feedback
        pulsating_color = (0, 255, int((1 + np.sin(cv2.getTickCount() / cv2.getTickFrequency())) * 127))
        cv2.putText(frame, gesture_text, (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, pulsating_color, 2)

    # Draw a subtle glowing cursor for better feedback
    cursor_radius = 15 + int(5 * np.sin(cv2.getTickCount() / cv2.getTickFrequency()))
    cursor_color = (0, 255, 0)
    cv2.circle(frame, (width - 50, height - 50), cursor_radius, cursor_color, 2)

    return frame
