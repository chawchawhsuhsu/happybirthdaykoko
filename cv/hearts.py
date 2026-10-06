import math
import random

from cv.drawing import blend_draw, draw_heart

PALETTE = [(180, 105, 255), (203, 192, 255), (147, 112, 255), (120, 80, 255), (200, 150, 255)]


class FallingHearts:
    def __init__(self, count=20):
        self.count = count
        self.size = None
        self.hearts = []

    def _new(self, w, h, initial=False):
        return {
            "x": random.uniform(0, w),
            "y": random.uniform(-h, 0) if initial else random.uniform(-60, -10),
            "speed": random.uniform(2, 5),
            "size": random.randint(14, 30),
            "phase": random.uniform(0, 6.28),
            "color": random.choice(PALETTE),
        }

    def update_and_draw(self, frame):
        h, w = frame.shape[:2]
        if self.size != (w, h):
            self.size = (w, h)
            self.hearts = [self._new(w, h, True) for _ in range(self.count)]

        for i, hr in enumerate(self.hearts):
            hr["y"] += hr["speed"]
            hr["phase"] += 0.08
            if hr["y"] > h + 40:
                self.hearts[i] = self._new(w, h)
                continue
            x = hr["x"] + math.sin(hr["phase"]) * 12
            blend_draw(
                frame, x, hr["y"], hr["size"], 0.85,
                lambda img, cx, cy, s, c=hr["color"]: draw_heart(img, cx, cy, s, c),
            )
        return frame