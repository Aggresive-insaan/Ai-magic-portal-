import pygame
import cv2
import numpy as np
import time

from hand_tracker import HandTracker
from particles import ParticleSystem
from portal import Portal

# ============================
# Initialize Objects
# ============================

tracker = HandTracker()
particles = ParticleSystem()
portal = Portal()

# ============================
# Sound
# ============================

pygame.mixer.init()
pygame.mixer.music.load("assets/portal.wav.mp3")
sound_playing = False

# ============================
# Camera
# ============================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# ============================
# Background
# ============================

background = None

# ============================
# Smooth Animation
# ============================

current_radius = 0
smooth_x = 0
smooth_y = 0

# ============================
# FPS
# ============================

prev_time = 0

# ============================
# Video Recording
# ============================

recording = False
video_writer = None

# ============================
# Screenshot Counter
# ============================

screenshot_count = 1

# ============================
# Main Loop
# ============================

while True:
    

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    if background is None:
        background = frame.copy()

    # Hand Detection
    frame, finger, detected_radius, gesture = tracker.findHands(frame)

    # Gesture Text
    cv2.putText(
        frame,
        f"Gesture : {gesture}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

        # ====================================
    # Show Portal
    # ====================================

    if finger and gesture != "FIST":

        # Smooth Radius
        current_radius += (detected_radius - current_radius) * 0.15
        radius = max(int(current_radius), 20)

        # Play Portal Sound
        if not sound_playing:
            pygame.mixer.music.play(-1)
            sound_playing = True

        # Smooth Position
        target_x, target_y = finger

        smooth_x += (target_x - smooth_x) * 0.25
        smooth_y += (target_y - smooth_y) * 0.25

        x = int(smooth_x)
        y = int(smooth_y)

        # ====================================
        # Portal Background
        # ====================================

        mask = np.zeros(frame.shape[:2], dtype=np.uint8)

        cv2.circle(mask, (x, y), radius, 255, -1)

        portal_bg = cv2.bitwise_and(background, background, mask=mask)

        inverse_mask = cv2.bitwise_not(mask)

        current = cv2.bitwise_and(frame, frame, mask=inverse_mask)

        frame = cv2.add(current, portal_bg)

        # ====================================
        # Fire Particles
        # ====================================

        particles.add_particles(x, y, radius)

        # ====================================
        # Draw Portal
        # ====================================

        portal.draw(frame, x, y, radius, gesture)

        # Portal Center Glow
        cv2.circle(frame, (x, y), 5, (255, 255, 255), -1)

        # Portal Size
        cv2.putText(
            frame,
            f"Portal Size : {radius}px",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

    else:

        if sound_playing:
            pygame.mixer.music.stop()
            sound_playing = False

    # Draw particles every frame
    particles.draw(frame)


        # ============================
    # FPS Counter
    # ============================

    current_time = time.time()

    fps = 1 / (current_time - prev_time) if prev_time else 0

    prev_time = current_time

    cv2.putText(
        frame,
        f"FPS : {int(fps)}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # ============================
    # Recording Indicator
    # ============================

    if recording:

        cv2.putText(
            frame,
            "REC",
            (540, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        video_writer.write(frame)

    # ============================
    # Display Window
    # ============================

    cv2.imshow("AI Magic Portal", frame)

    key = cv2.waitKey(1) & 0xFF

    # Quit
    if key == ord("q"):
        break

    # Capture Background
    elif key == ord("c"):

        background = frame.copy()

        print("Background Captured!")

    # Screenshot
    elif key == ord("s"):

        filename = f"screenshot_{screenshot_count}.png"

        cv2.imwrite(filename, frame)

        print(f"Saved {filename}")

        screenshot_count += 1

    # Video Recording
    elif key == ord("v"):

        if not recording:

            h, w = frame.shape[:2]

            fourcc = cv2.VideoWriter_fourcc(*"XVID")

            video_writer = cv2.VideoWriter(
                "portal_recording.avi",
                fourcc,
                20.0,
                (w, h)
            )

            recording = True

            print("Recording Started...")

        else:

            recording = False
 
            video_writer.release()

            video_writer = None

            print("Recording Saved!")


while True:

    # Display
    cv2.imshow("AI Magic Portal", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    elif key == ord("c"):
        background = frame.copy()
        print("Background Captured!")

    elif key == ord("s"):
        filename = f"screenshot_{screenshot_count}.png"
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")
        screenshot_count += 1

    elif key == ord("v"):

        if not recording:

            h, w = frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*"XVID")

            video_writer = cv2.VideoWriter(
                "portal_recording.avi",
                fourcc,
                20.0,
                (w, h)
            )

            recording = True
            print("Recording Started...")

        else:

            recording = False

            video_writer.release()
            video_writer = None

            print("Recording Saved!")

# ============================
# Cleanup
# ============================

if video_writer is not None:
    video_writer.release()

pygame.mixer.music.stop()
pygame.mixer.quit()

cap.release()
cv2.destroyAllWindows()