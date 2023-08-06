import cv2
import mediapipe as mp
import math
from pynput.mouse import Button, Controller
from pynput.keyboard import Controller as kb_controller
from pynput.keyboard import Key
import time

def run_gestures():

  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles
  mp_hands = mp.solutions.hands
  # For webcam input:
  cap = cv2.VideoCapture(0)
  with mp_hands.Hands(
      model_complexity=1,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as hands:
    previous_landmark = False
    previous_landmarks = False
    while cap.isOpened():
      success, image = cap.read()
      
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)

      # Draw the hand annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      image_height, image_width, _ = image.shape
      if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
          if not previous_landmark:
            gesture_handle(delta_landmark(hand_landmarks.landmark[7], hand_landmarks.landmark[7]), results.multi_handedness[i].classification[0])
          else:
            gesture_handle(delta_landmark(previous_landmark, hand_landmarks.landmark[7]), results.multi_handedness[i].classification[0])
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
          previous_landmark = hand_landmarks.landmark[8]
          previous_landmarks = hand_landmarks
      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
      if cv2.waitKey(5) & 0xFF == 27:
        break
  cap.release()

SCROLL_THRESH = 0.001 # Recommended between 0.005 and 0.001
SCALE_FACTOR = 40
SIGMOID_STRETCH = 10
OFFSET = 0

SCROLL_CONFIDENCE_THRESH = 0.9

SWIPE_THRESH = 0.001
SWIPE_UPPER_BOUND = 100

def delta_landmark(previous_landmark, current_landmark):
    return scroll_sens(current_landmark.x - previous_landmark.x), scroll_sens(current_landmark.y - previous_landmark.y), scroll_sens(current_landmark.z - previous_landmark.z)

def is_scroll(hand_data):
    return (2 * (hand_data.index) - 1) * hand_data.score < - SCROLL_CONFIDENCE_THRESH

def is_scroll_sideways(x, y):
    return abs(x) > abs(y)

def is_swipe(hand_data, x):
    return (2 * (hand_data.index) - 1) * hand_data.score > SCROLL_CONFIDENCE_THRESH and sigmoid(x) > SWIPE_THRESH

def swipe_sideways(x):
    if x > 0:
        input.swipe_left()
    else:
        input.swipe_right()

def gesture_handle(vels, hand_data):
    if is_scroll(hand_data):
        if is_scroll_sideways(vels[0], vels[1]):
            input.scroll_x(vels[0])
        else:
            input.scroll_y(vels[1])

    elif is_swipe(hand_data, vels[0]):
        swipe_sideways(vels[0])
                

def scroll_sens(x):
    return 0 if sigmoid(x) < SCROLL_THRESH else math.copysign(SCALE_FACTOR * sigmoid(x), x)

def sigmoid(x, factor=1): 
    x_new = 2 * abs(x)-1
    expo = -(SIGMOID_STRETCH * factor * (x_new + OFFSET))
    denom = math.e ** expo + 1
    return 1 / (denom + 1)

keyboard = kb_controller()

mouse = Controller()

def scroll_x(scroll_amount):
    mouse.scroll(scroll_amount, 0)

def scroll_y(scroll_amount):
    mouse.scroll(0, scroll_amount)

def swipe_left():
    keyboard.press(Key.left)
    time.sleep(0.05)
    keyboard.release(Key.left)

def swipe_right():
    keyboard.press(Key.right)
    time.sleep(0.05)
    keyboard.release(Key.right)
