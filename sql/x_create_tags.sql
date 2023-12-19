CREATE TABLE public.tags (
	id int8 NULL,
	"name" varchar NULL,
	slug varchar NULL,
	type varchar NULL,
	created_at timestamp NULL,
	updated_at timestamp NULL,
	CONSTRAINT tags_pk PRIMARY KEY (id)
);