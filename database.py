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
                new_rating varchar(32)
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

    # ADDS
    async def add_user(self, discord_id, user_id, username, rank, sr, playstyle, comparisons):
        self.cursor.execute(
            "INSERT INTO users VALUES(?,?,?,?,?,?,?)",
            (discord_id, user_id, username, rank, sr, playstyle, comparisons)
        )
        self.db.commit()

    # UPDATES
    async def update_user(self, discord_id, user_id, username, rank, sr, playstyle, comparisons):
        self.cursor.execute(
            "UPDATE users SET osu_id=? AND osu_username=? AND rank=? AND difficulty=? AND playstyle=? AND comparisons=? WHERE discord_id=?",
            (user_id, username, rank, sr, playstyle, comparisons, discord_id)
        )
        self.db.commit()
    # DELETES



