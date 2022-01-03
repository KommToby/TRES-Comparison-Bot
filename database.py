import sqlite3

class Database:
    def __init__(self):
        self.db = sqlite3.connect('database.db')
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                discord_id varchar(32) not null,
                osu_id varchar(32),
                osu_username varchar(32),
                rank varchar(32),
                difficulty varchar(32),
                playstyle varchar(32),
                comparisons varchar(32)
            )
        ''')  ## Storing user data

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comparisons(
                osu_id varchar(32) not null,
                first_beatmap_id varchar(32),
                second_beatmap_id varchar(32),
                outcome varchar(16)
            )
        ''')  # Storing comparison results after user has decided

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS beatmaps(
                beatmap_id varchar(32) not null,
                difficulty_rating varchar(32),
                comparisons varchar(32),
                new_rating varchar(32),
                bpm varchar(32),
                length varchar(32),
                artist varchar(32),
                artist varchar(32),
                title varchar(32),
                difficulty_name varchar(32),
                url varchar(32)
            )
        ''') # Specific beatmap 

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache(
                discord_id varchar(32) not null,
                message_id varchar(32),
                first_beatmap_id varchar(32),
                second_beatmap_id varchar(32)
            )
        ''') # Storing the comparison the user has been given so it doesnt have to always listen for a response

    # GETS
    async def get_beatmap(self, id):
        return self.cursor.execute(
            "SELECT * FROM beatmaps WHERE beatmap_id=?",
            (id,)
        ).fetchone()

    async def get_all_beatmaps(self):
        return self.cursor.execute(
            "SELECT * FROM beatmaps"
        ).fetchall()       

    async def get_user(self, id):
        return self.cursor.execute(
            "SELECT * FROM users WHERE discord_id=?",
            (id,)
        ).fetchone()

    async def get_user_comparison(self, user_id, beatmap1, beatmap2):
        return self.cursor.execute(
            "SELECT * FROM comparisons WHERE osu_id=? AND first_beatmap_id=? AND second_beatmap_id=?",
        (user_id, beatmap1, beatmap2)
        ).fetchone()

    async def get_playstyle(self, user_id):
        return self.cursor.execute(
            "SELECT playstyle FROM users WHERE discord_id=?",
            (user_id,)
        ).fetchone()

    # ADDS
    async def add_user(self, discord_id, user_id, username, rank, sr, playstyle, comparisons):
        self.cursor.execute(
            "INSERT INTO users VALUES(?,?,?,?,?,?,?)",
            (discord_id, user_id, username, rank, sr, playstyle, comparisons)
        )
        self.db.commit()

    async def add_beatmap(self, id, difficulty_rating, bpm, length, artist, title, difficulty_name, url):
        self.cursor.execute(
            "INSERT INTO beatmaps VALUES(?,?,?,?,?,?,?,?,?,?)",
            (id, difficulty_rating, 0, difficulty_rating, bpm, length, artist, title, difficulty_name, url)
        )
        self.db.commit()

    # UPDATES
    async def update_user(self, discord_id, user_id, username, rank, sr, playstyle):
        self.cursor.execute(
            "UPDATE users SET osu_id=?, osu_username=?, rank=?, difficulty=?, playstyle=? WHERE discord_id=?",
            (user_id, username, rank, sr, playstyle, discord_id)
        )
        self.db.commit()

    async def update_playstyle(self, discord_id, playstyle):
        self.cursor.execute(
            "UPDATE users SET playstyle=? WHERE discord_id=?",
            (playstyle, discord_id)
        )
        self.db.commit()

    # DELETES



