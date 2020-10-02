CREATE TABLE tasks (
    id SERIAL, skill varchar(20),
    arguments json,
    attempts smallint,
    worker_type varchar(20),
    state varchar(30)
);
--CREATE TABLE results (id SERIAL, task_id int, skill varchar(20), result json, executed_state varchar(20));
--CREATE TABLE games (id SERIAL, datetime timestamp, tournament text, left_command text, right_command text);