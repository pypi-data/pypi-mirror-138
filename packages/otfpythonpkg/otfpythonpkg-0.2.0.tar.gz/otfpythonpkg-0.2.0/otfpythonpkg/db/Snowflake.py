import snowflake.connector


class SnowflakeConnection:
    _dbconn = None
    _config = None

    def open(self, config):
        self._config = config

        self.close()

        host = config["HOST"]
        user = config["USERNAME"]
        password = config["PASSWORD"]
        account = config["ACCOUNT_ID"]
        warehouse = config["WAREHOUSE"]
        role = config["ROLE_NAME"]

        self._dbconn = snowflake.connector.connect(
            host=host, user=user, password=password, account=account, warehouse=warehouse)

        self.executeNonQuery("USE ROLE {}".format(role))
        self.executeNonQuery("USE WAREHOUSE {}".format(warehouse))

    def close(self):
        if self._dbconn is not None:
            try:
                self._dbconn.close()
            except Exception:
                pass

            self._dbconn = None

    def executeNonQuery(self, sql):
        d = self._dbconn.cursor()

        rc = d.execute(sql)

        rowsAffected = rc.rowcount

        d.close()

        return rowsAffected

    def executeMany(self, sql, rows):
        d = self._dbconn.cursor()

        rc = d.executemany(sql, rows)

        rowsAffected = rc.rowcount

        d.close()

        return rowsAffected

    def fetchRow(self, sql):
        d = self._dbconn.cursor()

        try:
            d.execute(sql)

            row = d.fetchone()

            d.close()
        except Exception as e:
            d.close()
            raise e

        return row

    def fetchRows(self, sql):
        d = self._dbconn.cursor()

        try:
            d.execute(sql)

            rows = d.fetchall()

            d.close()
        except Exception as e:
            d.close()
            raise e

        return rows

    def fetchRowsDF(self, sql):
        c = self._dbconn.cursor()

        try:
            cur = c.execute(sql)

            rows = cur.fetch_pandas_all()

            return rows
        except Exception as e:
            raise e

    def rollback(self):
        self._dbconn.rollback()

    def commit(self):
        self._dbconn.commit()

    def getDMLRowsAffected(self, rowsAffected):
        try:
            sql = "select * from table(RESULT_SCAN ( LAST_QUERY_ID() ))"

            row = self.fetchRow(sql)

            return row
        except Exception:
            return None

    def getMultipleDMLRowsAffected(self, rowsAffected):
        try:
            sql = "select * from table(RESULT_SCAN ( LAST_QUERY_ID() ))"

            rows = self.fetchRow(sql)

            return rows
        except Exception:
            return [{"inserted": 0, "updated": rowsAffected}]
