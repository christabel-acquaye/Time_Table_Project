import MySQLdb
from _mysql_exceptions import Error


def connect(func):
    def connect_db(**kwargs):
        time_table_db_conn = None
        results = None
        try:
            time_table_db_conn = MySQLdb.connect(
                host="localhost",
                user="root",
                passwd="jellybean",
                db="ttdb"
            )

            cursor = time_table_db_conn.cursor()
            results = func(cur=cursor, **kwargs)
            time_table_db_conn.commit()
            cursor.close()
        except Error as e:
            # time_table_db_conn.rollback()
            print('e', e)

        finally:
            time_table_db_conn.close()

        return results

    return connect_db


