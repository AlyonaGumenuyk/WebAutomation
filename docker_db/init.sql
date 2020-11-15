CREATE DATABASE "1xStavkaDB";
\c "1xStavkaDB"
GRANT ALL PRIVILEGES ON DATABASE "1xStavkaDB" to docker;
CREATE TABLE tasks (
    id SERIAL, skill varchar(20),
    arguments json,
    attempts smallint,
    worker_type varchar(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    state varchar(30)
);
CREATE TABLE results (
    id SERIAL, task_id int,
    skill varchar(20),
    result json,
    executed_state varchar(20)
);
CREATE TABLE games (
    id SERIAL,
    datetime timestamp,
    tournament text,
    left_command text,
    right_command text
);

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON todos
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();