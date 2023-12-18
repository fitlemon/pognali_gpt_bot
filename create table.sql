DROP DATABASE pognali_gpt_bot;
CREATE DATABASE pognali_gpt_bot WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru_RU.UTF-8';

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying,
    user_firstname character varying,
    user_surname character varying,
    age integer,
    sex character varying,
    user_city character varying,
    main_music_genres VARCHAR[],
    techno_music_genres VARCHAR[],
    favorite_techno_music_artists VARCHAR[],
    favorite_night_clubs VARCHAR[],
    favorite_bars VARCHAR[],
    current_location_address character varying,
    current_location_coordinates point,
    last_question character varying

);

ALTER TABLE public.users ADD CONSTRAINT users_pk PRIMARY KEY (user_id);
