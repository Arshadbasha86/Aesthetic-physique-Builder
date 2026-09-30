-- ====================================================================
-- Aesthetic Physique - Supabase Storage Buckets & Access Policies
-- Architectural Role: Provisions object storage buckets for badge artwork,
-- athlete avatar uploads, and client APK binaries with strict RLS policies.
-- ====================================================================

-- --------------------------------------------------------------------
-- 1. Provision Storage Buckets
-- --------------------------------------------------------------------

-- Bucket: badge-artwork (Vector SVGs and PNG badges from Badge Studio)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'badge-artwork',
    'badge-artwork',
    TRUE,
    5242880, -- 5 MB max
    ARRAY['image/svg+xml', 'image/png', 'image/jpeg', 'image/webp']
)
ON CONFLICT (id) DO UPDATE SET
    public = EXCLUDED.public,
    file_size_limit = EXCLUDED.file_size_limit,
    allowed_mime_types = EXCLUDED.allowed_mime_types;

-- Bucket: athlete-avatars (User profile images)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'athlete-avatars',
    'athlete-avatars',
    TRUE,
    10485760, -- 10 MB max
    ARRAY['image/png', 'image/jpeg', 'image/webp']
)
ON CONFLICT (id) DO UPDATE SET
    public = EXCLUDED.public,
    file_size_limit = EXCLUDED.file_size_limit,
    allowed_mime_types = EXCLUDED.allowed_mime_types;

-- Bucket: app-binaries (Production APK builds and release packages)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'app-binaries',
    'app-binaries',
    TRUE,
    157286400, -- 150 MB max for APK binaries
    ARRAY['application/vnd.android.package-archive', 'application/zip', 'application/octet-stream']
)
ON CONFLICT (id) DO UPDATE SET
    public = EXCLUDED.public,
    file_size_limit = EXCLUDED.file_size_limit,
    allowed_mime_types = EXCLUDED.allowed_mime_types;

-- --------------------------------------------------------------------
-- 2. Storage RLS Policies: Badge Artwork
-- --------------------------------------------------------------------
-- Anyone can view badge artwork
CREATE POLICY "Public Read for Badge Artwork"
ON storage.objects FOR SELECT
USING (bucket_id = 'badge-artwork');

-- Only admins and coaches can upload new badge artwork
CREATE POLICY "Admins and Coaches can upload Badge Artwork"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'badge-artwork' AND
    (
        EXISTS (
            SELECT 1 FROM public.athletes
            WHERE id = auth.uid() AND role IN ('ADMIN', 'SUPER_ADMIN', 'COACH')
        )
    )
);

-- Only admins can modify or delete badge artwork
CREATE POLICY "Admins can modify Badge Artwork"
ON storage.objects FOR UPDATE
USING (
    bucket_id = 'badge-artwork' AND
    (
        EXISTS (
            SELECT 1 FROM public.athletes
            WHERE id = auth.uid() AND role IN ('ADMIN', 'SUPER_ADMIN')
        )
    )
);

CREATE POLICY "Admins can delete Badge Artwork"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'badge-artwork' AND
    (
        EXISTS (
            SELECT 1 FROM public.athletes
            WHERE id = auth.uid() AND role IN ('ADMIN', 'SUPER_ADMIN')
        )
    )
);

-- --------------------------------------------------------------------
-- 3. Storage RLS Policies: Athlete Avatars
-- --------------------------------------------------------------------
-- Anyone can view athlete avatars for community profiles and leaderboards
CREATE POLICY "Public Read for Athlete Avatars"
ON storage.objects FOR SELECT
USING (bucket_id = 'athlete-avatars');

-- Users can upload/update only their own avatar (folder named after auth.uid())
CREATE POLICY "Athletes can upload own avatar"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'athlete-avatars' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] = auth.uid()::text
);

CREATE POLICY "Athletes can update own avatar"
ON storage.objects FOR UPDATE
USING (
    bucket_id = 'athlete-avatars' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] = auth.uid()::text
);

CREATE POLICY "Athletes or Admins can delete avatar"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'athlete-avatars' AND
    (
        (storage.foldername(name))[1] = auth.uid()::text OR
        EXISTS (
            SELECT 1 FROM public.athletes
            WHERE id = auth.uid() AND role IN ('ADMIN', 'SUPER_ADMIN')
        )
    )
);

-- --------------------------------------------------------------------
-- 4. Storage RLS Policies: App Binaries (APKs)
-- --------------------------------------------------------------------
-- Anyone can download APK binaries
CREATE POLICY "Public Read for App Binaries"
ON storage.objects FOR SELECT
USING (bucket_id = 'app-binaries');

-- Only Super Admins can upload or delete APK binaries
CREATE POLICY "Super Admins can upload App Binaries"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'app-binaries' AND
    (
        EXISTS (
            SELECT 1 FROM public.athletes
            WHERE id = auth.uid() AND role = 'SUPER_ADMIN'
        )
    )
);

CREATE POLICY "Super Admins can delete App Binaries"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'app-binaries' AND
    (
        EXISTS (
            SELECT 1 FROM public.athletes
            WHERE id = auth.uid() AND role = 'SUPER_ADMIN'
        )
    )
);
