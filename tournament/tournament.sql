-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;
CREATE TABLE players (name TEXT,
                      id SERIAL PRIMARY KEY);
CREATE TABLE matches (winner INTEGER REFERENCES players (id),
                      looser INTEGER REFERENCES players (id),
                      id SERIAL PRIMARY KEY);
-- VIEWS
CREATE VIEW matches_view AS
  SELECT P.id as ID, COUNT(M) AS match_count
  FROM players as P LEFT JOIN matches as M
  ON (P.id = M.winner) OR (P.id = M.looser)
  GROUP BY P.id
  ORDER BY match_count DESC;    
  
CREATE VIEW wins AS
  SELECT P.id as ID, COUNT(M.winner) AS WINS
  FROM players as P LEFT JOIN matches as M
  ON P.id = M.winner
  GROUP BY P.id
  ORDER BY WINS DESC;
  
CREATE VIEW looses AS
  SELECT P.id as ID, COUNT(M.looser) AS LOOSES
  FROM players as P LEFT JOIN matches as M
  ON P.id = M.looser
  GROUP BY P.id
  ORDER BY LOOSES DESC;
                    
