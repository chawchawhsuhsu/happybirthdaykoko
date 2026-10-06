import random

import cv2
import numpy as np

from cv.drawing import blend_draw


class BirthdayCake:
    def __init__(self):
        self.lit = True
        self.smoke = []

    def relight(self):
        self.lit = True
        self.smoke = []

    def blow_out(self, candle_points):
        if not self.lit:
            return
        self.lit = False
        for (cx, cy) in candle_points:
            self.smoke.append({"x": cx, "y": cy, "life": 1.0})

    def geometry(self, frame):
        h, w = frame.shape[:2]
        cake_w, cake_h = int(w * 0.4), int(h * 0.2)
        x = (w - cake_w) // 2
        y = h - cake_h - 15
        candles = [(x + int(cake_w * f), y - 8) for f in (0.25, 0.5, 0.75)]
        return x, y, cake_w, cake_h, candles

    def draw(self, frame):
        x, y, cw, ch, candles = self.geometry(frame)

        # plate
        cv2.ellipse(frame, (x + cw // 2, y + ch + 6), (int(cw * 0.65), 10), 0, 0, 360, (220, 220, 220), -1, cv2.LINE_AA)
        # sponge + icing
        cv2.rectangle(frame, (x, y), (x + cw, y + ch), (180, 105, 255), -1)
        cv2.rectangle(frame, (x, y), (x + cw, y + ch // 4), (255, 255, 255), -1)
        for i in range(6):  # icing drips
            dx = x + int(cw * (i + 0.5) / 6)
            cv2.circle(frame, (dx, y + ch // 4), cw // 24, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + cw, y + ch), (120, 60, 200), 2)

        # candles
        for (cx, cy) in candles:
            cv2.rectangle(frame, (cx - 5, cy - 32), (cx + 5, cy + 8), (255, 200, 100), -1)
            cv2.rectangle(frame, (cx - 5, cy - 32), (cx + 5, cy + 8), (200, 140, 60), 1)
            cv2.line(frame, (cx, cy - 32), (cx, cy - 38), (40, 40, 40), 2)
            if self.lit:
                f = random.randint(-2, 2)
                cv2.ellipse(frame, (cx + f, cy - 48), (7, 12), 0, 0, 360, (0, 140, 255), -1, cv2.LINE_AA)
                cv2.ellipse(frame, (cx + f, cy - 46), (4, 8), 0, 0, 360, (0, 230, 255), -1, cv2.LINE_AA)

        # smoke after blowing
        alive = []
        for s in self.smoke:
            s["y"] -= 1.5
            s["x"] += random.uniform(-1, 1)
            s["life"] -= 0.02
            if s["life"] > 0:
                alive.append(s)
                blend_draw(
                    frame, s["x"], s["y"] - 40, 10, s["life"] * 0.6,
                    lambda img, cx, cy, sz: cv2.circle(img, (cx, cy), int(sz), (200, 200, 200), -1, cv2.LINE_AA),
                )
        self.smoke = alive
        return frame