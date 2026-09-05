-- ============================================================
-- CropGuard AI: Row Level Security (RLS) Policies
-- Ensures strict user-level data isolation:
-- Farmers can only access their OWN prediction history, chat logs, and profile.
-- Public crop knowledge remains readable by all users.
-- ============================================================

-- 1. Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prediction_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crop_knowledge ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 2. Profiles Table Policies
-- ============================================================
-- Allow individual users to view only their own profile
CREATE POLICY "Users can view own profile"
    ON public.profiles
    FOR SELECT
    USING (auth.uid() = id);

-- Allow individual users to update only their own profile
CREATE POLICY "Users can update own profile"
    ON public.profiles
    FOR UPDATE
    USING (auth.uid() = id);

-- Allow authenticated users to insert their profile upon registration
CREATE POLICY "Users can insert own profile"
    ON public.profiles
    FOR INSERT
    WITH CHECK (auth.uid() = id);

-- ============================================================
-- 3. Prediction History Policies
-- ============================================================
-- Farmers can view ONLY their own prediction records
CREATE POLICY "Users can view own prediction history"
    ON public.prediction_history
    FOR SELECT
    USING (auth.uid() = user_id);

-- Farmers can insert new predictions associated with their UID
CREATE POLICY "Users can insert own predictions"
    ON public.prediction_history
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Farmers can delete only their own prediction records
CREATE POLICY "Users can delete own predictions"
    ON public.prediction_history
    FOR DELETE
    USING (auth.uid() = user_id);

-- ============================================================
-- 4. Chat History Policies
-- ============================================================
-- Farmers can view only their own conversation messages
CREATE POLICY "Users can view own chat history"
    ON public.chat_history
    FOR SELECT
    USING (auth.uid() = user_id);

-- Farmers can insert messages under their UID
CREATE POLICY "Users can insert own chat messages"
    ON public.chat_history
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- ============================================================
-- 5. Crop Knowledge Policies (Public Agricultural Reference)
-- ============================================================
-- Anyone (authenticated or anonymous) can view agronomic envelopes
CREATE POLICY "Public read access for crop knowledge"
    ON public.crop_knowledge
    FOR SELECT
    USING (true);

-- Only service role can modify crop knowledge (restricted from client)
CREATE POLICY "Service role can manage crop knowledge"
    ON public.crop_knowledge
    FOR ALL
    USING (auth.jwt() ->> 'role' = 'service_role');
