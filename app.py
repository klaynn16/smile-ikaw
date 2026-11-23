
import html
import re
import time

import streamlit as st
import bouquet3d as bouquet

st.set_page_config(
    page_title="A Bouquet For You",
    page_icon="💐",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(
            circle at top,
            #33213f 0%,
            #17121f 58%,
            #100d16 100%
        );
        color: #fff;
    }

    h1, p {
        text-align: center;
    }

    h1 {
        color: #f7c8e7;
        letter-spacing: 1px;
    }

    .bouquet-frame {
        width: 100%;
        overflow-x: auto;
        background: rgba(10,7,16,.48);
        border: 1px solid rgba(247,200,231,.22);
        border-radius: 18px;
        padding: 14px 6px;
        box-shadow: 0 12px 45px rgba(0,0,0,.25);
    }

    .bouquet-frame pre {
        margin: 0;
        text-align: center;
        font-family: Consolas, 'Courier New', monospace;
        font-size: clamp(7px, 1.05vw, 12px);
        line-height: 1.12;
        white-space: pre;
    }

    .subtitle {
        color: #e7cfe5;
        opacity: .9;
    }

    div.stButton > button {
        border-radius: 999px;
        border: 1px solid #e9b7dc;
        background: #754d78;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("💐 A Bouquet For You 💐")

st.markdown(
    '<p class="subtitle">A little bouquet, made just for you.</p>',
    unsafe_allow_html=True
)


# Convert ANSI colors into browser-friendly HTML.
def xterm_color(index: int) -> str:
    basic = [
        "#000000", "#800000", "#008000", "#808000",
        "#000080", "#800080", "#008080", "#c0c0c0",
        "#808080", "#ff0000", "#00ff00", "#ffff00",
        "#0000ff", "#ff00ff", "#00ffff", "#ffffff"
    ]

    if index < 16:
        return basic[index]

    if index < 232:
        n = index - 16
        levels = [0, 95, 135, 175, 215, 255]

        r = levels[n // 36]
        g = levels[(n % 36) // 6]
        b = levels[n % 6]

        return f"#{r:02x}{g:02x}{b:02x}"

    gray = 8 + (index - 232) * 10
    return f"#{gray:02x}{gray:02x}{gray:02x}"


ANSI = re.compile(r"\x1b\[([0-9;]*)m")


def ansi_to_html(frame: str) -> str:
    frame = frame.replace("\x1b[H", "")

    pieces = []
    last = 0
    color = None

    for match in ANSI.finditer(frame):
        segment = html.escape(frame[last:match.start()])

        if color:
            pieces.append(
                f'<span style="color:{color}">{segment}</span>'
            )
        else:
            pieces.append(segment)

        codes = [
            int(x)
            for x in match.group(1).split(";")
            if x
        ]

        if len(codes) >= 3 and codes[0] == 38 and codes[1] == 5:
            color = xterm_color(codes[2])

        elif not codes or codes[0] == 0:
            color = None

        last = match.end()

    tail = html.escape(frame[last:])

    if color:
        pieces.append(
            f'<span style="color:{color}">{tail}</span>'
        )
    else:
        pieces.append(tail)

    return "".join(pieces)


@st.cache_resource
def get_scene():
    return bouquet.build_scene()


# Animation states
if "hearts" not in st.session_state:
    st.session_state.hearts = []

if "playing" not in st.session_state:
    st.session_state.playing = True

if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0.0

if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.perf_counter()


@st.fragment(run_every="100ms")
def animated_bouquet():

    controls = st.columns([1, 1, 1])

    with controls[1]:
        label = (
            "⏸ Pause"
            if st.session_state.playing
            else "▶ Play"
        )

        if st.button(label, use_container_width=True):
            st.session_state.playing = not st.session_state.playing
            st.session_state.last_tick = time.perf_counter()

    now = time.perf_counter()

    dt = min(
        now - st.session_state.last_tick,
        0.2
    )

    if st.session_state.playing:
        st.session_state.elapsed += dt
        bouquet.update_hearts(
            st.session_state.hearts,
            dt
        )

    st.session_state.last_tick = now

    frame = bouquet.render(
        get_scene(),
        st.session_state.elapsed,
        86,
        32,
        st.session_state.hearts
    )

    # FIX: Render the generated HTML directly.
    # Do not use st.markdown for this HTML animation.
    rendered_frame = ansi_to_html(frame)

    st.html(
        f"""
        <div class="bouquet-frame">
            <pre>{rendered_frame}</pre>
        </div>
        """
    )


animated_bouquet()

st.markdown(
    '<p class="subtitle">With love ♥</p>',
    unsafe_allow_html=True
)
