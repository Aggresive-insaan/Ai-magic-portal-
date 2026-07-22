import random
import math
import cv2


class ParticleSystem:

    def __init__(self):
        self.particles = []

    def add_particles(self, x, y, radius):

        # Create new particles
        for _ in range(12):

            angle = random.uniform(0, 360)
            speed = random.uniform(2, 8)

            self.particles.append({
                "x": x,
                "y": y,
                "dx": speed,
                "dy": angle,
                "life": random.randint(20, 50),
                "size": random.randint(2, 6)
            })

    def draw(self, frame):

        remove = []

        for p in self.particles:

            # Move particle
            p["x"] += math.cos(math.radians(p["dy"])) * p["dx"]
            p["y"] += math.sin(math.radians(p["dy"])) * p["dx"]

            # Slow down particle slightly
            p["dx"] *= 0.97

            # Reduce life
            p["life"] -= 1

            if p["life"] <= 0:
                remove.append(p)
                continue

            # Change color as particle dies
            if p["life"] > 30:
                color = (0, 165, 255)      # Orange
            elif p["life"] > 15:
                color = (0, 220, 255)      # Yellow
            else:
                color = (255, 255, 255)    # White

            cv2.circle(
                frame,
                (int(p["x"]), int(p["y"])),
                p["size"],
                color,
                -1
            )

        # Remove dead particles
        for p in remove:
            self.particles.remove(p)