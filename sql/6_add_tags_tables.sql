CREATE TABLE public.tags (
	id int8 NULL,
	"name" varchar NULL,
	slug varchar NULL,
	name_rus varchar NULL,
	name_rus_lowercase varchar NULL,
	"type" varchar NULL,
	order_column int8 NULL,
	created_at varchar NULL,
	updated_at varchar NULL,
	CONSTRAINT tags_pk PRIMARY KEY (id)
);

CREATE TABLE public.taggable (
	tag_id int8 NULL,
	taggable_type varchar NULL,
	taggable_id int8 NULL,
	CONSTRAINT taggable_pk PRIMARY KEY (tag_id,taggable_type,taggable_id),
	CONSTRAINT fk_taggable_tag FOREIGN KEY (tag_id) REFERENCES public.tags(id)
);
