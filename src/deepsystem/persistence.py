import sqlite3
from config import config
from langgraph.checkpoint.sqlite import SqliteSaver

def create_checkpointer():
    conn = sqlite3.connect(config.database_path, check_same_thread=False)
    return SqliteSaver(conn)