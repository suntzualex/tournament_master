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
    connection = connect()
    print(connection)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM match');
    connection.commit()
    connection.close()



def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE from player")
    connection.commit()
    connection.close();


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(id) FROM player")
    row = cursor.fetchone();
    number_of_players = row[0]
    connection.close()
    return number_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO player (name) VALUES (%s)",(name,))
    connection.commit()
    connection.close()


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
    player_list = []
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select p.id, p.name, count(m.match_id) as wins, (select count(*) from match where p.id = winner or p.id = loser) as matches\
     from player p left join match m on p.id = m.winner group by p.id order by wins desc")
    rows = cursor.fetchall()
    for row in rows:
        player_list.append((row[0],row[1],row[2],row[3]))
    connection.close()
    return player_list
    connection.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    # There is a winner and a loser in my case two inserts in player_results
    cursor.execute("INSERT INTO match (winner, loser) VALUES(%s,%s)", (winner, loser))
    connection.commit()
    connection.close()


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
    # list of players ordered by wins (id, name, wins, matches).
    player_standings = playerStandings()
    # each player should play an equal player in standing.
    # create pairs
    swiss_pairings = []
    for index in range (0,len(player_standings)-1, 2):
        # per 2 players in the list
        player1 = player_standings[index]
        player2 = player_standings[index+1]
        swiss_pairings.append((player1[0], player1[1], player2[0], player2[1]))
    return swiss_pairings
