import sqlite3

from os.path import join
from ..exts.config import USER_CONFIG_DIR


__local_database_name__ = join(USER_CONFIG_DIR, 'local_conversation.db')

convs_database = sqlite3.connect(__local_database_name__, check_same_thread=False)
# convs_database_cursor = convs_database.cursor()