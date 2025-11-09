import pymysql.cursors
import os

class MySQLConnection:
    def __init__(self):
        self.connection = pymysql.connect(
            host=os.getenv("TIDB_HOST"),
            port=int(os.getenv("TIDB_PORT")),
            user=os.getenv("TIDB_USER"),
            password=os.getenv("TIDB_PASSWORD"),
            db=os.getenv("TIDB_DATABASE"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
            ssl={'ca': '/etc/ssl/cert.pem'}
        )
    
    def query_db(self, query: str, data: dict = None):
        """Executes a query and returns results if SELECT."""
        with self.connection.cursor() as cursor:
            try:
                if data:
                    query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query)
                if query.lower().strip().startswith("insert"):
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().strip().startswith("select"):
                    return cursor.fetchall()
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong:", e)
                return False
            finally:
                self.connection.close()

def connect_to_mysql():
    """Factory function to return a MySQLConnection object."""
    return MySQLConnection()