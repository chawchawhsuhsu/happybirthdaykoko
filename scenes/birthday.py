import av
import cv2
import streamlit as st
from streamlit_webrtc import VideoProcessorBase, WebRtcMode, webrtc_streamer

from cv.blow_detector import BlowDetector
from cv.cake import BirthdayCake
from cv.face_tracker import FaceTracker, ensure_model
from cv.hearts import FallingHearts
from cv.kisses import KissAnimationManager


class BirthdayProcessor(VideoProcessorBase):
    """Runs on a background thread for every live webcam frame."""

    def __init__(self):
        self.tracker = FaceTracker(max_faces=1)
        self.blow_detector = BlowDetector()
        self.kisses = KissAnimationManager(max_kisses=12)
        self.hearts = FallingHearts(count=20)
        self.cake = BirthdayCake()
        self.debug = False

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)  # mirror

        face = self.tracker.process_frame(img)

        # blow out candles
        if face and self.cake.lit and self.blow_detector.is_blowing(face):
            self.cake.blow_out(self.cake.geometry(img)[4])
            self.blow_detector.blow_counter = 0

        img = self.kisses.update_and_draw(img, face)
        img = self.hearts.update_and_draw(img)
        img = self.cake.draw(img)

        if self.debug:
            bd = self.blow_detector
            txt = f"MAR {bd.last_mar:.2f} | width {bd.last_ratio:.2f} | blow {bd.blow_counter}/{bd.required_frames}"
            cv2.putText(img, txt, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


def show_birthday_scene():
    st.markdown(
        """
        <style>
        #MainMenu, header, footer { visibility: hidden; }
        .stApp { background: linear-gradient(135deg, #180e30, #32152f, #54283f); color: #fff0eb; }
        .block-container { max-width: 900px; padding-top: 1rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 style='text-align: center; color: #ffd1dc;'>🎂 HAPPY BIRTHDAY! 🎂</h1>",
        unsafe_allow_html=True,
    )
    st.caption("Click START, allow the camera, then purse your lips like an 'O' and blow the candles!")

    if hasattr(__import__('mediapipe'), 'solutions') is False:
        with st.spinner('Downloading face model (first run only)...'):
            ensure_model()

    ctx = webrtc_streamer(
        key="birthday",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=BirthdayProcessor,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        async_processing=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        send = st.button("💋 Send Kiss")
    with col2:
        relight = st.button("🕯️ Relight Candles")
    with col3:
        debug = st.checkbox("Debug overlay")

    proc = ctx.video_processor
    if proc:
        proc.debug = debug
        if send:
            proc.kisses.spawn_kiss()
        if relight:
            proc.cake.relight()


if __name__ == "__main__":
    show_birthday_scene()