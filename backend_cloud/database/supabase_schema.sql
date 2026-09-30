-- ====================================================================
-- Aesthetic Physique - Supabase PostgreSQL Production Schema
-- Architectural Role: Remote cloud database schema with foreign keys,
-- indexes, Row-Level Security (RLS) policies, and administrative audit trails.
-- ====================================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- --------------------------------------------------------------------
-- 1. Athletes & Profiles (Mirrors local SQLite users table & auth)
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.athletes (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    avatar_url TEXT,
    vanity_tier TEXT NOT NULL DEFAULT 'Bronze' CHECK (vanity_tier IN ('Bronze', 'Silver', 'Gold', 'Platinum')),
    active_title TEXT NOT NULL DEFAULT 'The Aesthetic Initiate',
    role TEXT NOT NULL DEFAULT 'ATHLETE' CHECK (role IN ('ATHLETE', 'COACH', 'ADMIN', 'SUPER_ADMIN')),
    account_status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK (account_status IN ('ACTIVE', 'SUSPENDED', 'BANNED')),
    weight_kg NUMERIC(5, 2) DEFAULT 75.0,
    height_cm NUMERIC(5, 2) DEFAULT 178.0,
    current_streak_days INT NOT NULL DEFAULT 0,
    longest_streak_days INT NOT NULL DEFAULT 0,
    lifetime_failure_reps INT NOT NULL DEFAULT 0,
    total_workouts_completed INT NOT NULL DEFAULT 0,
    water_daily_target_ml INT NOT NULL DEFAULT 3500,
    protein_daily_target_g INT NOT NULL DEFAULT 150,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_athletes_email ON public.athletes(email);
CREATE INDEX IF NOT EXISTS idx_athletes_streak ON public.athletes(current_streak_days DESC);
CREATE INDEX IF NOT EXISTS idx_athletes_tier ON public.athletes(vanity_tier);

-- --------------------------------------------------------------------
-- 2. Badges & Accolades Catalog
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.badges (
    badge_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tier TEXT NOT NULL CHECK (tier IN ('Bronze', 'Silver', 'Gold', 'Platinum')),
    associated_title TEXT NOT NULL,
    description TEXT NOT NULL,
    glyph TEXT NOT NULL DEFAULT 'fitness_center_rounded',
    artwork_url TEXT,
    constraint_type TEXT NOT NULL CHECK (constraint_type IN ('STREAK_DAYS', 'TOTAL_FAILURE_REPS', 'HYDRATION_STREAK', 'SLEEP_CONSISTENCY', 'MANUAL_AWARD')),
    constraint_threshold INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- --------------------------------------------------------------------
-- 3. Athlete Badges & Unlocks
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.athlete_badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    athlete_id UUID NOT NULL REFERENCES public.athletes(id) ON DELETE CASCADE,
    badge_id TEXT NOT NULL REFERENCES public.badges(badge_id) ON DELETE CASCADE,
    unlocked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_equipped BOOLEAN NOT NULL DEFAULT FALSE,
    assigned_by TEXT NOT NULL DEFAULT 'SYSTEM_RULE', -- 'SYSTEM_RULE' or Admin User ID
    assignment_justification TEXT,
    UNIQUE(athlete_id, badge_id)
);

CREATE INDEX IF NOT EXISTS idx_athlete_badges_user ON public.athlete_badges(athlete_id);

-- --------------------------------------------------------------------
-- 4. Workout Sessions & Performance Telemetry
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.workout_sessions (
    session_id TEXT PRIMARY KEY,
    athlete_id UUID NOT NULL REFERENCES public.athletes(id) ON DELETE CASCADE,
    split_day TEXT NOT NULL, -- e.g. 'DAY-A', 'DAY-B'
    period TEXT NOT NULL CHECK (period IN ('morning', 'evening')),
    routine_name TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    duration_seconds INT NOT NULL DEFAULT 0,
    total_sets_completed INT NOT NULL DEFAULT 0,
    total_failure_reps INT NOT NULL DEFAULT 0,
    wall_clock_rest_compliance NUMERIC(5, 2) DEFAULT 100.0,
    status TEXT NOT NULL DEFAULT 'COMPLETED' CHECK (status IN ('COMPLETED', 'ABANDONED', 'IN_PROGRESS')),
    sync_status TEXT NOT NULL DEFAULT 'SYNCED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sessions_athlete ON public.workout_sessions(athlete_id, started_at DESC);

-- --------------------------------------------------------------------
-- 5. Workout Sets (Detailed Failure Reps & Weight)
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.workout_sets (
    set_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES public.workout_sessions(session_id) ON DELETE CASCADE,
    exercise_id TEXT NOT NULL,
    exercise_name TEXT NOT NULL,
    set_number INT NOT NULL,
    side TEXT CHECK (side IN ('LEFT', 'RIGHT', 'BILATERAL')),
    target_reps INT,
    completed_reps INT NOT NULL,
    is_failure_set BOOLEAN NOT NULL DEFAULT FALSE,
    weight_kg NUMERIC(5, 2) DEFAULT 0.0,
    rest_duration_seconds INT NOT NULL DEFAULT 60,
    logged_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sets_session ON public.workout_sets(session_id);

-- --------------------------------------------------------------------
-- 6. Daily Recovery Subsystems: Water, Sleep, Protein
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.recovery_water (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    athlete_id UUID NOT NULL REFERENCES public.athletes(id) ON DELETE CASCADE,
    log_date DATE NOT NULL,
    total_consumed_ml INT NOT NULL DEFAULT 0,
    target_ml INT NOT NULL DEFAULT 3500,
    target_reached BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(athlete_id, log_date)
);

CREATE TABLE IF NOT EXISTS public.recovery_sleep (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    athlete_id UUID NOT NULL REFERENCES public.athletes(id) ON DELETE CASCADE,
    log_date DATE NOT NULL,
    in_time TIMESTAMPTZ NOT NULL,
    out_time TIMESTAMPTZ NOT NULL,
    duration_hours NUMERIC(4, 2) NOT NULL,
    quality_tier TEXT NOT NULL CHECK (quality_tier IN ('Bad', 'Average', 'Good', 'Excellent')),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(athlete_id, log_date)
);

CREATE TABLE IF NOT EXISTS public.recovery_protein (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    athlete_id UUID NOT NULL REFERENCES public.athletes(id) ON DELETE CASCADE,
    log_date DATE NOT NULL,
    total_consumed_g INT NOT NULL DEFAULT 0,
    target_g INT NOT NULL DEFAULT 150,
    pre_workout_taken BOOLEAN NOT NULL DEFAULT FALSE,
    post_workout_taken BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(athlete_id, log_date)
);

-- --------------------------------------------------------------------
-- 7. Support Desk & Feedback Inbox
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.support_tickets (
    ticket_id TEXT PRIMARY KEY,
    athlete_id UUID NOT NULL REFERENCES public.athletes(id) ON DELETE CASCADE,
    subject TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'UNREAD' CHECK (status IN ('UNREAD', 'IN_PROGRESS', 'RESOLVED')),
    priority TEXT NOT NULL DEFAULT 'NORMAL' CHECK (priority IN ('LOW', 'NORMAL', 'HIGH', 'CRITICAL')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.support_messages (
    message_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id TEXT NOT NULL REFERENCES public.support_tickets(ticket_id) ON DELETE CASCADE,
    sender_role TEXT NOT NULL CHECK (sender_role IN ('ATHLETE', 'ADMIN', 'COACH')),
    sender_id TEXT NOT NULL,
    message_body TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_support_messages_ticket ON public.support_messages(ticket_id, created_at ASC);

-- --------------------------------------------------------------------
-- 8. Administrative Immutable Audit Ledger
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.admin_audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    admin_id TEXT NOT NULL,
    target_athlete_id UUID REFERENCES public.athletes(id) ON DELETE SET NULL,
    action TEXT NOT NULL CHECK (action IN ('USER_EDIT', 'BADGE_CREATE', 'BADGE_ASSIGN', 'BADGE_REVOKE', 'SYSTEM_CONFIG', 'TICKET_REPLY')),
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    mandatory_justification TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_created ON public.admin_audit_logs(created_at DESC);

-- --------------------------------------------------------------------
-- 9. Ecosystem Version & Client Build Configuration
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.app_version_configs (
    config_key TEXT PRIMARY KEY DEFAULT 'GLOBAL_CONFIG',
    latest_mobile_version TEXT NOT NULL DEFAULT '1.2.0',
    min_required_mobile_version TEXT NOT NULL DEFAULT '1.0.0',
    apk_download_url TEXT NOT NULL DEFAULT 'https://cdn.aestheticphysique.com/builds/AestheticPhysique-v1.2.0.apk',
    documentation_url TEXT NOT NULL DEFAULT 'https://docs.aestheticphysique.com',
    force_update_flag BOOLEAN NOT NULL DEFAULT FALSE,
    release_notes TEXT NOT NULL DEFAULT '52 unilateral routines, offline-first SQLite WAL, rest timer ducking audio.',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ====================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ====================================================================
ALTER TABLE public.athletes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.athlete_badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workout_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workout_sets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.recovery_water ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.recovery_sleep ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.recovery_protein ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.support_tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.support_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.admin_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.app_version_configs ENABLE ROW LEVEL SECURITY;

-- Helper function to check if current user is an admin
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN (
        SELECT (role IN ('ADMIN', 'SUPER_ADMIN'))
        FROM public.athletes
        WHERE id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Athletes RLS
CREATE POLICY "Athletes can view their own profile" ON public.athletes
    FOR SELECT USING (auth.uid() = id OR public.is_admin());

CREATE POLICY "Athletes can update their own biometrics" ON public.athletes
    FOR UPDATE USING (auth.uid() = id OR public.is_admin());

-- Badges Catalog (Public read, admin write)
CREATE POLICY "Anyone can view active badges" ON public.badges
    FOR SELECT USING (is_active = TRUE OR public.is_admin());

CREATE POLICY "Admins can create or modify badges" ON public.badges
    FOR ALL USING (public.is_admin());

-- Athlete Badges (Read self or public leaderboard, admin write)
CREATE POLICY "Users can view badge unlocks" ON public.athlete_badges
    FOR SELECT USING (TRUE);

CREATE POLICY "Admins can assign or revoke badges" ON public.athlete_badges
    FOR ALL USING (public.is_admin() OR auth.uid() = athlete_id);

-- Workouts & Recovery RLS
CREATE POLICY "Users own their workout sessions" ON public.workout_sessions
    FOR ALL USING (auth.uid() = athlete_id OR public.is_admin());

CREATE POLICY "Users own their workout sets" ON public.workout_sets
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.workout_sessions s
            WHERE s.session_id = workout_sets.session_id AND (s.athlete_id = auth.uid() OR public.is_admin())
        )
    );

CREATE POLICY "Users own recovery water logs" ON public.recovery_water
    FOR ALL USING (auth.uid() = athlete_id OR public.is_admin());

CREATE POLICY "Users own recovery sleep logs" ON public.recovery_sleep
    FOR ALL USING (auth.uid() = athlete_id OR public.is_admin());

CREATE POLICY "Users own recovery protein logs" ON public.recovery_protein
    FOR ALL USING (auth.uid() = athlete_id OR public.is_admin());

-- Support Tickets RLS
CREATE POLICY "Users can view their tickets" ON public.support_tickets
    FOR SELECT USING (auth.uid() = athlete_id OR public.is_admin());

CREATE POLICY "Users can create tickets" ON public.support_tickets
    FOR INSERT WITH CHECK (auth.uid() = athlete_id OR public.is_admin());

CREATE POLICY "Admins can manage tickets" ON public.support_tickets
    FOR UPDATE USING (public.is_admin());

CREATE POLICY "Users and admins can view ticket messages" ON public.support_messages
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.support_tickets t
            WHERE t.ticket_id = support_messages.ticket_id AND (t.athlete_id = auth.uid() OR public.is_admin())
        )
    );

CREATE POLICY "Users and admins can append ticket messages" ON public.support_messages
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.support_tickets t
            WHERE t.ticket_id = support_messages.ticket_id AND (t.athlete_id = auth.uid() OR public.is_admin())
        )
    );

-- Audit Logs RLS (Admins only)
CREATE POLICY "Admins can view and append audit logs" ON public.admin_audit_logs
    FOR ALL USING (public.is_admin());

-- Version Config RLS (Public read, admin write)
CREATE POLICY "Everyone can read app version configs" ON public.app_version_configs
    FOR SELECT USING (TRUE);

CREATE POLICY "Admins can update app version configs" ON public.app_version_configs
    FOR UPDATE USING (public.is_admin());

-- --------------------------------------------------------------------
-- Seed Initial Accolades Catalog & Global Config
-- --------------------------------------------------------------------
INSERT INTO public.badges (badge_id, name, tier, associated_title, description, glyph, constraint_type, constraint_threshold)
VALUES
    ('BADGE_IRON_WILL', 'Iron Will', 'Gold', 'The Unyielding', 'Complete 30 consecutive workout streak days without missing.', 'fitness_center_rounded', 'STREAK_DAYS', 30),
    ('BADGE_HYDRATION_SENTINEL', 'Hydration Sentinel', 'Silver', 'Pure Flow', 'Maintain 3,500 ml daily water target for 14 consecutive days.', 'water_drop_rounded', 'HYDRATION_STREAK', 14),
    ('BADGE_TITAN_FAILURE', 'Titan of Failure', 'Platinum', 'Apex Engine', 'Complete 100 sets taken to total muscular failure.', 'local_fire_department_rounded', 'TOTAL_FAILURE_REPS', 100),
    ('BADGE_SLEEP_MONARCH', 'Sleep Monarch', 'Gold', 'Somnus Lord', 'Maintain Excellent sleep quality for 14 consecutive nights.', 'bedtime_rounded', 'SLEEP_CONSISTENCY', 14),
    ('BADGE_EARLY_BIRD', 'Dawn Vanguard', 'Bronze', 'The Early Riser', 'Complete 5 consecutive morning routines before 08:00 AM.', 'military_tech_rounded', 'STREAK_DAYS', 5)
ON CONFLICT (badge_id) DO NOTHING;

INSERT INTO public.app_version_configs (config_key, latest_mobile_version, min_required_mobile_version, apk_download_url, force_update_flag)
VALUES ('GLOBAL_CONFIG', '1.2.0', '1.0.0', 'https://cdn.aestheticphysique.com/builds/AestheticPhysique-v1.2.0.apk', FALSE)
ON CONFLICT (config_key) DO NOTHING;
