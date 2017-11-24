class Hive_read_write:
    def __init__(self, host,usr=None,pwd=None,port=10000,database='default', auth_mechanism='PLAIN'):
        """
        host: str,The hostname for HS2,for Impala,this can be any of the `impalas`s
        usr: str,optional,if applicable
        pwd: str,optional,if applicable
        port: int,optional ,the Imapala default is 21050.the Hive port is likely different
        database: str,optional,if None,the result is implementation-dependent
        auth_mechanism: {'NOSASL','PLAIN','GSSAPI','LDAP'}
        'NOSASL': for unsecured Impala
        'PLAIN': for unsecured Hive(because Hive requires the SASL transport)
        'GSSAPI':for Kerberos
        'LDAP':for Kerberos with LDAP
        """
        try:
            from impala.dbapi import connect
            try:
                self.conn = connect(host=host, port=port, database=database,auth_mechanism=auth_mechanism,user=usr,password=pwd)
            except:
                raise
        except:
            raise

    #读取成列表格式
    def read_to_list(self,sql):
        try:
            self.cursor = self.conn.cursor()  # 获取游标
            self.cursor.execute(sql)
            self.result = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
        except:
            raise
        return(self.result)

    #读取成数据框格式
    def read_to_dataframe(self, sql):
        try:
            from impala.util import as_pandas
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.df = as_pandas(self.cursor)
        except:
            raise
        return(self.df)

    # 执行sql
    def exec_sql(self,sql):
        try:
            self.cursor = self.conn.cursor()  # 获取游标
            self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
            self.res = "done"
        except:
            self.res = "failed"
            raise
        return(self.res)

    # 关闭数据库连接
    def close(self):
        self.conn.close()
