import numpy as np


class BlowDetector:
    """
    Detects a 'blowing' mouth: the lips are pursed into an 'O'.
    That means the mouth is open a bit (MAR high enough) AND narrow
    compared to the face width. A plain wide-open mouth or a smile won't count.
    Tune the thresholds with the debug overlay if needed.
    """

    def __init__(self, mar_threshold=0.28, width_ratio_max=0.33, required_frames=4):
        self.mar_threshold = mar_threshold
        self.width_ratio_max = width_ratio_max
        self.required_frames = required_frames
        self.blow_counter = 0
        self.last_mar = 0.0
        self.last_ratio = 0.0

    def compute_mar(self, m):
        v = np.linalg.norm(np.array(m["top"]) - np.array(m["bottom"]))
        hz = np.linalg.norm(np.array(m["left"]) - np.array(m["right"]))
        return 0.0 if hz == 0 else float(v / hz)

    def is_blowing(self, face_data):
        if not face_data or "mouth" not in face_data:
            self.blow_counter = max(0, self.blow_counter - 1)
            return False

        m = face_data["mouth"]
        self.last_mar = self.compute_mar(m)
        mouth_w = np.linalg.norm(np.array(m["left"]) - np.array(m["right"]))
        self.last_ratio = float(mouth_w / max(face_data.get("face_width", 1.0), 1.0))

        if self.last_mar > self.mar_threshold and self.last_ratio < self.width_ratio_max:
            self.blow_counter += 1
        else:
            self.blow_counter = max(0, self.blow_counter - 1)

        return self.blow_counter >= self.required_frames