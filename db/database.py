from os.path import isfile
from sqlite3 import connect

DB_PATH = "./db/bot_db.db"
BUILD_PATH = "./db/build.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


def commit():
    cxn.commit()


def close():
    cxn.close()


def field(command, *values):
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchone()


def records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()


def column(command, *values):
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    cur.execute(command, tuple(values))


def multiexec(command, *values):
    cur.executemany(command, tuple(values))


def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())


@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)


def get_user_by_id(user_id):
    cur.execute("SELECT * FROM users WHERE UserID=?", user_id)

    return cur.fetchone()


def save_user(user_id, user_name):
    cur.execute("INSERT INTO users(UserID,UserName) VALUES (?,?)", (user_id, user_name))
    commit()

    return 1


def update_user(user_id, user_name):
    cur.execute("UPDATE users SET UserID=? UserName=? WHERE UserID=?", (user_id, user_name, user_id))
    commit()

    return 1


def delete_user(user_id):
    cur.execute("DELETE FROM users WHERE UserID=?", user_id)
    commit()

    return 1


def create_table_queue(qname):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS ? (QueueID integer PRIMARY KEY AUTOINCREMENT,QueueName VARCHAR, FK_UserID INTEGER "
        "FOREIGN KEY (FK_UserID) REFERENCES users (UserID) ON UPDATE CASCADE ON DELETE CASCADE",
        qname)
    commit()

    return 1


def join_queue(qname, user_id):
    cur.execute("INSERT INTO ? (QueueName,UserName) VALUES (?,?)", (qname, user_id))
    commit()

    return 1


def delete_fromq(qname, user_id):
    cur.execute("DELETE FROM ? WHERE FK_UserID=?", (qname, user_id))
    commit()

    return 1


def delete_queue(qname):
    if qname != "users":
        cur.execute("DROP TABLE ?", qname)
        commit()

    return 1
