# MIT License
#
# Copyright (c) 2024 Kostya Tatoshin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from tempos import Tempos

import streamlit as st
import plotly.express as px


@st.cache_resource
def create_tempos(
    filename,
    start=0.0,
    end=0.0,
    start_bpm=120.0,
    std_bpm=1.0,
    max_bpm=320.0,
    tightness=100.0,
    hop_length=256,
    ac_size=8.0,
    trim=True,
    start_bpm_auto=True,
):
    return Tempos(
        filename,
        start=start,
        end=end,
        start_bpm=start_bpm,
        std_bpm=std_bpm,
        max_bpm=max_bpm,
        tightness=tightness,
        hop_length=hop_length,
        ac_size=ac_size,
        trim=trim,
        start_bpm_auto=start_bpm_auto,
    )


def write_sidebar(tempos):
    if tempos is not None:
        st.sidebar.header("Parameters Of Dynamic Tempo")
        st.sidebar.header("Base")
        st.sidebar.number_input(
            "Start (in seconds)",
            value=0.0,
            help="float >= 0: Start time (in seconds) for trimming the audio.",
            min_value=0.0,
            step=10.0,
            key="start",
        )
        st.sidebar.number_input(
            "End (in seconds)",
            value=tempos.end,
            min_value=0.0,
            help="float >= 0: End time (in seconds) for trimming the audio.",
            step=10.0,
            key="end",
        )
        st.sidebar.toggle(
            "Trim Weak Onsets",
            value=True,
            help="Trim leading/trailing beats with weak onsets.",
            key="trim",
        )
        st.sidebar.header("Advance")
        st.sidebar.toggle(
            "Auto Start BPM",
            help="Auto guess of the initial BPM",
            value=st.session_state.get("start_bpm_auto", True),
            key="start_bpm_auto",
        )
        st.sidebar.number_input(
            "Start BPM",
            value=tempos.static_tempo
            if st.session_state.start_bpm_auto
            else st.session_state.start_bpm,
            help="float: Initial guess of the BPM",
            step=10.0,
            key="start_bpm",
        )
        st.sidebar.number_input(
            "Standard BPM",
            value=1.0,
            help="float > 0: Standard bpm is the standard deviation of the tempo estimator. Sensitivity of bpm.",
            step=1.0,
            key="std_bpm",
        )
        st.sidebar.number_input(
            "Max BPM",
            value=320.0,
            help="float > 0: If provided, only estimate tempo below this threshold",
            step=10.0,
            key="max_bpm",
        )
        st.sidebar.number_input(
            "Tightness",
            value=100.0,
            help="float: Tightness of beat distribution around tempo. Sensitivity to tempo changes.",
            step=100.0,
            key="tightness",
        )

        st.sidebar.number_input(
            "Hop Length",
            value=256,
            help="int > 0: Hop length is the step between consecutive analyzed windows.\n\
            Affects the offset accuracy.\n\
            Smaller numbers give a more accurate result but require more performance and a LOT of memory.",
            min_value=1,
            step=50,
            key="hop_length",
        )
        st.sidebar.number_input(
            "Auto Correlation Window",
            value=10.0,
            help="float > 0: Length (in seconds) of the auto-correlation window.\n\
            Affects the offset accuracy.\n\
            Larger numbers give a smoother result but require more performance and a LOT of memory.",
            step=1.0,
            key="ac_size",
        )
        st.sidebar.header("Song")
        st.sidebar.slider(
            "Song Volume",
            value=20,
            help="Volume of original song regarding the beats.",
            key="song_volume",
        )
        st.sidebar.number_input(
            "Click Frequency (in Hz)",
            value=660.0,
            help="float > 0: Frequency (in Hz) of the default click signal. Sound of clicks.",
            step=10.0,
            key="click_freq",
        )
        st.sidebar.number_input(
            "Click Duration (in seconds)",
            value=0.1,
            help="float > 0: Duration (in seconds) of the default click signal.",
            key="click_duration",
        )


def write_tempos(tempos):
    with st.container(border=True):
        st.file_uploader(
            "Choose an audio file",
            type=["wav", "mp3", "flac", "ogg", "m4a", "wma", "aiff", "aif"],
            key="uploaded",
        )
        if tempos is not None:
            y, sr = tempos.audio(
                st.session_state.song_volume,
                st.session_state.click_freq,
                st.session_state.click_duration,
            )
            st.audio(y, sample_rate=sr)
    if tempos is not None:
        with st.container(border=True):
            x, y = tempos.tempo_dynamic_plot
            data = {
                "x": x,
                "y": y,
            }
            fig = px.line(
                data,
                x="x",
                y="y",
                title="Tempo Dynamic",
                labels={"x": "Time (s)", "y": "BPM"},
            )
            fig.update_traces(line=dict(color="#d85791"))
            st.plotly_chart(fig)
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                data = {"Times": [], "Dynamic BPM": []}
                for start, end, tempo in tempos.segmentize():
                    data["Times"] += [f"{start:.3f} - {end:.3f}".replace(".", ",")]
                    data["Dynamic BPM"] += [round(tempo, 2)]
                st.table(data)
            with col2:
                data = {
                    "Offset": (
                        str(round(tempos.beat_times[0] + tempos.start, 3)).replace(
                            ".", ","
                        ),
                    ),
                    "Static BPM": (tempos.static_tempo,),
                }
                st.table(data)


st.set_page_config(
    page_title="Tanal",
    page_icon=":musical_note:",
    layout="wide",
    initial_sidebar_state="expanded",
)

if st.session_state.get("uploaded", None) is not None:
    tempos = create_tempos(
        st.session_state.uploaded,
        start=st.session_state.get("start", 0.0),
        end=st.session_state.get("end", 0.0),
        start_bpm=st.session_state.get("start_bpm", 120.0),
        std_bpm=st.session_state.get("std_bpm", 1.0),
        max_bpm=st.session_state.get("max_bpm", 320.0),
        tightness=st.session_state.get("tightness", 100.0),
        hop_length=st.session_state.get("hop_length", 256),
        ac_size=st.session_state.get("ac_size", 8.0),
        trim=st.session_state.get("trim", True),
        start_bpm_auto=st.session_state.get("start_bpm_auto", True),
    )
else:
    tempos = None
write_sidebar(tempos)
write_tempos(tempos)
