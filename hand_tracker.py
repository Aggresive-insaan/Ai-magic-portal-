import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.drawer = mp.solutions.drawing_utils

    def findHands(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        finger = None
        radius = 40
        gesture = "NONE"

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            self.drawer.draw_landmarks(
                frame,
                hand,
                self.mpHands.HAND_CONNECTIONS
            )

            h, w, _ = frame.shape

            # -----------------------
            # Finger Positions
            # -----------------------

            index = hand.landmark[8]
            thumb = hand.landmark[4]

            ix = int(index.x * w)
            iy = int(index.y * h)

            tx = int(thumb.x * w)
            ty = int(thumb.y * h)

            finger = (ix, iy)

            cv2.circle(frame, (ix, iy), 10, (0, 0, 255), -1)
            cv2.circle(frame, (tx, ty), 10, (255, 0, 0), -1)

            # -----------------------
            # Portal Size
            # -----------------------

            distance = int(((ix - tx) ** 2 + (iy - ty) ** 2) ** 0.5)

            radius = max(30, min(distance, 150))

            # -----------------------
            # Gesture Recognition
            # -----------------------

            landmarks = hand.landmark

            tips = [4, 8, 12, 16, 20]

            fingers = []

            # Thumb
            if landmarks[4].x > landmarks[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

            # Index, Middle, Ring, Pinky
            for tip in tips[1:]:

                if landmarks[tip].y < landmarks[tip - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            count = sum(fingers)

            if count == 0:
                gesture = "FIST"

            elif count == 1:
                gesture = "POINT"

            elif count == 2:
                gesture = "TWO"

            elif count >= 4:
                gesture = "PALM"

        return frame, finger, radius, gesture