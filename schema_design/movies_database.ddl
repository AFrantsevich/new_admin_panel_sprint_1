
CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL CONSTRAINT genre_name_unique UNIQUE,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    file_path TEXT, 
    description TEXT,
    creation_date DATE,
    rating FLOAT CHECK (rating BETWEEN 0 AND 100),
    type TEXT NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL REFERENCES content.genre ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work ON DELETE CASCADE,
    created_at timestamp with time zone,
    CONSTRAINT unique_film_genre UNIQUE(genre_id, film_work_id)
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL CONSTRAINT person_full_name_unique UNIQUE,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TYPE content.role_type AS ENUM 
    ('actor', 'director', 'writer'); 

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL REFERENCES content.person ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work ON DELETE CASCADE,
    role content.role_type NOT NULL,
    created_at timestamp with time zone
);

CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);

CREATE INDEX genre_film_work_idx ON content.genre_film_work(genre_id, film_work_id);

CREATE UNIQUE INDEX film_work_person_role_idx ON content.person_film_work (film_work_id, person_id, role);

