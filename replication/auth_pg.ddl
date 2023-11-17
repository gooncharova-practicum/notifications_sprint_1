CREATE SCHEMA IF NOT EXISTS auth;

CREATE TABLE IF NOT EXISTS auth.users (
    id uuid PRIMARY KEY,
    username character varying(80) NOT NULL UNIQUE,
    email character varying(120) NOT NULL UNIQUE,
    password_hash text NOT NULL,
    role_id uuid NOT NULL,
    created_at timestamp with time zone,
    modified_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS auth.users_info (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES auth.users (id) ON DELETE CASCADE UNIQUE,
    first_name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    timezone text,
    created_at timestamp with time zone,
    modified_at timestamp with time zone
);

CREATE UNIQUE INDEX users_role_id_email_username_idx ON auth.users USING btree (role_id, email, username);
CREATE UNIQUE INDEX users_info_user_id_fist_name_last_name_idx ON auth.users_info USING btree (user_id, first_name, last_name);
