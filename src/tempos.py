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

import librosa
import numpy as np


class Tempos:
    def __init__(
        self,
        file,
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
        self.start_bpm = start_bpm
        self.std_bpm = std_bpm
        self.max_bpm = max_bpm
        self.tightness = tightness
        self.hop_length = hop_length
        self.ac_size = ac_size
        self.trim = trim
        self.y, self.sr = librosa.load(file)
        self.start = start
        if end == 0 or end is None:
            self.end = librosa.get_duration(y=self.y, sr=self.sr)
        else:
            self.end = end
        self.y = self.y[
            librosa.time_to_samples(self.start, sr=self.sr) : librosa.time_to_samples(
                self.end, sr=self.sr
            )
        ]
        if start_bpm_auto:
            self.static_tempo, self.beat_times = self.extract_static_tempo()
            self.start_bpm = round(float(self.static_tempo), 2)
        self.static_tempo, self.beat_times = self.extract_static_tempo()
        self.static_tempo = round(float(self.static_tempo), 2)
        self.tempo_dynamic = self.extract_tempo_dynamic()
        self.tempo_times = self.extract_tempo_times()
        _, self.beats_time_dynamic = self.extract_beats_time_dynamic()
        self.tempo_dynamic_plot = (
            [time + self.start for time in self.tempo_times],
            self.tempo_dynamic,
        )
        self.segments = self.segmentize()

    def segmentize(self):
        segments = []
        start = self.tempo_times[0]
        curr_tempo = self.tempo_dynamic[0]
        for time, tempo in zip(self.tempo_times[1:], self.tempo_dynamic[1:]):
            if round(curr_tempo, 2) != round(tempo, 2):
                segments += [[start + self.start, time + self.start, curr_tempo]]
                start = time
                curr_tempo = tempo
        segments += [
            [start + self.start, self.tempo_times[-1] + self.start, curr_tempo]
        ]
        return segments

    def audio(self, volume=20, click_freq=660.0, click_duration=0.1):
        click_dynamic = librosa.clicks(
            times=self.beats_time_dynamic,
            sr=self.sr,
            hop_length=self.hop_length,
            click_freq=click_freq,
            click_duration=click_duration,
            length=len(self.y),
        )
        volume_reduce = volume / 100
        y_reduced = self.y * volume_reduce
        combined_audio = y_reduced + click_dynamic
        max_amplitude = np.mean(combined_audio)
        if max_amplitude > 1.0:
            combined_audio = combined_audio / max_amplitude
        return combined_audio, self.sr

    def extract_tempo_dynamic(self):
        return librosa.feature.tempo(
            y=self.y,
            sr=self.sr,
            hop_length=self.hop_length,
            aggregate=None,
            std_bpm=self.std_bpm,
            start_bpm=self.start_bpm,
            ac_size=self.ac_size,
            max_tempo=self.max_bpm,
        )

    def extract_tempo_times(self):
        return librosa.times_like(
            self.tempo_dynamic, sr=self.sr, hop_length=self.hop_length
        )

    def extract_static_tempo(self):
        return librosa.beat.beat_track(
            y=self.y,
            sr=self.sr,
            hop_length=self.hop_length,
            start_bpm=self.start_bpm,
            tightness=self.tightness,
            units="time",
            trim=self.trim,
        )

    def extract_beats_time_dynamic(self):
        return librosa.beat.beat_track(
            y=self.y,
            sr=self.sr,
            hop_length=self.hop_length,
            start_bpm=self.start_bpm,
            units="time",
            bpm=self.tempo_dynamic,
            trim=self.trim,
            tightness=self.tightness,
        )
