import cv2
import mediapipe as mp
import pyautogui
from pynput.mouse import Controller, Button

# Initialize global variables
mouse = Controller()
mouse_button = Button
screen_width, screen_height = pyautogui.size()
mp_hands = mp.solutions.hands
hand_detector = mp_hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils

def capture_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.flip(frame, 1)
    return frame

def process_frame(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    return output.multi_hand_landmarks

def draw_landmarks(frame, hands):
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

def draw_circles(frame, index_x, index_y, thumb_x, thumb_y):
    cv2.circle(img=frame, center=(index_x, index_y), radius=10, color=(0, 255, 255), thickness=-1)
    cv2.circle(img=frame, center=(thumb_x, thumb_y), radius=10, color=(0, 0, 255), thickness=-1)

def move_mouse(index_x, index_y):
    mouse.position = (index_x, index_y)

def perform_click():
    mouse.press(mouse_button.left)
    mouse.release(mouse_button.left)

def calculate_positions(frame, hand):
    frame_height, frame_width, _ = frame.shape
    
    # Access index finger tip (landmark 8) and thumb tip (landmark 4) directly
    index_finger_tip = hand.landmark[0]
    thumb_tip = hand.landmark[4]

    index_x = int(index_finger_tip.x * frame_width)
    index_y = int(index_finger_tip.y * frame_height)
    thumb_x = int(thumb_tip.x * frame_width)
    thumb_y = int(thumb_tip.y * frame_height)

    return index_x, index_y, thumb_x, thumb_y

def main():
    cap = cv2.VideoCapture(0)
    
    while True:
        frame = capture_frame(cap)
        if frame is None:
            break
        
        hands = process_frame(frame)
        draw_landmarks(frame, hands)
        
        if hands:
            hand = hands[0]
            index_x, index_y, thumb_x, thumb_y = calculate_positions(frame, hand)
            
            if index_x is not None and index_y is not None:
                screen_index_x = screen_width / frame.shape[1] * index_x
                screen_index_y = screen_height / frame.shape[0] * index_y
                move_mouse(screen_index_x, screen_index_y)
                
                draw_circles(frame, index_x, index_y, thumb_x, thumb_y)
                
                if thumb_x is not None and thumb_y is not None:
                    screen_thumb_x = screen_width / frame.shape[1] * thumb_x
                    screen_thumb_y = screen_height / frame.shape[0] * thumb_y
                    if abs(screen_index_x - screen_thumb_x) < 50 and abs(screen_index_y - screen_thumb_y) < 50:
                        perform_click()
        
        cv2.imshow("Virtual Mouse", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
