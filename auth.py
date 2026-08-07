import sqlite3
import bcrypt

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password BLOB
)
""")

conn.commit()

def register_user(username, password):

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:
        c.execute(
            "INSERT INTO users VALUES (?, ?)",
            (username, hashed)
        )

        conn.commit()
        return True

    except:
        return False

def login_user(username, password):

    c.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    data = c.fetchone()

    if data:

        if bcrypt.checkpw(
            password.encode(),
            data[0]
        ):
            return True

    return False