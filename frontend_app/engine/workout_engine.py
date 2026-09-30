"""
Aesthetic Physique Builder - Non-Drift Workout Wall-Clock & Unilateral Engine
Relative Path: frontend_app/engine/workout_engine.py
Architectural Role: Core workout coordinator managing wall-clock timing,
unilateral limb alternating state machine (Left -> Intra-Rest -> Right -> Inter-Rest),
audio countdown synchronization, session cache updates, and set lifecycle.
"""

import time
import threading
from typing import Optional, Dict, Any, List, Callable

from config.exercise_catalog import EXERCISE_DIRECTORY, get_routine
from config.default_config import REST_ADD_BUTTON_SECONDS
from engine.audio_coordinator import audio_coordinator
from database.db_manager import db


class WorkoutEngine:
    """
    Wall-Clock Workout State Machine.
    Guarantees non-drift countdowns and enforces unilateral alternating rest mechanics.
    """
    def __init__(self):
        self.day_id: str = "DAY-A"
        self.session_type: str = "evening"
        self.routine_name: str = ""
        self.exercises: List[Dict[str, Any]] = []

        # Session indices
        self.current_exercise_index: int = 0
        self.current_set_index: int = 0
        self.active_side: str = "NONE"       # 'LEFT', 'RIGHT', 'NONE'
        self.current_sub_phase: str = "PRE_SET" # 'PRE_SET', 'ACTIVE_SET', 'INTRA_SET_REST', 'INTER_SET_REST', 'COMPLETED'

        # Wall-clock timer properties
        self.target_end_timestamp: float = 0.0
        self.total_phase_duration: int = 0
        self.is_paused: bool = False
        self.pause_time_remaining: int = 0
        self.is_screen_locked: bool = False

        # Session metrics
        self.session_start_time: float = 0.0
        self.total_tonnage_kg: float = 0.0
        self.total_completed_sets: int = 0
        self.total_expected_sets: int = 0

        # UI reactive callbacks
        self.on_tick_callback: Optional[Callable[[int, float], None]] = None
        self.on_state_change_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None
        self.on_session_completed_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        self.on_request_reps_input_callback: Optional[Callable[[str, int], None]] = None

        # Background thread control
        self._timer_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._last_announced_second: int = -1

    # ==========================================================================
    # 1. Session Setup & Resumption
    # ==========================================================================
    def load_routine(self, day_id: str, session_type: str = "evening") -> bool:
        """Loads prescribed routine and computes total sets."""
        self.day_id = day_id
        self.session_type = session_type.lower()
        routine = get_routine(day_id, self.session_type)
        if not routine or not routine.get("exercises"):
            return False

        self.routine_name = routine.get("name", f"{day_id} {session_type.capitalize()}")
        self.exercises = routine["exercises"]
        self.current_exercise_index = 0
        self.current_set_index = 0
        self.current_sub_phase = "PRE_SET"

        # Calculate total set volume
        self.total_expected_sets = sum(item.get("sets", 1) for item in self.exercises)
        self.total_completed_sets = 0
        return True

    def resume_from_saved_state(self, saved_state: Dict[str, Any]) -> bool:
        """Restores session from local SQLite cache."""
        if not self.load_routine(saved_state["day_id"], saved_state["session_type"]):
            return False
        self.current_exercise_index = saved_state.get("current_exercise_index", 0)
        self.current_set_index = saved_state.get("current_set_index", 0)
        self.active_side = saved_state.get("active_side", "NONE")
        self.current_sub_phase = saved_state.get("current_sub_phase", "ACTIVE_SET")
        self.is_screen_locked = bool(saved_state.get("is_screen_locked", 0))
        return True

    # ==========================================================================
    # 2. Workout Execution Lifecycle
    # ==========================================================================
    def start_workout(self):
        """Starts the active session timer thread."""
        self.session_start_time = time.time()
        self._stop_event.clear()
        self._start_active_set()

        if self._timer_thread is None or not self._timer_thread.is_alive():
            self._timer_thread = threading.Thread(target=self._run_timer_loop, daemon=True)
            self._timer_thread.start()

    def _start_active_set(self):
        """Mounts active set, sets up unilateral limbs, and initializes timers."""
        if self.current_exercise_index >= len(self.exercises):
            self._complete_workout()
            return

        current_item = self.exercises[self.current_exercise_index]
        ex_meta = EXERCISE_DIRECTORY.get(current_item["exercise_id"], {})
        is_unilateral = ex_meta.get("unilateral", False)

        if is_unilateral:
            if self.active_side == "NONE" or self.active_side == "RIGHT":
                self.active_side = "LEFT"
        else:
            self.active_side = "NONE"

        self.current_sub_phase = "ACTIVE_SET"
        mode = ex_meta.get("execution_mode", "repetition_count")

        if mode == "timed_hold":
            duration = current_item.get("target", ex_meta.get("default_target_value", 30))
            self.total_phase_duration = duration
            self.target_end_timestamp = time.time() + duration
        else:
            # Repetition / until_failure stopwatch
            self.total_phase_duration = 0
            self.target_end_timestamp = time.time()

        self._last_announced_second = -1
        self._persist_session()
        self._notify_state_change()

    def complete_current_set(self, actual_reps: Optional[int] = None):
        """Called when a set finishes (timer expires or Done checkmark tapped)."""
        if self.current_exercise_index >= len(self.exercises):
            return

        current_item = self.exercises[self.current_exercise_index]
        ex_meta = EXERCISE_DIRECTORY.get(current_item["exercise_id"], {})
        is_unilateral = ex_meta.get("unilateral", False)
        mode = ex_meta.get("execution_mode", "repetition_count")

        # Check if Until Failure modal is required
        if mode == "until_failure" and actual_reps is None:
            if self.on_request_reps_input_callback:
                self.on_request_reps_input_callback(ex_meta.get("name", "Exercise"), current_item.get("target", 15))
                return

        # Record set entry in SQLite
        reps = actual_reps or current_item.get("target", 15) if mode != "timed_hold" else None
        hold_sec = current_item.get("target", 30) if mode == "timed_hold" else None
        db.add_activity_entry(
            session_id="active_live_session",
            movement_name=ex_meta.get("name", "Exercise"),
            sequence_order=self.current_exercise_index,
            entry_type="time_hold" if mode == "timed_hold" else "weight_reps",
            weight_kg=5.0 if "Dumbbells" in ex_meta.get("equipment_required", []) else 0.0,
            reps_completed=reps,
            hold_duration_sec=hold_sec,
            is_unilateral=is_unilateral,
            limb_designation=self.active_side.lower() if is_unilateral else "bilateral"
        )

        # Unilateral vs Bilateral Transition Logic
        if is_unilateral and self.active_side == "LEFT":
            # SIDE A COMPLETE -> Transition to INTRA-SET REST
            intra_rest = ex_meta.get("intra_set_rest_seconds", 20)
            self.current_sub_phase = "INTRA_SET_REST"
            self.total_phase_duration = intra_rest
            self.target_end_timestamp = time.time() + intra_rest
            audio_coordinator.play_set_completion_sequence(transition_prompt="Switch sides")
        else:
            # BILATERAL OR SIDE B COMPLETE -> Transition to INTER-SET REST
            self.total_completed_sets += 1
            max_sets = current_item.get("sets", 1)
            inter_rest = current_item.get("rest_seconds", ex_meta.get("rest_after_seconds", 60))

            if self.current_set_index + 1 < max_sets:
                # More sets of same exercise remain
                self.current_set_index += 1
                self.current_sub_phase = "INTER_SET_REST"
                self.total_phase_duration = inter_rest
                self.target_end_timestamp = time.time() + inter_rest
                audio_coordinator.play_set_completion_sequence(transition_prompt="Take a rest")
            else:
                # Advance to next exercise
                if self.current_exercise_index + 1 < len(self.exercises):
                    self.current_exercise_index += 1
                    self.current_set_index = 0
                    self.current_sub_phase = "INTER_SET_REST"
                    self.total_phase_duration = inter_rest
                    self.target_end_timestamp = time.time() + inter_rest
                    audio_coordinator.play_set_completion_sequence(transition_prompt="Take a rest")
                else:
                    self._complete_workout()
                    return

        self._last_announced_second = -1
        self._persist_session()
        self._notify_state_change()

    # ==========================================================================
    # 3. Rest Modifiers
    # ==========================================================================
    def add_rest_time(self, seconds: int = REST_ADD_BUTTON_SECONDS):
        """Adds +20 seconds to remaining rest without resetting ticking state."""
        if self.current_sub_phase in ("INTRA_SET_REST", "INTER_SET_REST"):
            self.target_end_timestamp += seconds
            self.total_phase_duration += seconds
            self._persist_session()

    def skip_rest(self):
        """Immediately ends rest, rings bell, and mounts the next active set."""
        if self.current_sub_phase in ("INTRA_SET_REST", "INTER_SET_REST"):
            audio_coordinator.play_bell()
            if self.current_sub_phase == "INTRA_SET_REST":
                self.active_side = "RIGHT"
                self._start_active_set()
            else:
                self._start_active_set()

    # ==========================================================================
    # 4. Timer Thread & Audio Countdown Logic
    # ==========================================================================
    def _run_timer_loop(self):
        """Continuous non-drift 200ms evaluation loop."""
        while not self._stop_event.is_set():
            time.sleep(0.2)
            if self.is_paused or self.current_sub_phase == "COMPLETED":
                continue

            now = time.time()
            if self.current_sub_phase in ("INTRA_SET_REST", "INTER_SET_REST"):
                # Rest countdown
                remaining = max(0, int(round(self.target_end_timestamp - now)))
                fraction = 1.0 - (remaining / max(1, self.total_phase_duration))

                if self.on_tick_callback:
                    self.on_tick_callback(remaining, fraction)

                self._process_countdown_audio(remaining)

                if remaining <= 0:
                    self.skip_rest()

            elif self.current_sub_phase == "ACTIVE_SET":
                current_item = self.exercises[self.current_exercise_index]
                ex_meta = EXERCISE_DIRECTORY.get(current_item["exercise_id"], {})
                mode = ex_meta.get("execution_mode", "repetition_count")

                if mode == "timed_hold":
                    remaining = max(0, int(round(self.target_end_timestamp - now)))
                    fraction = 1.0 - (remaining / max(1, self.total_phase_duration))

                    if self.on_tick_callback:
                        self.on_tick_callback(remaining, fraction)

                    self._process_countdown_audio(remaining)

                    if remaining <= 0:
                        self.complete_current_set()
                else:
                    # Stopwatch upward count
                    elapsed = int(round(now - self.target_end_timestamp))
                    if self.on_tick_callback:
                        self.on_tick_callback(elapsed, 0.0)

    def _process_countdown_audio(self, remaining: int):
        """Fires 1s ticks when T > 3, spoken countdown at 3, 2, 1, and bells at 0."""
        if remaining == self._last_announced_second:
            return

        self._last_announced_second = remaining
        if remaining > 3:
            audio_coordinator.play_tick()
        elif remaining == 3:
            audio_coordinator.speak_cue("three", fallback_text="Three")
        elif remaining == 2:
            audio_coordinator.speak_cue("two", fallback_text="Two")
        elif remaining == 1:
            audio_coordinator.speak_cue("one", fallback_text="One")

    # ==========================================================================
    # 5. Session Completion & State Management
    # ==========================================================================
    def _complete_workout(self):
        """Wraps up session, creates activity record, and credits daily streak."""
        self.current_sub_phase = "COMPLETED"
        self._stop_event.set()
        duration_seconds = int(time.time() - self.session_start_time)

        # Log session to database
        session_id = db.create_activity_session(
            activity_type="resistance" if "Upper" in self.routine_name or "Lower" in self.routine_name else "yoga",
            session_title=self.routine_name,
            duration_seconds=duration_seconds,
            total_tonnage_kg=self.total_tonnage_kg,
            total_poses_completed=len(self.exercises)
        )
        db.clear_active_session()
        db.record_day_completed()

        summary_data = {
            "session_id": session_id,
            "routine_name": self.routine_name,
            "duration_seconds": duration_seconds,
            "total_sets": self.total_completed_sets
        }
        if self.on_session_completed_callback:
            self.on_session_completed_callback(summary_data)

    def pause_session(self):
        if not self.is_paused:
            self.is_paused = True
            self.pause_time_remaining = max(0, int(round(self.target_end_timestamp - time.time())))
            self._persist_session()

    def resume_session(self):
        if self.is_paused:
            self.is_paused = False
            self.target_end_timestamp = time.time() + self.pause_time_remaining
            self._persist_session()

    def toggle_screen_lock(self) -> bool:
        self.is_screen_locked = not self.is_screen_locked
        self._persist_session()
        return self.is_screen_locked

    def _persist_session(self):
        """Writes current execution coordinates to SQLite active_session_state."""
        pct = int((self.total_completed_sets / max(1, self.total_expected_sets)) * 100)
        db.save_active_session(
            day_id=self.day_id,
            session_type=self.session_type,
            current_exercise_index=self.current_exercise_index,
            current_set_index=self.current_set_index,
            active_side=self.active_side,
            current_sub_phase=self.current_sub_phase,
            completion_percentage=pct,
            target_end_timestamp=self.target_end_timestamp,
            is_paused=1 if self.is_paused else 0,
            is_screen_locked=1 if self.is_screen_locked else 0
        )

    def _notify_state_change(self):
        if self.on_state_change_callback:
            current_ex = self.exercises[self.current_exercise_index] if self.current_exercise_index < len(self.exercises) else {}
            self.on_state_change_callback(self.current_sub_phase, {
                "exercise": current_ex,
                "exercise_index": self.current_exercise_index,
                "set_index": self.current_set_index,
                "active_side": self.active_side,
                "duration": self.total_phase_duration
            })


# Global workout engine singleton
workout_engine = WorkoutEngine()
