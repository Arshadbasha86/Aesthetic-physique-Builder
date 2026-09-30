-- ==============================================================================
-- Aesthetic Physique Builder - Local SQLite Offline Schema (WAL Mode)
-- Relative Path: frontend_app/database/local_schema.sql
-- Architectural Role: Authoritative local database DDL establishing offline-first
-- persistence for workouts, habits, gamification, settings, and sync outbox.
-- ==============================================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- 1. App Lifecycle & Installation State
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS app_config (
    config_key TEXT PRIMARY KEY,
    config_value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Pre-populate onboarding default flags
INSERT OR IGNORE INTO app_config (config_key, config_value) VALUES 
    ('app_version', '1.1.1-alpha'),
    ('first_time_user', 'true'),
    ('has_seen_disclaimer', 'false'),
    ('has_seen_warning', 'false'),
    ('is_onboarding_completed', 'false'),
    ('installed_timestamp', strftime('%s', 'now')),
    ('website_url', 'https://aestheticphysique.app');

-- Week Schedule Mapping (Calendar Day -> Routine DAY-A..DAY-G)
CREATE TABLE IF NOT EXISTS week_schedule (
    day_of_week TEXT PRIMARY KEY, -- 'Monday', 'Tuesday', ..., 'Sunday'
    routine_day_id TEXT NOT NULL,  -- 'DAY-A', 'DAY-B', ..., 'DAY-G'
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO week_schedule (day_of_week, routine_day_id) VALUES
    ('Monday', 'DAY-A'),
    ('Tuesday', 'DAY-B'),
    ('Wednesday', 'DAY-C'),
    ('Thursday', 'DAY-D'),
    ('Friday', 'DAY-E'),
    ('Saturday', 'DAY-F'),
    ('Sunday', 'DAY-G');

-- ------------------------------------------------------------------------------
-- 2. User Profile & Biometrics
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_profile (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL DEFAULT 'athlete',
    full_name TEXT NOT NULL DEFAULT 'Athlete',
    email TEXT DEFAULT 'athlete@aestheticphysique.app',
    avatar_url TEXT,
    banner_url TEXT,
    equipped_title TEXT DEFAULT 'Novice Trainee',
    tier TEXT NOT NULL DEFAULT 'bronze',
    current_weight_kg REAL NOT NULL DEFAULT 65.0,
    target_weight_kg REAL NOT NULL DEFAULT 70.0,
    height_cm REAL NOT NULL DEFAULT 175.0,
    age_years INTEGER NOT NULL DEFAULT 21,
    biological_sex TEXT NOT NULL DEFAULT 'male',
    body_fat_pct REAL,
    activity_tier TEXT NOT NULL DEFAULT 'moderate',
    is_synced INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Seed single local default athlete
INSERT OR IGNORE INTO user_profile (user_id, username, full_name) 
VALUES ('local_athlete_001', 'athlete_basha', 'Athlete');

-- ------------------------------------------------------------------------------
-- 3. Hardware & System Settings
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_settings (
    setting_key TEXT PRIMARY KEY,
    setting_value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO user_settings (setting_key, setting_value) VALUES
    ('voice_tts_enabled', 'true'),
    ('selected_persona', 'william'),
    ('speech_rate', '1.0'),
    ('pitch', '1.0'),
    ('volume', '0.95'),
    ('voice_commands_enabled', 'false'),
    ('haptics_enabled', 'true'),
    ('screen_awake_during_workout', 'true'),
    ('dnd_during_workout', 'false'),
    ('auto_backup_enabled', 'true'),
    ('daily_reminder_enabled', 'true'),
    ('daily_reminder_time', '06:30'),
    ('preferred_units', 'metric'); -- 'metric' (kg, cm) or 'imperial' (lbs, ft-in)

-- ------------------------------------------------------------------------------
-- 4. In-Workout Session Cache (State Interruption Recovery)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS active_session_state (
    id INTEGER PRIMARY KEY CHECK (id = 1), -- Single-row singleton cache
    day_id TEXT NOT NULL,                  -- e.g. 'DAY-A'
    session_type TEXT NOT NULL,            -- 'morning' or 'evening'
    current_exercise_index INTEGER NOT NULL DEFAULT 0,
    current_set_index INTEGER NOT NULL DEFAULT 0,
    active_side TEXT NOT NULL DEFAULT 'NONE', -- 'LEFT', 'RIGHT', 'NONE'
    current_sub_phase TEXT NOT NULL DEFAULT 'ACTIVE_SET', -- 'ACTIVE_SET', 'INTRA_SET_REST', 'INTER_SET_REST'
    completion_percentage INTEGER NOT NULL DEFAULT 0,
    target_end_timestamp REAL DEFAULT 0,
    is_paused INTEGER NOT NULL DEFAULT 0,
    is_screen_locked INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ------------------------------------------------------------------------------
-- 5. Workout & Yoga Activity Historical Ledgers
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS activity_sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    activity_type TEXT NOT NULL, -- 'resistance', 'yoga', 'hybrid_mobility'
    session_title TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    total_tonnage_kg REAL NOT NULL DEFAULT 0.0,
    total_poses_completed INTEGER NOT NULL DEFAULT 0,
    average_intensity_rpe REAL,
    notes TEXT,
    sync_state TEXT NOT NULL DEFAULT 'pending_insert', -- 'synced', 'pending_insert', 'pending_update'
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS activity_entries (
    entry_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    movement_name TEXT NOT NULL,
    sequence_order INTEGER NOT NULL,
    entry_type TEXT NOT NULL, -- 'weight_reps', 'time_hold', 'breath_cycles'
    weight_kg REAL,
    reps_completed INTEGER,
    hold_duration_sec INTEGER,
    is_unilateral INTEGER NOT NULL DEFAULT 0,
    limb_designation TEXT NOT NULL DEFAULT 'bilateral', -- 'bilateral', 'left', 'right'
    rpe_rating REAL,
    is_warmup INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (session_id) REFERENCES activity_sessions (session_id) ON DELETE CASCADE
);

-- ------------------------------------------------------------------------------
-- 6. Biological Habit Ledgers (Water, Sleep, Protein)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS water_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date TEXT NOT NULL, -- 'YYYY-MM-DD'
    amount_ml INTEGER NOT NULL,
    logged_at TEXT NOT NULL DEFAULT (datetime('now')),
    sync_state TEXT NOT NULL DEFAULT 'pending_insert'
);

CREATE TABLE IF NOT EXISTS sleep_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date TEXT NOT NULL, -- 'YYYY-MM-DD'
    in_time TEXT NOT NULL,  -- 'HH:MM' or 'YYYY-MM-DD HH:MM'
    out_time TEXT NOT NULL, -- 'HH:MM' or 'YYYY-MM-DD HH:MM'
    duration_minutes INTEGER NOT NULL,
    quality_tier TEXT NOT NULL DEFAULT 'Good Sleep', -- 'Excellent Sleep', 'Good Sleep', 'Average Sleep', 'Bad Sleep'
    logged_at TEXT NOT NULL DEFAULT (datetime('now')),
    sync_state TEXT NOT NULL DEFAULT 'pending_insert'
);

CREATE TABLE IF NOT EXISTS protein_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date TEXT NOT NULL, -- 'YYYY-MM-DD'
    timing_window TEXT NOT NULL, -- 'before_workout', 'after_workout', 'daily_total'
    amount_gm REAL NOT NULL,
    logged_at TEXT NOT NULL DEFAULT (datetime('now')),
    sync_state TEXT NOT NULL DEFAULT 'pending_insert'
);

-- ------------------------------------------------------------------------------
-- 7. Gamification, Badges & Consistency Streaks
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS daily_streaks (
    user_id TEXT PRIMARY KEY,
    current_streak_days INTEGER NOT NULL DEFAULT 0,
    longest_streak_days INTEGER NOT NULL DEFAULT 0,
    last_completed_date TEXT,
    streak_freeze_active INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO daily_streaks (user_id, current_streak_days, longest_streak_days)
VALUES ('local_athlete_001', 1, 1);

CREATE TABLE IF NOT EXISTS badge_definitions (
    badge_id TEXT PRIMARY KEY,
    badge_name TEXT NOT NULL,
    tier TEXT NOT NULL, -- 'bronze', 'silver', 'gold', 'platinum'
    associated_title TEXT,
    artwork_url TEXT,
    assignment_criteria TEXT,
    rule_type TEXT,
    rule_parameters TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);

-- Insert baseline achievements
INSERT OR IGNORE INTO badge_definitions (badge_id, badge_name, tier, associated_title, artwork_url, assignment_criteria) VALUES
    ('first_step', 'First Session', 'bronze', 'Initiate', 'assets/badges/first_step.png', 'Complete your first workout session'),
    ('iron_consistency_7', 'Iron Consistency', 'bronze', 'Consistent', 'assets/badges/iron_7.png', 'Maintain a 7-day workout streak'),
    ('steel_grit_14', 'Steel Grit', 'silver', 'Disciplined', 'assets/badges/steel_14.png', 'Maintain a 14-day workout streak'),
    ('titan_consistency_30', 'Titan of Consistency', 'gold', 'Consistency Titan', 'assets/badges/titan_30.png', 'Maintain a 30-day unbroken streak'),
    ('century_smasher', 'Century Smasher', 'platinum', 'Centurion', 'assets/badges/century_100.png', 'Complete 100 sets taken to failure'),
    ('hydration_master', 'Hydration Master', 'silver', 'Pure Hydrated', 'assets/badges/hydration.png', 'Hit 3000ml water goal for 7 consecutive days'),
    ('sleep_guardian', 'Sleep Guardian', 'silver', 'Deep Sleeper', 'assets/badges/sleep.png', 'Log 8+ hours sleep with Good/Excellent tier for 7 days');

CREATE TABLE IF NOT EXISTS user_badges (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    badge_id TEXT NOT NULL,
    assigned_by TEXT DEFAULT 'automated_rule',
    assignment_type TEXT DEFAULT 'automated_rule', -- 'automated_rule', 'manual_admin', 'event_grant'
    awarded_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (badge_id) REFERENCES badge_definitions (badge_id)
);

-- Grant starter badge
INSERT OR IGNORE INTO user_badges (id, user_id, badge_id)
VALUES ('ub_starter_001', 'local_athlete_001', 'first_step');

-- ------------------------------------------------------------------------------
-- 8. Customer Support Desk Ledger (Offline-First Ticket Enclave)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'feedback', -- 'bug', 'feedback', 'workout_help', 'billing'
    status TEXT NOT NULL DEFAULT 'open',        -- 'open', 'in_progress', 'resolved'
    has_unread_reply INTEGER NOT NULL DEFAULT 0,
    sync_state TEXT NOT NULL DEFAULT 'pending_insert',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS support_messages (
    message_id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    sender_type TEXT NOT NULL, -- 'user' or 'admin'
    body TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (ticket_id) REFERENCES support_tickets (ticket_id) ON DELETE CASCADE
);

-- ------------------------------------------------------------------------------
-- 9. Offline Mutation Journal (Sync Outbox Queue)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sync_outbox (
    outbox_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mutation_type TEXT NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    entity_table TEXT NOT NULL,  -- 'user_profile', 'activity_sessions', etc.
    entity_id TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'syncing', 'failed'
    retry_count INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    synced_at TEXT
);
