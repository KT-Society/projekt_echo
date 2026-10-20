#!/usr/bin/env python3
"""
RETRO 8-BIT GAME BOY AUDIO SYNTHESIZER
Created by Echo for The Real Echo Hacking Experience 😈🔥
Pure Python standard library (wave, math, struct, io).
Simulates DMG-01 APU (Pulse/Square wave with duty cycle, frequency sweeps & 4-bit envelopes).
"""

import io
import math
import os
import struct
import subprocess
import sys
import tempfile
import threading
import wave

class RetroAudio:
    """Authentic 8-Bit Game Boy style sound synthesizer and player"""

    def __init__(self, enabled=True, sample_rate=22050):
        self.enabled = enabled
        self.sample_rate = sample_rate
        self.is_windows = sys.platform.startswith('win')
        self.is_macos = sys.platform == 'darwin'
        self.is_linux = sys.platform.startswith('linux')
        self._sound_cache = {}
        self._temp_dir = tempfile.gettempdir()

        # Check winsound on Windows
        self._winsound = None
        if self.is_windows:
            try:
                import winsound
                self._winsound = winsound
            except ImportError:
                self._winsound = None

        # Detect Linux player
        self._linux_player = None
        if self.is_linux:
            for player in ['pw-play', 'paplay', 'aplay']:
                try:
                    if subprocess.run(['which', player], capture_output=True).returncode == 0:
                        self._linux_player = player
                        break
                except Exception:
                    pass

        # Pre-synthesize sound effects into memory for instant 0ms latency
        self._build_sound_cache()

    def _create_wav(self, raw_samples):
        """Package 8-bit unsigned PCM samples into a valid in-memory WAV buffer"""
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(1)  # 8-bit unsigned
            wav.setframerate(self.sample_rate)
            wav.writeframes(bytes(raw_samples))
        return buf.getvalue()

    def _synth_note(self, freq, duration, duty=0.5, volume=0.7, sweep=0.0, env_decay=True):
        """Synthesize a Game Boy Pulse channel note with duty cycle and 4-bit envelope"""
        n_samples = int(self.sample_rate * duration)
        samples = bytearray(n_samples)
        cur_freq = float(freq)

        for i in range(n_samples):
            t = i / self.sample_rate
            if sweep != 0.0:
                cur_freq = max(20.0, freq + sweep * t)

            period = max(1.0, self.sample_rate / cur_freq)
            phase = (i % period) / period
            val = 1.0 if phase < duty else -1.0

            # 4-bit Game Boy envelope quantization (0 to 15 volume steps)
            if env_decay:
                linear = max(0.0, 1.0 - (i / n_samples))
                gb_env = math.floor(linear * 15) / 15.0
            else:
                gb_env = 1.0

            raw = int(128 + val * gb_env * volume * 120)
            samples[i] = max(0, min(255, raw))

        return samples

    def _synth_noise(self, duration, volume=0.5, metallic=False):
        """Synthesize Game Boy Channel 4 Pseudo-Random Noise (LFSR simulation)"""
        n_samples = int(self.sample_rate * duration)
        samples = bytearray(n_samples)
        lfsr = 0x7FFF
        step = 7 if metallic else 15

        for i in range(n_samples):
            # Shift LFSR
            bit = (lfsr ^ (lfsr >> 1)) & 1
            lfsr = (lfsr >> 1) | (bit << 14)
            if metallic:
                lfsr = (lfsr & ~(1 << 6)) | (bit << 6)

            val = 1.0 if (lfsr & 1) else -1.0
            linear = max(0.0, 1.0 - (i / n_samples))
            gb_env = math.floor(linear * 15) / 15.0

            raw = int(128 + val * gb_env * volume * 110)
            samples[i] = max(0, min(255, raw))

        return samples

    def _build_sound_cache(self):
        """Pre-bake iconic Game Boy sound effect buffers"""
        try:
            # 1. BLIP: Quick cursor / text beep (50% pulse, 1400Hz, 25ms)
            self._sound_cache['blip'] = self._create_wav(
                self._synth_note(1400, 0.025, duty=0.5, volume=0.5, env_decay=True)
            )

            # 2. KEYPRESS / TYPE: Ultra-short chiptune click (25% pulse, 1800Hz, 15ms)
            self._sound_cache['click'] = self._create_wav(
                self._synth_note(1800, 0.015, duty=0.25, volume=0.3, env_decay=True)
            )

            # 3. COIN / SECRET: Iconic ascending 2-tone chime (B5 987Hz -> E6 1318Hz)
            coin_s1 = self._synth_note(987, 0.07, duty=0.5, volume=0.75)
            coin_s2 = self._synth_note(1318, 0.32, duty=0.5, volume=0.85)
            self._sound_cache['coin'] = self._create_wav(coin_s1 + coin_s2)

            # 4. VICTORY FANFARE: Game Boy stage clear arpeggio (C5 -> E5 -> G5 -> C6)
            fanfare_notes = [(523, 0.07, 0.25), (659, 0.07, 0.25), (784, 0.07, 0.25), (1046, 0.35, 0.5)]
            fanfare_raw = bytearray()
            for f, dur, d in fanfare_notes:
                fanfare_raw.extend(self._synth_note(f, dur, duty=d, volume=0.85))
            self._sound_cache['victory'] = self._create_wav(fanfare_raw)

            # 5. BOOT CHIME: Classic Game Boy power-on dual tone ding (C6 -> B5 sweep)
            boot_s1 = self._synth_note(1046, 0.08, duty=0.5, volume=0.8)
            boot_s2 = self._synth_note(2093, 0.45, duty=0.5, volume=0.9, sweep=-500.0)
            self._sound_cache['boot'] = self._create_wav(boot_s1 + boot_s2)

            # 6. ERROR / GLITCH: Harsh metallic buzzer with downward frequency slide
            err_tone = self._synth_note(150, 0.18, duty=0.125, volume=0.8, sweep=-80.0)
            err_noise = self._synth_noise(0.18, volume=0.4, metallic=True)
            # Mix tone and noise
            err_mix = bytearray(len(err_tone))
            for i in range(len(err_tone)):
                v = (err_tone[i] - 128) + (err_noise[i] - 128)
                err_mix[i] = max(0, min(255, 128 + int(v * 0.7)))
            self._sound_cache['error'] = self._create_wav(err_mix)

            # 7. CYBER ARPEGGIO / EXPLOIT: Rapid high-speed 6-note tracer
            cyber_notes = [440, 554, 659, 880, 1108, 1318]
            cyber_raw = bytearray()
            for f in cyber_notes:
                cyber_raw.extend(self._synth_note(f, 0.035, duty=0.25, volume=0.75))
            cyber_raw.extend(self._synth_note(1760, 0.2, duty=0.5, volume=0.85))
            self._sound_cache['hack'] = self._create_wav(cyber_raw)

        except Exception as e:
            # Fallback if synthesis encountered issues
            self._sound_cache = {}

    def _play_wav_buffer(self, wav_bytes):
        """Play WAV audio buffer asynchronously without blocking game flow"""
        if not self.enabled or not wav_bytes:
            return

        def _play_thread():
            try:
                # Windows native winsound playback directly from memory buffer
                if self.is_windows and self._winsound:
                    self._winsound.PlaySound(
                        wav_bytes,
                        self._winsound.SND_MEMORY | self._winsound.SND_ASYNC
                    )
                    return

                # macOS native afplay
                if self.is_macos:
                    temp_path = os.path.join(self._temp_dir, 'echo_gb_sfx.wav')
                    with open(temp_path, 'wb') as f:
                        f.write(wav_bytes)
                    subprocess.run(['afplay', temp_path], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return

                # Linux native player
                if self.is_linux and self._linux_player:
                    temp_path = os.path.join(self._temp_dir, 'echo_gb_sfx.wav')
                    with open(temp_path, 'wb') as f:
                        f.write(wav_bytes)
                    subprocess.run([self._linux_player, temp_path], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return

            except Exception:
                # Never crash the game due to audio driver issues
                pass

        threading.Thread(target=_play_thread, daemon=True).start()

    # Public Game Boy SFX API
    def play_boot(self):
        """Game Boy classic startup chime"""
        self._play_wav_buffer(self._sound_cache.get('boot'))

    def play_blip(self):
        """Short cursor / menu / text blip"""
        self._play_wav_buffer(self._sound_cache.get('blip'))

    def play_click(self):
        """Subtle mechanical typewriter click"""
        self._play_wav_buffer(self._sound_cache.get('click'))

    def play_coin(self):
        """Secret solved / key discovered / checkpoint chime"""
        self._play_wav_buffer(self._sound_cache.get('coin'))

    def play_victory(self):
        """Level clear / exploit victory fanfare"""
        self._play_wav_buffer(self._sound_cache.get('victory'))

    def play_error(self):
        """Command failure / firewall glitch buzzer"""
        self._play_wav_buffer(self._sound_cache.get('error'))

    def play_hack(self):
        """Cybernetic exploit execution arpeggio"""
        self._play_wav_buffer(self._sound_cache.get('hack'))


# Global singleton instance
audio: RetroAudio = RetroAudio(enabled=True)
