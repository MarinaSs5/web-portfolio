import os, sqlite3, multiprocessing
from . import shared, user, project





def start():
    shared.connection = sqlite3.connect(os.path.join(os.getcwd(), 'internal', 'database', 'database.sqlite'), check_same_thread = False)
    shared.synchronization = multiprocessing.Lock()
    shared.cursor = shared.connection.cursor()

def save():
    with shared.synchronization:
        shared.connection.commit()