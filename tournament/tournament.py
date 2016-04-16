#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")


def deleteMatches():
	"""Remove all the match records from the database."""
	conn = connect()
	C = conn.cursor()
	C.execute("DELETE FROM matches")
	conn.commit()
	conn.close()


def deletePlayers():
	"""Remove all the player records from the database."""
	conn = connect()
	C = conn.cursor()
	C.execute("DELETE FROM players")
	conn.commit()
	conn.close()


def countPlayers():
	"""Returns the number of players currently registered."""
	conn = connect()
	C = conn.cursor()
	C.execute("SELECT COUNT(*) AS num FROM players")
	Row = C.fetchone()
	if Row:
	  Count = int(Row[0])
	conn.close()
	return Count


def registerPlayer(name):
	"""Adds a player to the tournament database.
  
	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)
  
	Args:
	  name: the player's full name (need not be unique).
	"""
	conn = connect()
	C = conn.cursor()
	C.execute("INSERT INTO players(name) VALUES(%s)", (name,))
	conn.commit()
	conn.close()


def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.

	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.

	Returns:
	  A list of tuples, each of which contains (id, name, wins, matches):
		id: the player's unique id (assigned by the database)
		name: the player's full name (as registered)
		wins: the number of matches the player has won
		matches: the number of matches the player has played
	"""
	conn = connect()
	C = conn.cursor()
	Query = """ 
			SELECT P.id, P.name, W.WINS, matches_view.match_count
			FROM players as P LEFT JOIN wins as W 
			ON P.id = W.ID
			LEFT JOIN matches_view ON P.id = matches_view.ID
			GROUP BY P.id, W.WINS, matches_view.match_count
			ORDER BY W.WINS DESC
			 """
	C.execute(Query)
	standings = C.fetchall()
	conn.close()
	return standings

def reportMatch(Winner, Looser):
	"""Records the outcome of a single match between two players.

	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
	conn = connect()
	C = conn.cursor()
	C.execute("INSERT INTO matches(winner, looser) VALUES(%s, %s)", (int(Winner), int(Looser)))
	conn.commit()
	conn.close()

def swissPairings():
	"""Returns a list of pairs of players for the next round of a match.
  
	Assuming that there are an even number of players registered, each player
	appears exactly once in the pairings.  Each player is paired with another
	player with an equal or nearly-equal win record, that is, a player adjacent
	to him or her in the standings.
  
	Returns:
	  A list of tuples, each of which contains (id1, name1, id2, name2)
		id1: the first player's unique id
		name1: the first player's name
		id2: the second player's unique id
		name2: the second player's name
	"""
	""" 0th position of standings is id
		1st position of standings is name
		match will be in pairs that is why loop has 
		match of i*2-1 and i*2-2 for i has value 1 to total number_of_matches/2
	"""
	standings = playerStandings()
	CountOfMatches = len(standings)/2
	matches_list = list()
	for i in range(1, CountOfMatches+1):
		first = i * 2 - 2
		second = i * 2 - 1
		matches_list.append((standings[first][0], standings[first][1], standings[second][0], standings[second][1]))
	return matches_list


