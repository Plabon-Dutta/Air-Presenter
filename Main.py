import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1)  # We only need to track one hand

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Get screen dimensions
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Settings
gesture_cooldown = 1.0  # Time in seconds between gestures
horizontal_threshold = 0.15  # Horizontal movement threshold (as percentage of screen width)
movement_threshold = 10  # Convert to pixel distance
boundary_line_y = frame_height - 0  # Horizontal line at the middle of the screen

# Variables to track hand movement
previous_wrist_x = None
last_gesture_time = time.time() - gesture_cooldown
gesture_direction = None
c = 0

# Stats for debugging
frame_count = 0
fps_start_time = time.time()
fps = 0

print("Hand Gesture PowerPoint Control - Above Line Only")
print("-------------------------------------")
print("Move your right hand from right to left ABOVE the line for NEXT slide")
print("Move your right hand from left to right ABOVE the line for PREVIOUS slide")
print("Hand gestures below the line will be ignored")
print("Press 'q' to quit")

try:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Error: Failed to grab frame")
            break
            
        # Flip the image horizontally for a more intuitive experience
        image = cv2.flip(image, 1)
        
        # Update FPS counter
        frame_count += 1
        if frame_count >= 10:
            current_time = time.time()
            fps = frame_count / (current_time - fps_start_time)
            fps_start_time = current_time
            frame_count = 0
        
        # Convert the image to RGB and process with MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        
        # Draw the horizontal boundary line
        cv2.line(image, (0, boundary_line_y), (frame_width, boundary_line_y), (0, 0, 255), 2)
        
        # Add text to indicate active and inactive zones
        cv2.putText(image, "ACTIVE ZONE", (10, boundary_line_y - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, "INACTIVE ZONE", (10, boundary_line_y + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128, 128, 128), 2)
        
        # Draw status on screen
        cv2.putText(image, "Hand Gesture PowerPoint Control", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(image, f"FPS: {fps:.1f}", (frame_width - 120, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display cooldown timer if active
        cooldown_remaining = max(0, gesture_cooldown - (time.time() - last_gesture_time))
        if cooldown_remaining > 0:
            cv2.putText(image, f"Cooldown: {cooldown_remaining:.1f}s", (frame_width - 200, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # If gesture was recently detected, show what it was
        if gesture_direction and time.time() - last_gesture_time < 2:
            cv2.putText(image, f"Detected: {gesture_direction}", (frame_width // 2 - 100, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Process hand landmarks if detected
        hand_above_line = False
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks for visualization
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                # Get wrist position (landmark 0)
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                wrist_x = int(wrist.x * image.shape[1])
                wrist_y = int(wrist.y * image.shape[0])
                
                # Check if the hand is above the boundary line
                if wrist_y < boundary_line_y:
                    hand_above_line = True
                    # Draw a green circle at the wrist when above the line
                    cv2.circle(image, (wrist_x, wrist_y), 8, (0, 255, 0), -1)
                else:
                    # Draw a gray circle at the wrist when below the line
                    cv2.circle(image, (wrist_x, wrist_y), 8, (128, 128, 128), -1)
                
                # Only process gestures when hand is above the line
                if hand_above_line:
                    # Check if we have a previous position to compare
                    if previous_wrist_x is not None and previous_wrist_y is not None:
                        # Only compare if the previous position was also above the line
                        if previous_wrist_y < boundary_line_y:
                            # Calculate horizontal movement
                            movement_x = wrist_x - previous_wrist_x
                            
                            # Draw a line showing the movement
                            cv2.line(image, (previous_wrist_x, previous_wrist_y), 
                                    (wrist_x, wrist_y), (0, 255, 0), 2)
                            
                            # Show movement amount
                            cv2.putText(image, f"Movement: {movement_x}", (10, 60), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            
                            # Check if enough time has passed since last gesture
                            current_time = time.time()
                            if current_time - last_gesture_time > gesture_cooldown:
                                # Check if the movement exceeds the threshold
                                flag = False
                                if abs(movement_x) > movement_threshold and flag == False:
                                    if movement_x > 0:
                                        # Movement to the right (in flipped frame) - Previous slide
                                        print("Detected: Previous slide gesture")
                                        pyautogui.press('left')
                                        gesture_direction = "PREVIOUS slide"
                                        last_gesture_time = current_time
                                        flag = True
                                    else:
                                        # Movement to the left (in flipped frame) - Next slide
                                        print("Detected: Next slide gesture")
                                        pyautogui.press('right')
                                        gesture_direction = "NEXT slide"
                                        last_gesture_time = current_time
                                        flag = True
                            if c < 60 and flag == True:
                                c = c + 1
                            if c == 60:
                                flag = True
                                c = 0
                # Update the previous position
                previous_wrist_x = wrist_x
                previous_wrist_y = wrist_y
        else:
            # Reset if no hand is detected
            previous_wrist_x = None
            previous_wrist_y = None
        
        # Display the image
        cv2.imshow('Hand Gesture PowerPoint Control', image)
        
        # Check for key press to exit
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Release resources
    hands.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Hand gesture control terminated")
