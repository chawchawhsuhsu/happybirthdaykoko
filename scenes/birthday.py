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

# aioice/aiortc can produce noisy cleanup messages when a
# WebRTC connection is restarted or the browser disconnects.
logging.getLogger("aioice").setLevel(logging.CRITICAL)
logging.getLogger("aiortc").setLevel(logging.CRITICAL)


# ============================================================
# WEBRTC CONFIGURATION
# ============================================================

# Keep the configuration simple first.
#
# The old configuration used public TURN servers:
#     openrelay.metered.ca
#
# Those public credentials are not reliable enough for a
# deployed Streamlit application and can cause ICE connection
# problems.
#
# STUN is sufficient for many users. If a particular network
# requires TURN, a proper TURN server can be added later.

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
    Create one FaceTracker resource and reuse it across
    Streamlit reruns.
    """
    return FaceTracker(max_faces=1)


# ============================================================
# VIDEO PROCESSOR
# ============================================================

class BirthdayProcessor(VideoProcessorBase):
    """
    Processes webcam frames for the birthday scene.

    Existing CV modules are intentionally kept separate:
        - FaceTracker
        - BlowDetector
        - BirthdayCake
        - KissAnimationManager
        - FallingHearts
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
        Process one webcam frame.
        """

        # ----------------------------------------------------
        # Convert frame to OpenCV image
        # ----------------------------------------------------

        img = frame.to_ndarray(format="bgr24")

        # Mirror webcam like a normal selfie camera
        img = cv2.flip(img, 1)

        # ----------------------------------------------------
        # Face tracking
        # ----------------------------------------------------

        face = self.tracker.process_frame(img)

        # ----------------------------------------------------
        # Blow out candles
        # ----------------------------------------------------

        if (
            face
            and self.cake.lit
            and self.blow_detector.is_blowing(face)
        ):
            geometry = self.cake.geometry(img)

            # Your existing BirthdayCake.geometry()
            # returns the candle information used by the
            # original implementation.
            self.cake.blow_out(geometry[4])

            # Reset detector counter after successful blow
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
        # Birthday cake
        # ----------------------------------------------------

        img = self.cake.draw(img)

        # ----------------------------------------------------
        # Debug overlay
        # ----------------------------------------------------

        if self.debug:
            bd = self.blow_detector

            text = (
                f"MAR {bd.last_mar:.2f} | "
                f"width {bd.last_ratio:.2f} | "
                f"blow {bd.blow_counter}/{bd.required_frames}"
            )

            cv2.putText(
                img,
                text,
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

        # ----------------------------------------------------
        # Convert OpenCV image back to WebRTC frame
        # ----------------------------------------------------

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24",
        )

    def on_ended(self):
        """
        Called when the WebRTC session ends.

        The individual CV modules do not need special cleanup,
        so there is nothing to do here.
        """
        pass


# ============================================================
# PAGE
# ============================================================

def show_birthday_scene():

    # --------------------------------------------------------
    # Streamlit configuration
    # --------------------------------------------------------

    st.set_page_config(
        page_title="Happy Birthday!",
        page_icon="🎂",
        layout="centered",
    )

    # --------------------------------------------------------
    # Styling
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
    # Title
    # --------------------------------------------------------

    st.markdown(
        """
        <h1 style="
            text-align: center;
            color: #ffd1dc;
            margin-bottom: 0.2rem;
        ">
            🎂 HAPPY BIRTHDAY! 🎂
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="
            text-align: center;
            color: #ffe8ee;
            font-size: 1rem;
        ">
            Click START, allow the camera,
            then purse your lips like an "O"
            and blow the candles! 💨🕯️
        </p>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # MediaPipe model
    # --------------------------------------------------------

    try:
        import mediapipe

        if not hasattr(mediapipe, "solutions"):
            with st.spinner(
                "Preparing the face tracking model..."
            ):
                ensure_model()

    except Exception as e:
        st.error(
            "The face-tracking component could not be initialized."
        )

        st.caption(
            f"Details: {type(e).__name__}: {e}"
        )

        return

    # --------------------------------------------------------
    # WebRTC camera
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

        # Keep processing asynchronous so the WebRTC
        # communication thread is not unnecessarily blocked.
        async_processing=True,

        sendback_audio=False,
    )

    # --------------------------------------------------------
    # Controls
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------------------
    # Kiss
    # --------------------------------------------------------

    with col1:
        send_kiss = st.button(
            "💋 Send Kiss",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # Relight
    # --------------------------------------------------------

    with col2:
        relight = st.button(
            "🕯️ Relight Candles",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # Debug
    # --------------------------------------------------------

    with col3:
        debug = st.checkbox(
            "Debug overlay",
        )

    # --------------------------------------------------------
    # Access processor
    # --------------------------------------------------------

    proc = ctx.video_processor

    if proc is not None:

        # Update debug mode
        proc.debug = debug

        # ----------------------------------------------------
        # Send kiss
        # ----------------------------------------------------

        if send_kiss:
            proc.kisses.spawn_kiss()

        # ----------------------------------------------------
        # Relight candles
        # ----------------------------------------------------

        if relight:
            proc.cake.relight()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    show_birthday_scene()
