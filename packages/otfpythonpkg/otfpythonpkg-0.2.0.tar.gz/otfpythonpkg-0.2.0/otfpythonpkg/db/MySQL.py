# import mysql.connector
import pymysql
import time
from sshtunnel import SSHTunnelForwarder

class OtfMySQLConnection():
    _config = None
    _dbsection = ""
    _sshTunnel = None
    _dbconn = None
    _otbaseSchemaName = "OTbase"
    _otbaseStatSchemaName = "OTbaseStat"
    _otpushSchemaName = "OTpush"
    _otstageSchemaName = "OTstage"
    _otstageETLSchemaName = "OTstageETL"
    _otstageOTInsightsSchemaName = "OTstageOTInsights"
    _otcrmSchemaName = "OTcrm"
    _currentCursor = None

    def __init__(self, dbSchemas):
        self._otbaseSchemaName = dbSchemas['OTbase']
        self._otpushSchemaName = dbSchemas['OTpush']
        self._otstageSchemaName = dbSchemas['OTstage']
        self._otstageETLSchemaName = dbSchemas['OTstageETL']
        self._otstageOTInsightsSchemaName = dbSchemas['OTstageOTInsights']
        self._otbaseStatSchemaName = dbSchemas['OTbaseStat']
        self._otcrmSchemaName = dbSchemas['OTcrm']

    def open(self, host, user, password, dbName, port=3306):
        #        self._dbconn = mysql.connector.connect(
        #            host=host, user=user, passwd=password, port=port, database=dbName)
        self._dbconn = pymysql.connect(
            host=host, user=user, passwd=password, port=int(port), database=dbName)

    def open_ssh_tunnel(self, host, user, password, dbName, port=3306):
        self.close()

        try:
            self._sshTunnel = self.create_ssh_tunnel(host, port)
            self._sshTunnel.start()
        except Exception as ex:
            self._sshTunnel = None
            raise ex

        port = self._sshTunnel.local_bind_port
        hostname = "127.0.0.1"

        x = range(6)

        for n in x:
            try:
                self._dbconn = None

                self._dbconn = pymysql.connect(user=user,
                                               passwd=password,
                                               host=hostname,
                                               database=dbName,
                                               port=port,
                                               charset='utf8',
                                               use_unicode=True)

                break
            except Exception as e:
                self._dbconn = None
                print("Error connecting to database: {}".format(str(e)))
                time.sleep(5)

        if self._dbconn is None:
            self.close()
            raise Exception("Unable to connect to database.  Retries have been exceeded")

        print("Connected to RDS host {} port {}".format(host, port))

        try:
            self.executeNonQuery("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

            row = self.fetchRow("SELECT @@SESSION.tx_isolation as isolevel")

            if row:
                print("Isolation level is now {}".format(row["isolevel"]))
            else:
                print("Isolation level is unknown")

        except Exception as e:
            print("Error setting transaction isolation level", e)

        return port

    def close(self):
        if self._dbconn is not None:
            try:
                self._dbconn.close()
            except Exception:
                pass

            self._dbconn = None

    def create_ssh_tunnel(self, host, port):
        sshkey = "/Users/rroyce/Documents/sslkeys/otf-bastion-prod.pem"
        jumpserver = "prodbastion.orangetheory.co"
        sshuser = "ec2-user"
        sshlocalport = 5432
        sshport = 22

        tunnel = None
        tries_ = 0

        if tunnel is None and tries_ < 5:
            try:
                print(f"Connecting to sshtunnel [{jumpserver}] ssh port [{sshport}]  ssh username [{sshuser}]  ssh key [{sshkey}]  remote host [{host}]  remote port [{port}]")
                tunnel = SSHTunnelForwarder(
                    (jumpserver, sshport),
                    ssh_username=sshuser,
                    ssh_pkey=sshkey,
                    remote_bind_address=(
                        host,
                        int(port)
                    )
                )
            finally:
                tries_ += 1
                time.sleep(.5)

        return tunnel

    def fetchRow(self, sql):
        d = self._dbconn.cursor(pymysql.cursors.DictCursor)

        d.execute(sql)

        row = d.fetchone()

        d.close()

        return row

    def fetchRows(self, sql, asDict=True):
        if asDict:
            d = self._dbconn.cursor(pymysql.cursors.DictCursor)
        else:
            d = self._dbconn.cursor()

        d.execute(sql)

        rows = d.fetchall()

        d.close()

        return rows

    def fetchRowsMany(self, sql, blocksize, closecursor):
        if self._currentCursor is None:
            self._currentCursor = self._dbconn.cursor(
                pymysql.cursors.DictCursor)
            self._currentCursor.execute(sql)

        rows = self._currentCursor.fetchmany(int(blocksize))

        if rows is None or closecursor:
            self._currentCursor.close()
            self._currentCursor = None

        return rows

    def executeNonQuery(self, sql):
        d = self._dbconn.cursor(pymysql.cursors.DictCursor)

        rowsAffected = d.execute(sql)

        d.close()

        return rowsAffected

    def executemany(self, sql, data):
        d = self._dbconn.cursor(pymysql.cursors.DictCursor)

        rowsAffected = d.executemany(sql, data)

        d.close()

        return rowsAffected

    def truncateTable(self, tableName):
        cur = self._dbconn.cursor()

        cur.execute("TRUNCATE TABLE {}".format(tableName))

        cur.close()

    def dropTable(self, tableName):
        sql = "DROP TABLE IF EXISTS {}".format(tableName)

        self.executeNonQuery(sql)

    def tableExists(self, tableSchema, tableName):
        sql = "SELECT table_name FROM information_schema.tables where table_schema = '{}' and table_name = '{}'".format(
            tableSchema, tableName)

        row = self.fetchRow(sql)

        return row is not None

    def OTbaseSchema(self):
        return self._otbaseSchemaName

    def OTbaseStatSchema(self):
        return self._otbaseStatSchemaName

    def OTpushSchema(self):
        return self._otpushSchemaName

    def OTcrmSchema(self):
        return self._otcrmSchemaName

    def OTstageSchema(self):
        return self._otstageSchemaName

    def OTstageETLSchema(self):
        return self._otstageETLSchemaName

    def rollback(self):
        self._dbconn.rollback()

    def commit(self):
        self._dbconn.commit()

    def get_connection(self):
        return self._dbconn

    def callStoredProcedureWithRead(self, storedProcName, args):
        d = self._dbconn.cursor(pymysql.cursors.DictCursor)

        d.callproc(storedProcName, args)

        rows = d._rows

        d.close()

        return rows
