import pymysql.cursors
from credential import Credential


class Connection(Credential):
    def __init__(self):
        Credential.__init__(self)

    def start(self, host, dbName):
        connection = pymysql.connect(host=host, user=self.get_username(self), password=self.get_password(self),
                                     db=dbName, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        return connection

    @staticmethod
    def get_single_data(conn, attributes, table, condition, condition_vals):
        with conn.cursor() as cursor:
            # generating query
            select_sql = "Select {0} from {1} where {2}".format(",".join(
                attributes), ",".join(table), " and ".join([x+"=%s" for x in condition]))
            cursor.execute(select_sql, tuple(condition_vals))
            result = cursor.fetchone()
            return result

    @staticmethod
    def insert_data(conn, attributes, table, data):
        with conn.cursor() as cursor:
            # generating query
            insert_sql = "INSERT INTO {0} ({1}) VALUES ({2})".format(
                table, ",".join(attributes), ",".join(["%s" for _ in range(len(attributes))]))
            cursor.execute(insert_sql, tuple(data))
            result = cursor.lastrowid
            conn.commit()
            return result

    @staticmethod
    def get_all_data(conn, attributes, table, condition, condition_vals):
        with conn.cursor() as cursor:
            # generating query
            select_sql = "Select {0} from {1} where {2}".format(",".join(
                attributes), ",".join(table), " and ".join([x+"=%s" for x in condition]))
            cursor.execute(select_sql, tuple(condition_vals))
            result = cursor.fetchall()
            return result
