-- 1. Create a new role (user) with a secure password.
-- Replace 'a_very_strong_and_secret_password' with a password you generate.
CREATE ROLE nlp_service_worker WITH LOGIN PASSWORD 'a_very_strong_and_secret_password';

-- 2. Grant the role permission to connect to the database.
GRANT CONNECT ON DATABASE postgres TO nlp_service_worker;

-- 3. Grant the role permission to use the 'public' schema.
-- This allows the role to see the tables inside it.
GRANT USAGE ON SCHEMA public TO nlp_service_worker;

-- 4. Grant specific permissions ONLY on the target table.
-- This allows the service to read, write, and update posts.
GRANT INSERT, SELECT, UPDATE ON TABLE public.social_media_posts TO nlp_service_worker;

-- 5. Grant permission to use the table's ID sequence.
-- This is required to let the database auto-generate the 'id' for new rows.
GRANT USAGE, SELECT ON SEQUENCE public.social_media_posts_id_seq TO nlp_service_worker;