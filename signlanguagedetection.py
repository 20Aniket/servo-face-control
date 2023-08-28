import cv2
import mediapipe as mp
import serial

def main():
    # Establish serial connection with Arduino
    arduino = serial.Serial('/dev/cu.usb', 9600)
    
    mp_holistic = mp.solutions.holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_drawing = mp.solutions.drawing_utils

    capture = cv2.VideoCapture(0)
    
    if not capture.isOpened():
        print("Error: Unable to access the webcam.")
        return
    
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        
        image, detected = process_frame(frame, mp_holistic, mp_drawing)
        
        # Send signal to Arduino if face or hand is detected
        if detected:
            arduino.write(b'1')
        else:
            arduino.write(b'0')

        cv2.imshow("Facial and Hand Landmarks", image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

def process_frame(frame, holistic_model, drawing_utils):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = holistic_model.process(image)
    image.flags.writeable = True
    
    detected = False

    if results.left_hand_landmarks or results.right_hand_landmarks or results.face_landmarks:
        detected = True

    drawing_utils.draw_landmarks(
        image,
        results.left_hand_landmarks,
        mp.solutions.holistic.HAND_CONNECTIONS  # Use mp.solutions.holistic.HAND_CONNECTIONS
    )
    drawing_utils.draw_landmarks(
        image,
        results.right_hand_landmarks,
        mp.solutions.holistic.HAND_CONNECTIONS  # Use mp.solutions.holistic.HAND_CONNECTIONS
    )
    drawing_utils.draw_landmarks(
        image,
        results.face_landmarks,
        mp.solutions.holistic.FACEMESH_CONTOURS  # Use mp.solutions.holistic.FACEMESH_CONTOURS
    )

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    return image, detected

if __name__ == "__main__":
    main()

