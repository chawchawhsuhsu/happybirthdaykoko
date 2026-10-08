import logging

import av
import cv2
import streamlit as st

from streamlit_webrtc import (
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

from cv.blow_detector import BlowDetector
from cv.cake import BirthdayCake
from cv.face_tracker import FaceTracker, ensure_model
from cv.hearts import FallingHearts
from cv.kisses import KissAnimationManager


# ============================================================
# LOGGING
# ============================================================

# WebRTC can produce noisy messages when a browser closes or
# restarts a camera connection. Keep actual errors visible.
logging.getLogger("aioice").setLevel(logging.ERROR)
logging.getLogger("aiortc").setLevel(logging.ERROR)
logging.getLogger("streamlit_webrtc").setLevel(logging.ERROR)


# ============================================================
# WEBRTC CONFIGURATION
# ============================================================

# Keep this simple.
#
# We intentionally do NOT use the old public TURN servers
# from the previous version.
#
# The first goal is to establish a clean WebRTC connection
# using STUN.

RTC_CONFIG = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": [
                    "stun:stun.l.google.com:19302",
                ]
            }
        ]
    }
)


# ============================================================
# FACE TRACKER
# ============================================================

@st.cache_resource
def get_face_tracker():
    """
    Create and cache the face tracker.

    Streamlit reruns the script frequently, so caching the
    tracker prevents unnecessary recreation.
    """
    return FaceTracker(max_faces=1)


# ============================================================
# BIRTHDAY VIDEO PROCESSOR
# ============================================================

class BirthdayProcessor(VideoProcessorBase):
    """
    Processes every webcam frame.

    The actual computer-vision features remain in their
    separate modules:

        FaceTracker
        BlowDetector
        BirthdayCake
        KissAnimationManager
        FallingHearts
    """

    def __init__(self):
        # Face tracking
        self.tracker = get_face_tracker()

        # Existing birthday components
        self.blow_detector = BlowDetector()
        self.kisses = KissAnimationManager(max_kisses=12)
        self.hearts = FallingHearts(count=20)
        self.cake = BirthdayCake()

        # Debug mode
        self.debug = False

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        """
        Process one webcam frame and return the modified frame.
        """

        # ----------------------------------------------------
        # Convert WebRTC frame -> OpenCV image
        # ----------------------------------------------------

        img = frame.to_ndarray(format="bgr24")

        # Mirror webcam image
        img = cv2.flip(img, 1)

        # ----------------------------------------------------
        # Face tracking
        # ----------------------------------------------------

        face = self.tracker.process_frame(img)

        # ----------------------------------------------------
        # Blow detection
        # ----------------------------------------------------

        if face and self.cake.lit:
            if self.blow_detector.is_blowing(face):

                # Get cake geometry from your existing module
                geometry = self.cake.geometry(img)

                # Blow out candles
                self.cake.blow_out(geometry[4])

                # Reset detector
                self.blow_detector.blow_counter = 0

        # ----------------------------------------------------
        # Kiss animation
        # ----------------------------------------------------

        img = self.kisses.update_and_draw(
            img,
            face,
        )

        # ----------------------------------------------------
        # Falling hearts
        # ----------------------------------------------------

        img = self.hearts.update_and_draw(img)

        # ----------------------------------------------------
        # Cake
        # ----------------------------------------------------

        img = self.cake.draw(img)

        # ----------------------------------------------------
        # Debug information
        # ----------------------------------------------------

        if self.debug:
            bd = self.blow_detector

            debug_text = (
                f"MAR {bd.last_mar:.2f} | "
                f"width {bd.last_ratio:.2f} | "
                f"blow "
                f"{bd.blow_counter}/{bd.required_frames}"
            )

            cv2.putText(
                img,
                debug_text,
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

        # ----------------------------------------------------
        # OpenCV image -> WebRTC frame
        # ----------------------------------------------------

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24",
        )

    def on_ended(self):
        """
        Called when the WebRTC session ends.

        Your existing CV components don't require explicit
        cleanup here.
        """
        pass


# ============================================================
# BIRTHDAY PAGE
# ============================================================

def show_birthday_scene():

    # --------------------------------------------------------
    # Streamlit page configuration
    # --------------------------------------------------------

    st.set_page_config(
        page_title="Happy Birthday!",
        page_icon="🎂",
        layout="centered",
    )

    # --------------------------------------------------------
    # Page styling
    # --------------------------------------------------------

    st.markdown(
        """
        <style>

        #MainMenu,
        header,
        footer {
            visibility: hidden;
        }

        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #180e30,
                    #32152f,
                    #54283f
                );

            color: #fff0eb;
        }

        .block-container {
            max-width: 900px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Birthday title
    # --------------------------------------------------------

    st.markdown(
        """
        <h1
            style="
                text-align: center;
                color: #ffd1dc;
                margin-bottom: 0.3rem;
            "
        >
            🎂 HAPPY BIRTHDAY! 🎂
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p
            style="
                text-align: center;
                color: #ffe8ee;
                font-size: 1rem;
            "
        >
            Click START, allow the camera,
            then purse your lips like an "O"
            and blow the candles! 💨🕯️
        </p>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Make sure MediaPipe/model is available
    # --------------------------------------------------------

    try:
        import mediapipe

        if not hasattr(mediapipe, "solutions"):

            with st.spinner(
                "Preparing the face-tracking model..."
            ):
                ensure_model()

    except Exception as e:

        st.error(
            "The face-tracking component could not be "
            "initialized."
        )

        st.caption(
            f"{type(e).__name__}: {e}"
        )

        return

    # --------------------------------------------------------
    # WebRTC CAMERA
    # --------------------------------------------------------

    ctx = webrtc_streamer(
        key="birthday",

        mode=WebRtcMode.SENDRECV,

        video_processor_factory=BirthdayProcessor,

        media_stream_constraints={
            "video": True,
            "audio": False,
        },

        rtc_configuration=RTC_CONFIG,

        # Run video processing asynchronously.
        async_processing=True,

        sendback_audio=False,
    )

    # --------------------------------------------------------
    # Controls
    # --------------------------------------------------------

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    # ========================================================
    # SEND KISS
    # ========================================================

    with col1:

        send_kiss = st.button(
            "💋 Send Kiss",
            use_container_width=True,
        )

    # ========================================================
    # RELIGHT CANDLES
    # ========================================================

    with col2:

        relight = st.button(
            "🕯️ Relight Candles",
            use_container_width=True,
        )

    # ========================================================
    # DEBUG
    # ========================================================

    with col3:

        debug = st.checkbox(
            "Debug overlay",
        )

    # --------------------------------------------------------
    # Get active video processor
    # --------------------------------------------------------

    proc = ctx.video_processor

    if proc is not None:

        # Update debug mode
        proc.debug = debug

        # ----------------------------------------------------
        # Kiss button
        # ----------------------------------------------------

        if send_kiss:
            proc.kisses.spawn_kiss()

        # ----------------------------------------------------
        # Relight button
        # ----------------------------------------------------

        if relight:
            proc.cake.relight()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    show_birthday_scene()
