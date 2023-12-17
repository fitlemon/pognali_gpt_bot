DROP DATABASE pognali_gpt_bot;
CREATE DATABASE pognali_gpt_bot WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru_RU.UTF-8';

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying,
    user_firstname character varying,
    user_surname character varying,
    age integer,
    sex boolean,
    user_city character varying,
    last_question character varying,
    misc_data jsonb
);

ALTER TABLE public.users ADD CONSTRAINT users_pk PRIMARY KEY (user_id);
