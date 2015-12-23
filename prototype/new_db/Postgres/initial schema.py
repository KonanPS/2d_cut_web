import pcycopg2 

conn = psycopg2.connect("dbname=7times user=pavel")

create_users = """

CREATE TABLE users
(
  id integer NOT NULL,
  user_name text,
  email text,
  password text,
  account_type text,
  session_token text,
  paid_utill timestamp without time zone,
  CONSTRAINT users_pkey PRIMARY KEY (id)
)"""

create_jobs = """
CREATE TABLE jobs
(
  id integer NOT NULL,
  user_id integer,
  request json,
  result json,
  state text,
  processing_time integer,
  created_at time without time zone,
  CONSTRAINT jobs_pkey PRIMARY KEY (id),
  CONSTRAINT user_id FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)"""