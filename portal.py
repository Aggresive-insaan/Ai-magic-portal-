import cv2
import math


class Portal:

    def __init__(self):

        self.angle = 0

        # Glow Pulse Animation
        self.glow = 0
        self.direction = 1

    def draw(self, frame, x, y, radius, gesture):

        # ==========================
        # Portal Color
        # ==========================

        if gesture == "POINT":
            color = (0, 165, 255)      # Orange

        elif gesture == "TWO":
            color = (255, 120, 0)      # Blue

        elif gesture == "PALM":
            color = (255, 0, 255)      # Purple

        else:
            color = (0, 255, 255)      # Default Yellow

        # ==========================
        # Glow Animation
        # ==========================

        self.glow += self.direction

        if self.glow >= 15:
            self.direction = -1

        elif self.glow <= 0:
            self.direction = 1

        glow_radius = radius + self.glow

        # ==========================
        # Glow Layers
        # ==========================

        for i in range(15, 0, -1):

            cv2.circle(
                frame,
                (x, y),
                glow_radius + i * 2,
                color,
                1
            )

        # ==========================
        # Triple Rings
        # ==========================

        cv2.circle(frame, (x, y), glow_radius, color, 2)
        cv2.circle(frame, (x, y), glow_radius - 8, color, 2)
        cv2.circle(frame, (x, y), glow_radius - 16, color, 1)

        # ==========================
        # Outer Rotating Sparks
        # ==========================

        for i in range(48):

            theta = math.radians(self.angle + i * 7.5)

            px = int(x + glow_radius * math.cos(theta))
            py = int(y + glow_radius * math.sin(theta))

            cv2.circle(frame, (px, py), 3, color, -1)

        # ==========================
        # Inner Rotation
        # ==========================

        for i in range(24):

            theta = math.radians(-self.angle * 1.5 + i * 15)

            px = int(x + (glow_radius - 15) * math.cos(theta))
            py = int(y + (glow_radius - 15) * math.sin(theta))

            cv2.circle(frame, (px, py), 2, (255, 255, 255), -1)

        # ==========================
        # Magic Runes
        # ==========================

        for i in range(12):

            theta = math.radians(self.angle * 2 + i * 30)

            px = int(x + (glow_radius - 30) * math.cos(theta))
            py = int(y + (glow_radius - 30) * math.sin(theta))

            cv2.circle(frame, (px, py), 2, color, -1)

        # ==========================
        # Energy Core
        # ==========================

        cv2.circle(frame, (x, y), glow_radius // 3, color, 2)
        cv2.circle(frame, (x, y), glow_radius // 5, (255, 255, 255), -1)

        # ==========================
        # Rotation Animation
        # ==========================

        self.angle = (self.angle + 4) % 360