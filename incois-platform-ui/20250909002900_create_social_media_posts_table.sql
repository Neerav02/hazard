-- Table to store data ingested and processed by the NLP microservice
CREATE TABLE "public".social_media_posts (
    id BIGSERIAL PRIMARY KEY,
    source_id TEXT UNIQUE NOT NULL, -- The original ID from the social media platform
    source_platform TEXT NOT NULL,
    author TEXT,
    raw_text TEXT NOT NULL,
    posted_at TIMESTAMPTZ,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Columns to be populated by the NLP service
    sentiment TEXT,
    sentiment_score REAL,
    topic TEXT,
    topic_score REAL
);