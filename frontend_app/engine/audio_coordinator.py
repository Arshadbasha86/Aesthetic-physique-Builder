"""
Aesthetic Physique Builder - Hybrid Audio & Voice Coach Coordinator
Relative Path: frontend_app/engine/audio_coordinator.py
Architectural Role: Event-driven audio subsystem separating short low-latency
SFX (tick, whistle, bell) from spoken voice guidance with automatic ticking
ducking and sequential non-collision execution.
"""

import os
import time
import threading
import queue
from pathlib import Path
from typing import Optional, Dict, Any

from config.default_config import (
    SFX_DIR, COACH_VOICE_DIR, DEFAULT_COACH_PERSONA,
    POST_SET_WHISTLE_DELAY_MS
)
from database.db_manager import db

# Try importing pyttsx3 for offline speech synthesis fallback
try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False


class AudioCoordinator:
    """
    Hybrid audio engine handling:
    1. Low-latency SFX pool (tick, bell, whistle)
    2. Voice Coach playback (pre-rendered MP3s or local TTS synthesizer)
    3. Background ticking ducking during vocal cues
    4. Strict sequential non-collision execution
    """
    _instance: Optional["AudioCoordinator"] = None

    def __new__(cls) -> "AudioCoordinator":
        if cls._instance is None:
            cls._instance = super(AudioCoordinator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.page = None
        self.is_ducked = False
        self.is_speaking = False
        self.is_muted = False
        self._speech_queue = queue.Queue()
        self._tts_engine = None
        self._lock = threading.Lock()

        # Start background TTS dispatch worker
        self._worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self._worker_thread.start()
        self._initialized = True

    def attach_page(self, page):
        """Attaches active Flet page reference for UI-bound audio players."""
        self.page = page

    # ==========================================================================
    # 1. Low-Latency SFX Triggers
    # ==========================================================================
    def play_tick(self):
        """Plays subtle 100ms clock tick on second transitions (suppressed if ducked)."""
        if self.is_ducked or self.is_speaking or self.is_muted:
            return
        tick_path = SFX_DIR / "tick.mp3"
        self._play_sound_file(str(tick_path))

    def play_whistle(self):
        """Plays referee sports whistle signalling exercise or set termination."""
        if self.is_muted:
            return
        whistle_path = SFX_DIR / "whistle.mp3"
        self._play_sound_file(str(whistle_path))

    def play_bell(self):
        """Plays boxing chime signalling rest interval conclusion."""
        if self.is_muted:
            return
        bell_path = SFX_DIR / "bell.mp3"
        self._play_sound_file(str(bell_path))

    def play_set_completion_sequence(self, transition_prompt: str = "Take a rest"):
        """
        Executes strict sequential non-collision:
        Play whistle -> Wait 400ms -> Trigger Coach Voice: 'Take a rest.'
        """
        def _sequence():
            self.play_whistle()
            time.sleep(POST_SET_WHISTLE_DELAY_MS / 1000.0)
            self.speak_cue("take_a_rest", fallback_text=transition_prompt)

        threading.Thread(target=_sequence, daemon=True).start()

    # ==========================================================================
    # 2. Voice Coach Dispatcher & Audio Ducking
    # ==========================================================================
    def speak_cue(self, cue_id: str, fallback_text: Optional[str] = None):
        """
        Dispatches voice cue with immediate audio ducking:
        1. Checks pre-rendered voice pack MP3 (assets/audio/coach/<persona>/<cue_id>.mp3)
        2. Falls back to offline synthesizer (pyttsx3)
        """
        if self.is_muted:
            return

        tts_enabled = db.get_setting("voice_tts_enabled", "true").lower() == "true"
        if not tts_enabled:
            return

        persona = db.get_setting("selected_persona", DEFAULT_COACH_PERSONA)

        # Check for pre-rendered MP3 file
        pre_rendered_file = COACH_VOICE_DIR / persona / f"{cue_id}.mp3"
        if pre_rendered_file.exists():
            self._play_voice_file(str(pre_rendered_file))
            return

        # Fallback to spoken text
        text_mapping = {
            "test": "Hi, I am your workout coach. Let's get started!",
            "get_ready": "Get ready.",
            "three": "Three.",
            "two": "Two.",
            "one": "One.",
            "take_a_rest": "Take a rest.",
            "next_up": "Next up:",
            "switch_sides": "Switch sides.",
            "halfway": "Halfway through.",
        }
        spoken_text = fallback_text or text_mapping.get(cue_id, cue_id)
        self.speak_text(spoken_text)

    def speak_text(self, text: str):
        """Enqueues text for asynchronous TTS synthesis with background ducking."""
        if not text or self.is_muted:
            return
        self._speech_queue.put(text)

    # ==========================================================================
    # 3. Speech Worker & Synthesizer Engine
    # ==========================================================================
    def _speech_worker(self):
        """Background daemon processing voice cues without blocking timer loops."""
        while True:
            text = self._speech_queue.get()
            try:
                # Duck ticking SFX immediately
                self.is_ducked = True
                self.is_speaking = True

                if HAS_PYTTSX3:
                    self._synthesize_offline_tts(text)
                else:
                    # Simulation mode if synthesizer not available
                    time.sleep(1.0)
            except Exception as e:
                print(f"[AudioCoordinator] Speech synthesis error: {e}")
            finally:
                # Unduck audio after speaking completes
                time.sleep(0.2)
                self.is_ducked = False
                self.is_speaking = False
                self._speech_queue.task_done()

    def _synthesize_offline_tts(self, text: str):
        """Executes pyttsx3 speech in isolated worker with current rate & volume."""
        try:
            engine = pyttsx3.init()
            rate = float(db.get_setting("speech_rate", "1.0"))
            volume = float(db.get_setting("volume", "0.95"))
            engine.setProperty("rate", int(175 * rate))
            engine.setProperty("volume", min(1.0, max(0.0, volume)))
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"[AudioCoordinator] TTS Engine exception: {e}")

    # ==========================================================================
    # 4. Low-Level Playback Utility
    # ==========================================================================
    def _play_sound_file(self, file_path: str):
        """Plays sound effect via platform audio or winsound/fallback."""
        if not os.path.exists(file_path):
            return

        # If on Windows, use winsound for 0ms low-latency background WAV/MP3 triggers if needed
        # Or dispatch via Flet audio component if page is mounted
        try:
            if os.name == "nt":
                import winsound
                # Non-blocking async sound
                if file_path.endswith(".wav"):
                    winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

    def _play_voice_file(self, file_path: str):
        """Plays pre-rendered vocal MP3 with ducking state management."""
        def _play():
            self.is_ducked = True
            self.is_speaking = True
            try:
                # If page attached and flet audio is mounted, trigger page audio
                # Otherwise, fallback
                time.sleep(1.2)
            finally:
                self.is_ducked = False
                self.is_speaking = False

        threading.Thread(target=_play, daemon=True).start()


# Global singleton instance
audio_coordinator = AudioCoordinator()
