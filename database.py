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
                elo_target varchar(32),
                playstyle varchar(32),
                comparisons varchar(32),
                confirmation varchar(16),
                password varchar(16),
                beatmap_order varchar(16)
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
                title varchar(32),
                difficulty_name varchar(32),
                url varchar(32)
            )
        ''') # Specific beatmap 

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache(
                discord_id varchar(32) not null,
                message_id varchar(32),
                beatmap_0 varchar(32),
                beatmap_1 varchar(32),
                beatmap_2 varchar(32),
                beatmap_3 varchar(32),
                beatmap_4 varchar(32),
                beatmap_5 varchar(32),
                beatmap_6 varchar(32),
                beatmap_7 varchar(32),
                beatmap_8 varchar(32),
                beatmap_9 varchar(32)
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

    async def get_user_osu_id(self, discord_id):
        return self.cursor.execute(
            "SELECT osu_id FROM users WHERE discord_id=?",
            (discord_id,)
        ).fetchone()

    async def get_all_comparisons(self):
        return self.cursor.execute(
            "SELECT * FROM comparisons"
        ).fetchall()

    async def get_user_comparison(self, user_id, beatmap1, beatmap2):
        return self.cursor.execute(
            "SELECT * FROM comparisons WHERE osu_id=? AND first_beatmap_id=? AND second_beatmap_id=?",
        (user_id, beatmap1, beatmap2)
        ).fetchone()

    async def get_user_comparisons(self, discord_id):
        return self.cursor.execute(
            "SELECT comparisons FROM users WHERE discord_id=?",
            (discord_id,)
        ).fetchone()

    async def get_playstyle(self, user_id):
        return self.cursor.execute(
            "SELECT playstyle FROM users WHERE discord_id=?",
            (user_id,)
        ).fetchone()

    async def get_cache(self, discord_id):
        return self.cursor.execute(
            "SELECT * FROM cache WHERE discord_id=?",
            (discord_id,)
        ).fetchone()

    async def get_elo(self, discord_id):
        return self.cursor.execute(
            "SELECT elo_target FROM users WHERE discord_id=?",
            (discord_id,)
        ).fetchone()

    async def get_beatmap_comparisons(self, beatmap_id):
        return self.cursor.execute(
            "Select comparisons FROM beatmaps WHERE beatmap_id=?",
            (beatmap_id,)
        ).fetchone()

    # ADDS
    async def add_user(self, discord_id, user_id, username, rank, sr, playstyle, comparisons):
        self.cursor.execute(
            "INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?)",
            (discord_id, user_id, username, rank, sr, playstyle, comparisons, "0", "", "")
        )
        self.db.commit()

    async def add_beatmap(self, id, difficulty_rating, bpm, length, artist, title, difficulty_name, url):
        self.cursor.execute(
            "INSERT INTO beatmaps VALUES(?,?,?,?,?,?,?,?,?,?)",
            (id, difficulty_rating, 0, difficulty_rating, bpm, length, artist, title, difficulty_name, url)
        )
        self.db.commit()

    async def add_cache(self, id):
        self.cursor.execute(
            "INSERT INTO cache VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (id, "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0")
        )
        self.db.commit()

    async def add_comparison(self, osu_id, beatmap_1_id, beatmap_2_id, outcome):
        self.cursor.execute(
            "INSERT INTO comparisons VALUES(?,?,?,?)",
            (osu_id, beatmap_1_id, beatmap_2_id, outcome)
        )
        self.db.commit()

    # UPDATES
    async def update_user(self, discord_id, user_id, username, rank, sr, playstyle):
        self.cursor.execute(
            "UPDATE users SET osu_id=?, osu_username=?, rank=?, elo_target=?, playstyle=? WHERE discord_id=?",
            (user_id, username, rank, sr, playstyle, discord_id)
        )
        self.db.commit()

    async def update_playstyle(self, discord_id, playstyle):
        self.cursor.execute(
            "UPDATE users SET playstyle=? WHERE discord_id=?",
            (playstyle, discord_id)
        )
        self.db.commit()

    async def update_SR(self, discord_id, elo):
        self.cursor.execute(
            "UPDATE users SET elo_target=? WHERE discord_id=?",
            (elo, discord_id)
        )
        self.db.commit()

    async def update_cache(self, discord_id, message_id, beatmaps):
        if beatmaps == "":
            self.cursor.execute(
                "UPDATE cache SET message_id=?, beatmap_0=?, beatmap_1=?, beatmap_2=?, beatmap_3=?, beatmap_4=?, beatmap_5=?, beatmap_6=?, beatmap_7=?, beatmap_8=?, beatmap_9=? WHERE discord_id=?",
                (message_id, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', discord_id)
            )
            self.db.commit()
        else:
            b0 = beatmaps[0][0]
            b1 = beatmaps[1][0]
            b2 = beatmaps[2][0]
            b3 = beatmaps[3][0]
            b4 = beatmaps[4][0]
            b5 = beatmaps[5][0]
            b6 = beatmaps[6][0]
            b7 = beatmaps[7][0]
            b8 = beatmaps[8][0]
            b9 = beatmaps[9][0]

            self.cursor.execute(
                "UPDATE cache SET message_id=?, beatmap_0=?, beatmap_1=?, beatmap_2=?, beatmap_3=?, beatmap_4=?, beatmap_5=?, beatmap_6=?, beatmap_7=?, beatmap_8=?, beatmap_9=? WHERE discord_id=?",
                (message_id, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, discord_id)
            )
            self.db.commit()

    async def update_comparisons(self, beatmap_id, comparisons):
        self.cursor.execute(
            "UPDATE beatmaps SET comparisons=? WHERE beatmap_id=?",
            (comparisons, beatmap_id)
        )
        self.db.commit()

    async def update_user_comparisons(self, discord_id, comparisons):
        self.cursor.execute(
            "UPDATE users SET comparisons=? WHERE discord_id=?",
            (comparisons, discord_id)
        )
        self.db.commit()

    async def start_confirmation(self, discord_id):
        self.cursor.execute(
            "UPDATE users SET confirmation=? WHERE discord_id=?",
            ("1", discord_id)
        )
        self.db.commit()

    async def update_password(self, discord_id, password):
        self.cursor.execute(
            "UPDATE users SET password=? WHERE discord_id=?",
            (password, discord_id)
        )
        self.db.commit()

    async def update_order(self, discord_id, order):
        self.cursor.execute(
            "UPDATE users SET beatmap_order=? WHERE discord_id=?",
            (order, discord_id)
        )
        self.db.commit()

    # DELETES



