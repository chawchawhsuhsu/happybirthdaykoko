import time
import cv2
import numpy as np
from cv.blow_detector import BlowDetector
from cv.face_tracker import FaceTracker
from cv.kisses import KissAnimationManager


class BirthdayCVExperience:
    def __init__(self):
        self.tracker = FaceTracker()
        self.kiss_mgr = KissAnimationManager()
        self.blow_detector = BlowDetector()

        self.state = "DETECT"
        self.state_start_time = time.time()
        self.candle_lit = True

    def process(self, frame):
        h, w, _ = frame.shape
        face_data = self.tracker.process_frame(frame)
        now = time.time()
        elapsed = now - self.state_start_time

        if self.state == "DETECT":
            if face_data:
                x, y, bw, bh = face_data["bbox"]
                cv2.rectangle(frame, (x, y), (x + bw, y + bh), (200, 180, 255), 2)
                cv2.putText(
                    frame,
                    "Magical Presence Detected",
                    (x, max(20, y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (230, 210, 255),
                    2,
                )
                if elapsed > 3.0:
                    self.state = "KISSES"
                    self.state_start_time = now
            else:
                cv2.putText(
                    frame,
                    "Looking for the Birthday Prince...",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (200, 200, 250),
                    2,
                )

        elif self.state == "KISSES":
            frame = self.kiss_mgr.update_and_draw(frame, face_data)
            cv2.putText(
                frame,
                "Kiss Attack! 💋",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (180, 100, 255),
                2,
            )
            if elapsed > 5.0:
                self.state = "CAKE"
                self.state_start_time = now

        elif self.state == "CAKE":
            cv2.putText(
                frame,
                "🎂 Here comes the cake! 🎂",
                (w // 2 - 180, h - 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )
            if elapsed > 2.5:
                self.state = "WISH"
                self.state_start_time = now

        elif self.state == "WISH":
            if self.candle_lit:
                cv2.putText(
                    frame,
                    "🕯️ BLOW OUT THE CANDLE! 🕯️",
                    (w // 2 - 190, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 215, 255),
                    2,
                )
                if face_data and self.blow_detector.is_blowing(face_data):
                    self.candle_lit = False
                    self.state = "FIREWORKS"
                    self.state_start_time = now
            else:
                self.state = "FIREWORKS"
                self.state_start_time = now

        elif self.state == "FIREWORKS":
            for _ in range(5):
                fx = np.random.randint(0, w)
                fy = np.random.randint(0, h)
                cv2.circle(
                    frame,
                    (fx, fy),
                    np.random.randint(5, 25),
                    (
                        np.random.randint(150, 255),
                        np.random.randint(150, 255),
                        np.random.randint(200, 255),
                    ),
                    -1,
                )

            cv2.putText(
                frame,
                "🎆 HAPPY BIRTHDAY, TOTO! 🤎 🎆",
                (w // 2 - 250, h // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                3,
            )

        return frame, self.state