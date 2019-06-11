from app import cursor
import json


def get_columns(table):
    column = None
    try:
        cursor.execute("SELECT column_name FROM ALL_TAB_COLUMNS  where TABLE_NAME='"+table+"'")
        column = [row[0] for row in cursor]
    except Exception as e:
        column = str(e)
    return column

def query(query):
    try:
        cursor.execute(query)
    except Exception as e:
        return str(e)
    else:
        return cursor



