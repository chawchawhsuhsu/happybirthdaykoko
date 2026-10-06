import os
import urllib.request

import cv2
import numpy as np
import mediapipe as mp

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_landmarker.task")


def ensure_model():
    """Download the face landmark model once (only needed for new mediapipe versions)."""
    if not os.path.exists(MODEL_PATH):
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    return MODEL_PATH


class FaceTracker:
    def __init__(self, max_faces=1):
        self.legacy = None
        self.landmarker = None

        if hasattr(mp, "solutions"):
            # Old mediapipe (<= ~0.10.21)
            self.legacy = mp.solutions.face_mesh.FaceMesh(
                max_num_faces=max_faces,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )
        else:
            # New mediapipe: Tasks API
            from mediapipe.tasks import python as mp_python
            from mediapipe.tasks.python import vision

            options = vision.FaceLandmarkerOptions(
                base_options=mp_python.BaseOptions(model_asset_path=ensure_model()),
                running_mode=vision.RunningMode.IMAGE,
                num_faces=max_faces,
                min_face_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )
            self.landmarker = vision.FaceLandmarker.create_from_options(options)

        self.LEFT_CHEEK_IDX = 205
        self.RIGHT_CHEEK_IDX = 425
        self.FACE_LEFT_IDX = 234
        self.FACE_RIGHT_IDX = 454
        self.MOUTH_TOP_IDX = 13
        self.MOUTH_BOTTOM_IDX = 14
        self.MOUTH_LEFT_IDX = 61
        self.MOUTH_RIGHT_IDX = 291

    def _get_landmarks(self, frame_bgr):
        rgb = np.ascontiguousarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
        if self.legacy is not None:
            res = self.legacy.process(rgb)
            return res.multi_face_landmarks[0].landmark if res.multi_face_landmarks else None
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        res = self.landmarker.detect(mp_image)
        return res.face_landmarks[0] if res.face_landmarks else None

    def process_frame(self, frame_bgr):
        h, w = frame_bgr.shape[:2]
        lms = self._get_landmarks(frame_bgr)
        if not lms:
            return None

        pts = np.array([(int(lm.x * w), int(lm.y * h)) for lm in lms])

        def P(i):
            return (int(pts[i][0]), int(pts[i][1]))

        min_x, min_y = pts.min(axis=0)
        max_x, max_y = pts.max(axis=0)
        face_width = float(np.linalg.norm(pts[self.FACE_LEFT_IDX] - pts[self.FACE_RIGHT_IDX]))

        return {
            "bbox": (int(min_x), int(min_y), int(max_x - min_x), int(max_y - min_y)),
            "landmarks": pts,
            "face_width": face_width,
            "left_cheek": P(self.LEFT_CHEEK_IDX),
            "right_cheek": P(self.RIGHT_CHEEK_IDX),
            "mouth": {
                "top": P(self.MOUTH_TOP_IDX),
                "bottom": P(self.MOUTH_BOTTOM_IDX),
                "left": P(self.MOUTH_LEFT_IDX),
                "right": P(self.MOUTH_RIGHT_IDX),
            },
        }