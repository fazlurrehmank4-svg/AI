-- ============================================================
-- CropGuard AI: Supabase PostgreSQL Database Schema
-- Project URL: https://tspdpkyhszrebrclsefz.supabase.co
-- ============================================================

-- Enable UUID extension if not already active
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Profiles Table (Linked to Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    full_name TEXT,
    farm_location TEXT,
    primary_crops TEXT[] DEFAULT ARRAY['Wheat', 'Rice'],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Prediction History Table (Stores full ML & reasoning inference logs)
CREATE TABLE IF NOT EXISTS public.prediction_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    crop TEXT NOT NULL,
    location TEXT NOT NULL,
    weather JSONB NOT NULL,
    crop_health_score NUMERIC(5, 2) NOT NULL,
    health_status TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    primary_risk_factor TEXT,
    causes JSONB DEFAULT '[]'::jsonb,
    precautions JSONB DEFAULT '[]'::jsonb,
    ai_explanation TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Chat History Table (Stores farmer queries and local AI replies)
CREATE TABLE IF NOT EXISTS public.chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    crop TEXT,
    confidence NUMERIC(4, 2),
    matched_topic TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Crop Knowledge Table (Public domain agronomic reference data)
CREATE TABLE IF NOT EXISTS public.crop_knowledge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop TEXT UNIQUE NOT NULL,
    temp_optimal JSONB NOT NULL,       -- e.g. [15.0, 25.0]
    humidity_optimal JSONB NOT NULL,   -- e.g. [50.0, 70.0]
    rainfall_optimal JSONB NOT NULL,   -- e.g. [50.0, 100.0]
    soil_type TEXT NOT NULL,
    water_requirement TEXT NOT NULL,
    diseases JSONB DEFAULT '[]'::jsonb,
    precautions JSONB DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. Learned Knowledge Table (Stores continuous self-learning phrases & feedback permanently)
CREATE TABLE IF NOT EXISTS public.learned_knowledge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic TEXT NOT NULL,
    crop TEXT DEFAULT 'General',
    language TEXT DEFAULT 'en',
    query_templates JSONB DEFAULT '[]'::jsonb,
    answer_en TEXT,
    answer_hi TEXT,
    answer_ur TEXT,
    sample_count INTEGER DEFAULT 1,
    learned_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Indexes for high-performance querying
CREATE INDEX IF NOT EXISTS idx_prediction_user_date ON public.prediction_history (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chat_user_date ON public.chat_history (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_crop_knowledge_name ON public.crop_knowledge (crop);
CREATE INDEX IF NOT EXISTS idx_learned_knowledge_topic ON public.learned_knowledge (topic);
