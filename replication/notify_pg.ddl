CREATE SCHEMA IF NOT EXISTS notify;

CREATE TABLE IF NOT EXISTS notify.users (
    id uuid PRIMARY KEY,
    username character varying(80) NOT NULL UNIQUE,
    email character varying(120) NOT NULL UNIQUE,
    created_at timestamp with time zone,
    modified_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS notify.users_info (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL UNIQUE,
    first_name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    timezone text,
    created_at timestamp with time zone,
    modified_at timestamp with time zone
);

CREATE UNIQUE INDEX users_info_user_id_first_name_last_name_idx ON notify.users_info USING btree (user_id, first_name, last_name);
