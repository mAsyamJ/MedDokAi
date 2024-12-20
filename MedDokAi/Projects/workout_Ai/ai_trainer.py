import cv2
import mediapipe as mp
import numpy as np
import pyttsx3  # For voice feedback
import time

# Initialize MediaPipe pose model and drawing utilities
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize text-to-speech for voice feedback
engine = pyttsx3.init()
def speak_feedback(text):
    engine.say(text)
    engine.runAndWait()

# Variables to count reps
rep_count = 0
stage = None  # Used to track whether the movement is up or down

# Start time for session duration
start_time = time.time()

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    Points `a`, `b`, and `c` are tuples of (x, y) coordinates.
    """
    a = np.array(a)  # First point (shoulder)
    b = np.array(b)  # Second point (elbow)
    c = np.array(c)  # Third point (wrist)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame for a selfie-view display
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Convert the frame to RGB as MediaPipe works with RGB images
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Extract landmarks
        landmarks = results.pose_landmarks.landmark

        # Get coordinates of shoulder, elbow, and wrist for both arms
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * w,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * h]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * w,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * h]
        
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]

        # Calculate the angle at both elbows
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

        # Draw the progress bar based on the right elbow angle
        progress_bar_height = int(np.interp(right_angle, [30, 160], [h - 100, 100]))
        cv2.rectangle(frame, (w - 50, h - 100), (w - 30, 100), (0, 255, 0), 2)
        cv2.rectangle(frame, (w - 50, progress_bar_height), (w - 30, h - 100), (0, 255, 0), -1)

        # Display overlay background
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 170), (0, 0, 0), -1)
        alpha = 0.5
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Display the angles and rep count on the overlay
        cv2.putText(frame, f'Right Angle: {int(right_angle)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, (255, 255, 255), 2)
        cv2.putText(frame, f'Left Angle: {int(left_angle)}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, (255, 255, 255), 2)
        cv2.putText(frame, f'Reps: {rep_count}', (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 
                    1.2, (0, 255, 0), 3)

        # Calculate elapsed time and display session duration
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        cv2.putText(frame, f'Time: {minutes:02d}:{seconds:02d}', (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, (255, 255, 255), 2)

        # Curl counter logic (check for either arm)
        if right_angle > 160 and left_angle > 160:  # Both arms are fully extended
            stage = "down"
        if (right_angle < 30 or left_angle < 30) and stage == "down":  # One arm is fully flexed (curl up)
            stage = "up"
            rep_count += 1
            speak_feedback("Good job! Rep completed.")

            # Milestone feedback every 5 reps
            if rep_count % 5 == 0:
                speak_feedback(f"Awesome! You've completed {rep_count} reps.")

        # Draw pose landmarks on the frame
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the frame
    cv2.imshow("Dumbbell Curl Rep Counter", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture
cap.release()
cv2.destroyAllWindows()
