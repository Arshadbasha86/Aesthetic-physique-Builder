"""
Aesthetic Physique Builder - Configuration Subsystem
Relative Path: frontend_app/config/default_config.py
Architectural Role: Authoritative static configuration, layout constants,
timing thresholds, asset path mappings, and fallback defaults for the client.
"""

import os
from pathlib import Path

# ==============================================================================
# 1. Application Metadata & Versioning
# ==============================================================================
APP_NAME = "Aesthetic Physique Builder"
APP_SLOGAN = "Make Your Body Better"
APP_VERSION = "1.1.1-alpha"
BUILD_NUMBER = 101

# ==============================================================================
# 2. Viewport & Responsive Layout Constraints
# Strict 460px mobile width container with letterboxing on wider displays
# ==============================================================================
MOBILE_VIEWPORT_WIDTH = 460
MOBILE_VIEWPORT_HEIGHT = 840
LETTERBOX_BREAKPOINT = 500

# Backdrop and surface color tokens
COLOR_LETTERBOX_BG = "#0D1117"       # Slate dark tone for widescreen letterboxing
COLOR_SURFACE_LIGHT = "#FFFFFF"      # Mobile card surface default
COLOR_SURFACE_DARK = "#121212"       # Dark surface variant
COLOR_BG_PRIMARY = "#F8FAFC"         # Clean neutral background
COLOR_PRIMARY = "#1E293B"            # Deep slate primary accent
COLOR_ACCENT = "#0EA5E9"             # Athletic electric blue
COLOR_SUCCESS = "#10B981"            # Emerald green check
COLOR_WARNING = "#F59E0B"            # Amber warning
COLOR_DANGER = "#EF4444"             # Coral red alert
COLOR_LOCK_OVERLAY = "#00000088"     # Transparent touch-lock suppressor mask

# Tier Colors for Badges and Leaderboard
TIER_COLORS = {
    "bronze": "#CD7F32",
    "silver": "#C0C0C0",
    "gold": "#FFD700",
    "platinum": "#E5E4E2",
}

# ==============================================================================
# 3. Path & Asset Directory Mapping
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
WORKOUTS_MEDIA_DIR = ASSETS_DIR / "images" / "workouts"
AUDIO_DIR = ASSETS_DIR / "audio"
SFX_DIR = AUDIO_DIR / "sfx"
COACH_VOICE_DIR = AUDIO_DIR / "coach"
DATABASE_DIR = BASE_DIR / "database"
DB_FILE_PATH = DATABASE_DIR / "aesthetic_physique.db"

# ==============================================================================
# 4. Timing Engine Constants (Wall-Clock Synchronization)
# ==============================================================================
SPLASH_SCREEN_DURATION_SEC = 2.0     # 2.0s branded splash before dissolve
TICK_INTERVAL_SEC = 1.0              # Standard 1-second cadence
COUNTDOWN_CUE_THRESHOLDS = (3, 2, 1) # Voice announcements at 3, 2, 1
REST_ADD_BUTTON_SECONDS = 20         # +20s button rest extension
POST_SET_WHISTLE_DELAY_MS = 400      # 400ms pause after whistle before "Take a rest"
SCREEN_LOCK_HOLD_DURATION_SEC = 1.5  # Long press to unlock touch suppressor

# ==============================================================================
# 5. Audio Architecture & Voice Coaching Manifest
# ==============================================================================
AVAILABLE_COACH_PERSONAS = {
    "william": {
        "name": "William",
        "accent": "British (en-GB)",
        "style": "Friendly / Structured",
        "voice_id": "en-GB-RyanNeural"
    },
    "james": {
        "name": "James",
        "accent": "United States (en-US)",
        "style": "Energetic / High Tempo",
        "voice_id": "en-US-GuyNeural"
    },
    "lily": {
        "name": "Lily",
        "accent": "British (en-GB)",
        "style": "Standard / Calm",
        "voice_id": "en-GB-SoniaNeural"
    },
    "emily": {
        "name": "Emily",
        "accent": "United States (en-US)",
        "style": "Cheerful / Supportive",
        "voice_id": "en-US-JennyNeural"
    },
    "device_tts": {
        "name": "System Default",
        "accent": "Device OS",
        "style": "Native Device Synthesizer",
        "voice_id": "system_tts"
    }
}
DEFAULT_COACH_PERSONA = "william"

# SFX Cues
SFX_TICK = "tick.mp3"
SFX_WHISTLE = "whistle.mp3"
SFX_BELL = "bell.mp3"

# ==============================================================================
# 6. Default Week Cycle Mapping (7-Day Program)
# ==============================================================================
DEFAULT_WEEK_SCHEDULE = {
    "Monday": "DAY-A",     # Spinal Decompression & Upper Body A
    "Tuesday": "DAY-B",    # Hip Mobility & Lower Body A
    "Wednesday": "DAY-C",  # Active Recovery / Mid-Week Rest
    "Thursday": "DAY-D",   # Posture Alignment & Upper Body B
    "Friday": "DAY-E",     # Yoga Flow & Lower Body B
    "Saturday": "DAY-F",   # Full Recovery
    "Sunday": "DAY-G",     # Full Recovery
}

DAY_ROUTINE_NAMES = {
    "DAY-A": "Spinal Decompression & Upper Body A",
    "DAY-B": "Hip Mobility & Lower Body A",
    "DAY-C": "Active Recovery / Mid-Week Rest",
    "DAY-D": "Posture Alignment & Upper Body B",
    "DAY-E": "Yoga Flow & Lower Body B",
    "DAY-F": "Full Recovery",
    "DAY-G": "Full Recovery",
}

# ==============================================================================
# 7. Default Biometrics & Personal Metric Bounds
# ==============================================================================
DEFAULT_BIOMETRICS = {
    "current_weight_kg": 65.0,
    "target_weight_kg": 70.0,
    "height_cm": 175.0,
    "age_years": 21,
    "biological_sex": "male",
    "body_fat_pct": None,
    "activity_tier": "moderate",
}

BIOMETRIC_BOUNDS = {
    "weight_min_kg": 30.0,
    "weight_max_kg": 250.0,
    "height_min_cm": 100.0,
    "height_max_cm": 250.0,
    "age_min": 10,
    "age_max": 100,
}

# ==============================================================================
# 8. Habit Ledgers & Daily Target Baselines
# ==============================================================================
DEFAULT_WATER_TARGET_ML = 3000
DEFAULT_SLEEP_TARGET_HOURS = 8.0
DEFAULT_PROTEIN_TARGET_GM = 120

# ==============================================================================
# 9. Server & Dynamic Endpoints Fallback
# ==============================================================================
DEFAULT_DYNAMIC_CONFIG = {
    "website_url": "https://aestheticphysique.app",
    "web_portal_url": "https://portal.aestheticphysique.app",
    "admin_portal_url": "https://admin.aestheticphysique.app",
    "terms_privacy_url": "https://aestheticphysique.app/legal",
    "support_email": "support@aestheticphysique.app",
}
