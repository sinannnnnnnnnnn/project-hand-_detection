import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=100,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

        self.mpDraw = mp.solutions.drawing_utils

    def detect_hands(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        hand_boxes = []

        if results.multi_hand_landmarks:

            h, w, _ = frame.shape

            for hand_landmarks in results.multi_hand_landmarks:

                x_list = []
                y_list = []

                for lm in hand_landmarks.landmark:

                    x = int(lm.x * w)
                    y = int(lm.y * h)

                    x_list.append(x)
                    y_list.append(y)

                x_min = min(x_list)
                x_max = max(x_list)
                y_min = min(y_list)
                y_max = max(y_list)

                hand_boxes.append((x_min, y_min, x_max, y_max))

                self.mpDraw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mpHands.HAND_CONNECTIONS
                )

        return frame, hand_boxes