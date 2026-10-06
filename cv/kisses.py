import random
import time

from cv.drawing import blend_draw, draw_lips


class KissAnimationManager:
    """Kisses appear one by one on the player's cheeks, follow the face, then fade."""

    def __init__(self, max_kisses=12, spawn_interval=0.6, lifetime=4.0):
        self.kisses = []
        self.max_kisses = max_kisses
        self.spawn_interval = spawn_interval
        self.lifetime = lifetime
        self.last_spawn = 0.0

    def spawn_kiss(self):
        if len(self.kisses) >= self.max_kisses:
            self.kisses.pop(0)
        self.kisses.append({
            "side": random.choice(["left_cheek", "right_cheek"]),
            "dx": random.randint(-25, 25),
            "dy": random.randint(-25, 25),
            "scale": random.uniform(0.8, 1.3),
            "born": time.time(),
        })

    def update_and_draw(self, frame, face_data=None):
        now = time.time()
        if face_data and now - self.last_spawn >= self.spawn_interval:
            self.spawn_kiss()
            self.last_spawn = now

        alive = []
        for k in self.kisses:
            age = now - k["born"]
            if age >= self.lifetime:
                continue
            alive.append(k)
            if not face_data:
                continue
            fs = max(face_data["face_width"] / 250.0, 0.4)
            bx, by = face_data[k["side"]]
            x = bx + k["dx"] * fs
            y = by + k["dy"] * fs - age * 10 * fs
            alpha = min(1.0, (1 - age / self.lifetime) * 1.5)
            blend_draw(frame, x, y, 16 * k["scale"] * fs, alpha, draw_lips)
        self.kisses = alive
        return frame