import configparser
import psycopg2
from psycopg2 import Error


class DatabaseUtils:
    __conn = None

    @classmethod
    def __init_conn(cls):
        if cls.__conn is not None:
            return

        config = configparser.ConfigParser()
        config.read('database.ini')

        database = config['postgresql']['database']
        user = config['postgresql']['user']
        password = config['postgresql']['password']
        host = config['postgresql']['host']
        port = config['postgresql']['port']

        try:
            cls.__conn = psycopg2.connect(
                database=database,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Connected to PostgreSQL successfully")
        except Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            cls.__conn = None

    @staticmethod
    def close_connection(cls):
        if cls.__conn is not None:
            cls.__conn.close()
            cls.__conn = None
            print("PostgreSQL connection is closed")

    @staticmethod
    def execute_query(cls, query):
        if cls.__conn is None:
            raise Exception("Database connection is not initialized")

        with cls.__conn.cursor() as cursor:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                return results
            except Error as e:
                print(f"Error executing query: {e}")
                return None

    @staticmethod
    def execute_command(cls, command):
        if cls.__conn is None:
            raise Exception("Database connection is not initialized")

        with cls.__conn.cursor() as cursor:
            try:
                cursor.execute(command)
                cls.__conn.commit()
                return True
            except Error as e:
                print(f"Error executing command: {e}")
                cls.__conn.rollback()
                return False

            # 使用示例


if __name__ == "__main__":
    # 初始化数据库连接（如果需要的话）
    LM = DatabaseUtils()

    # 示例查询操作
    query = "SELECT * FROM your_table"
    results = LM.execute_query(query)
    for row in results:
        print(row)

        # 示例写入操作
    command = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
    data = ('value1', 'value2')
    success = LM.execute_command(command, data)
    if success:
        print("Command executed successfully")

        # 关闭数据库连接（如果需要的话）
    LM.close_connection()