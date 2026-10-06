import cv2
import numpy as np


def blend_draw(frame, x, y, size, alpha, draw_fn):
    """Draw a shape with transparency, only touching a small region of the frame."""
    h, w = frame.shape[:2]
    pad = int(size * 2.5) + 2
    x, y = int(x), int(y)
    x0, y0 = max(x - pad, 0), max(y - pad, 0)
    x1, y1 = min(x + pad, w), min(y + pad, h)
    if x1 <= x0 or y1 <= y0 or alpha <= 0:
        return
    roi = frame[y0:y1, x0:x1]
    over = roi.copy()
    draw_fn(over, x - x0, y - y0, size)
    cv2.addWeighted(over, min(alpha, 1.0), roi, 1 - min(alpha, 1.0), 0, dst=roi)


def draw_heart(img, cx, cy, size, color=(180, 105, 255)):
    r = max(int(size * 0.5), 2)
    cv2.circle(img, (cx - r, cy - r), r, color, -1, cv2.LINE_AA)
    cv2.circle(img, (cx + r, cy - r), r, color, -1, cv2.LINE_AA)
    pts = np.array(
        [[cx - 2 * r + 1, cy - int(r * 0.6)],
         [cx + 2 * r - 1, cy - int(r * 0.6)],
         [cx, cy + 2 * r]],
        np.int32,
    )
    cv2.fillConvexPoly(img, pts, color, cv2.LINE_AA)
    cv2.circle(img, (cx - r, cy - r - r // 3), max(r // 4, 1), (255, 255, 255), -1, cv2.LINE_AA)


def draw_lips(img, cx, cy, size):
    """A simple lipstick-kiss mark."""
    r = max(int(size), 4)
    col = (50, 30, 220)  # BGR red
    cv2.circle(img, (cx - r // 2, cy - r // 3), int(r * 0.6), col, -1, cv2.LINE_AA)
    cv2.circle(img, (cx + r // 2, cy - r // 3), int(r * 0.6), col, -1, cv2.LINE_AA)
    cv2.ellipse(img, (cx, cy + r // 3), (int(r * 1.1), int(r * 0.7)), 0, 0, 360, col, -1, cv2.LINE_AA)
    cv2.line(img, (cx - int(r * 0.9), cy), (cx + int(r * 0.9), cy), (20, 10, 120),
             max(r // 6, 1), cv2.LINE_AA)