import cv2
import time
from gesture_handler import process_gesture
from voice_handler import *  # Corrected import
from ui_utils import add_ui_effects

def main():
    """
    Main function for running the gesture-enabled virtual mouse
    and voice-activated tool.
    """
    # Start video capture
    cap = cv2.VideoCapture(0)
    prev_time = 0
    fps = 0

    print("Starting Virtual Mouse and Voice Assistant...")
    print("Press 'q' to exit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip frame horizontally for a mirror view
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Gesture processing
        results, annotated_frame = process_gesture(frame_rgb, frame)

        # # Calculate FPS
        # curr_time = time.time()
        # fps = 1 / (curr_time - prev_time)
        # prev_time = curr_time

        # Add UI effects (FPS and animations)
        annotated_frame = add_ui_effects(annotated_frame,  gesture_text="Gesture Enabled") # , fps=fps)

        cv2.putText(annotated_frame, "Press 'v' for voice command or 'q' to quit", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        # Display the annotated frame
        cv2.imshow('Gesture and Voice Assistant', annotated_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('v'):
            # Process voice command
            command = recognize_voice_command()
            if command:
                execute_command(command)
        elif key == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
