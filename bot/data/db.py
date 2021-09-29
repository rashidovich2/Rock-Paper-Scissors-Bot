# - *- coding: utf- 8 - *-

import sqlite3

from data import settings


def ensure_connection(func):
    def decorator(*args, **kwargs):
        with sqlite3.connect("database.db") as conn:
            result = func(conn, *args, **kwargs)
        return result
    return decorator


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute("DROP TABLE IF EXISTS users")
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id              INTEGER PRIMARY KEY,
        first_name                   STRING,
        last_name                    STRING,
        user_id                     INTEGER,
        wins              INTEGER DEFAULT 0,
        all_games         INTEGER DEFAULT 0,
        date                        STRING);
    """)
    c.execute("""CREATE TABLE IF NOT EXISTS games (
        id              INTEGER PRIMARY KEY,
        player_move                  STRING,
        player_name                  STRING,
        user_id                    INTEGER);
    """)
    conn.commit()


@ensure_connection
def add_user(conn, first_name: str, last_name: str, date: str, user_id):
    c = conn.cursor()
    c.execute("INSERT INTO users (first_name, last_name, date, user_id) VALUES (?, ?, ?, ?)",
              (first_name, last_name, date, user_id))
    conn.commit()


@ensure_connection
def add_game(conn, player_move: str, player_name: str, user_id):
    c = conn.cursor()
    c.execute("INSERT INTO games (player_move, player_name, user_id) VALUES (?, ?, ?)",
              (player_move, player_name, user_id))
    conn.commit()


@ensure_connection
def delete_game(conn, id):
    c = conn.cursor()
    c.execute("DELETE FROM games WHERE id = ?", (id,))
    conn.commit()


@ensure_connection
def return_game_number(conn):
    c = conn.cursor()
    c.execute("SELECT id FROM games")
    all_results = c.fetchone()
    return all_results[-1]


@ensure_connection
def return_info_game(conn, id):
    c = conn.cursor()
    c.execute("SELECT * FROM games WHERE id = ?", (id,))
    all_results = c.fetchall()
    if str(all_results) == "[]":
        return None
    else:
        return all_results[0]


@ensure_connection
def return_user_wins(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT wins FROM users WHERE user_id = ?", (user_id,))
    wins = c.fetchone()
    wins = int(wins[0]) + 1
    return wins


@ensure_connection
def return_user_wins_2(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT wins FROM users WHERE user_id = ?", (user_id,))
    wins = c.fetchone()
    return wins[0]


@ensure_connection
def return_user_games(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT all_games FROM users WHERE user_id = ?", (user_id,))
    all_games = c.fetchone()
    all_games = int(all_games[0]) + 1
    return all_games


@ensure_connection
def return_user_games_2(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT all_games FROM users WHERE user_id = ?", (user_id,))
    all_games = c.fetchone()
    return all_games[0]


@ensure_connection
def update_user_stat_victory(conn, user_id, wins, all_games):
    c = conn.cursor()
    c.execute('UPDATE users SET wins = ? WHERE user_id = ?', (wins, user_id,))
    c.execute('UPDATE users SET all_games = ? WHERE user_id = ?',
              (all_games, user_id,))
    conn.commit()


@ensure_connection
def update_user_stat_loss(conn, user_id, all_games):
    c = conn.cursor()
    c.execute('UPDATE users SET all_games = ? WHERE user_id = ?',
              (all_games, user_id,))
    conn.commit()
