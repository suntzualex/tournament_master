-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use views.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- if there are tables drop them if there are databases empty them and drop them
-- first close all connections to it.
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament'
  AND pid <> pg_backend_pid();

DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS player;
DROP DATABASE IF EXISTS tournament;

-- create database
CREATE DATABASE tournament;

-- connect to that database
\connect tournament

-- table player has an id and a name.
CREATE TABLE player(
  id serial PRIMARY KEY,
  name VARCHAR NOT NULL
);

-- table match has match_id, a winner and a loser.
CREATE TABLE match(
  match_id serial PRIMARY KEY,
  winner integer NOT NULL,
  loser integer NOT NULL,
  FOREIGN KEY (winner) REFERENCES player(id),
  FOREIGN KEY (loser) REFERENCES player(id)
);
