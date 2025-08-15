import sqlite3
from config import get_configuration
from langgraph.checkpoint.sqlite import SqliteSaver

config = get_configuration()

def create_checkpointer():
    database_path = config['database']['path']
    conn = sqlite3.connect(database_path, check_same_thread=False)
    return SqliteSaver(conn)