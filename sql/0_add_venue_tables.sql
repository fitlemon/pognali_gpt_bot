CREATE TABLE public.cities (
	id int8 NULL,
	"name" varchar NULL,
	slug varchar NULL,
	sorting varchar NULL,
	created_at timestamp NULL,
	updated_at timestamp NULL,
	title varchar NULL,
	description varchar NULL,
	"sort" int8 NULL,
	unisender_enabled boolean NULL,
	unisender_list_id int4 NULL,
	CONSTRAINT cities_pk PRIMARY KEY (id)
);

CREATE TABLE public.venue_types (
	id int8 NULL,
	"name" varchar NULL,
	slug varchar NULL,
	created_at timestamp NULL,
	updated_at timestamp NULL,
	CONSTRAINT venue_types_pk PRIMARY KEY (id)
);

CREATE TABLE public.event_types (
	id int8 NULL,
	"name" varchar NULL,
	slug varchar NULL,
	created_at timestamp NULL,
	updated_at timestamp null,
	CONSTRAINT event_types_pk PRIMARY KEY (id)
);

CREATE TABLE public.venues (
	id int8 NULL,
	venue_type_id int4 NULL,
	city_id int4 NULL,
	title varchar NULL,
	slug varchar NULL,
	description varchar NULL,
	address varchar NULL,
	lat int4 NULL,
	lng int4 NULL,
	"open" boolean NULL,
	deleted_at timestamp NULL,
	created_at timestamp NULL,
	updated_at timestamp NULL,
	website varchar NULL,
	"views" int8 NULL,
	seo_title varchar NULL,
	seo_description varchar NULL,
	phone varchar NULL,
	metro varchar NULL,
	open_time varchar NULL,
	user_id varchar NULL,
	CONSTRAINT venues_pk PRIMARY KEY (id),
	CONSTRAINT fk_venues_venue_type FOREIGN KEY (venue_type_id) REFERENCES public.venue_types(id),
	CONSTRAINT fk_venues_cities FOREIGN KEY (city_id) REFERENCES public.cities(id)
);

CREATE TABLE public.events (
	id int8 NOT NULL,
	title varchar NULL,
	slug varchar NULL,
	start_date date NULL,
	end_date date NULL,
	start_time time NULL,
	end_time time NULL,
	description varchar NULL,
	price_from int4 NULL,
	price_gate varchar NULL,
	city_id int4 NULL,
	venue_id int4 NULL,
	event_type_id int4 NULL,
	tickets_url varchar NULL,
	info_url varchar NULL,
	is_cancelled boolean NULL,
	is_featured boolean NULL,
	deleted_at timestamp NULL,
	user_id int4 NULL,
	created_at timestamp NULL,
	updated_at timestamp NULL,
	ticketscloud_event_id int8 NULL,
	ticketscloud_event_token varchar NULL,
	ticketscloud_event_multi varchar NULL,
	age_limit int4 NULL,
	"views" int8 NULL,
	CONSTRAINT events_pk PRIMARY KEY (id),
	CONSTRAINT fk_events_cities FOREIGN KEY (city_id) REFERENCES public.cities(id),
	CONSTRAINT fk_events_venues FOREIGN KEY (venue_id) REFERENCES public.venues(id),
	CONSTRAINT fk_events_event_types FOREIGN KEY (event_type_id) REFERENCES public.event_types(id)
);
