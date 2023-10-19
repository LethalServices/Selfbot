import os, sqlite3

class DatabaseManager:
    """
    Manages operations on SQLite3 database, including creating, closing connections, and executing queries.
    
    Attributes:
        db_file (str): Path to the SQLite3 database file.
        conn (sqlite3.Connection, optional): SQLite3 connection object. Defaults to None.
        cur (sqlite3.Cursor, optional): SQLite3 cursor object for executing SQL commands. Defaults to None.
    """
    
    def __init__(self, db_file):
        """
        Initializes the DatabaseManager object and setups database connection.
        
        Args:
            db_file (str): Path to the SQLite3 database file.
        """
        self.db_file = db_file
        self.conn = None
        self.cur = None
        self.create_connection()
        self.database_setup()

    def create_connection(self):
        """
        Creates a connection to the SQLite3 database. If the database doesn't exist, it's created.
        """
        if not os.path.exists(self.db_file):
            self.conn = sqlite3.connect(self.db_file)
            self.cur = self.conn.cursor()
            self.database_setup()
        else:
            self.conn = sqlite3.connect(self.db_file)
            self.cur = self.conn.cursor()

    def close_connection(self):
        """
        Closes the connection to the SQLite3 database and resets the connection and cursor attributes.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cur = None

    def database_setup(self):
        """
        Sets up the database schema if not already present. Also initializes some default configurations.
        """
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS auth(id INTEGER PRIMARY KEY,token VARCHAR(255));""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS config(id INTEGER PRIMARY KEY,message_logger VARCHAR(255),antistaff VARCHAR(255),prefix VARCHAR(255),antigrabify VARCHAR(255),antianonexploit VARCHAR(255),afk VARCHAR(255));""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS blacklist(id INTEGER PRIMARY KEY,member_id VARCHAR(255));""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS groupchat(id INTEGER PRIMARY KEY,member_id VARCHAR(255));""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS webhooks(id INTEGER PRIMARY KEY,message_wh VARCHAR(255),sniper_wh VARCHAR(255));""")
            self.cur.execute("""SELECT message_logger, antistaff, Afk, prefix, antigrabify, antianonexploit FROM config;""")
            row = self.cur.fetchone()
            if row is None:
                self.cur.execute("""INSERT INTO config (message_logger,antistaff,prefix,antigrabify,antianonexploit,afk) VALUES ('off','0','.','off','off','off');""")
            self.cur.execute("""SELECT message_wh, sniper_wh FROM webhooks;""")
            row = self.cur.fetchone()
            if row is None:
                self.cur.execute("""INSERT INTO webhooks (message_wh, sniper_wh)VALUES ('url', 'url');""")
            self.conn.commit()
        except sqlite3.Error as e:
            return f"Error setting up the database: {e}"
            self.close_connection()
            raise

    def execute_query(self, query, params=None):
        """
        Executes a database query, mostly used for INSERT, UPDATE, DELETE operations.
        
        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): Parameters for SQL query. Defaults to None.
        """
        c = self.conn.cursor()
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        self.conn.commit()

    def execute_read_all_query(self, query, params=None):
        """
        Executes a read query that returns all matching rows.
        
        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): Parameters for SQL query. Defaults to None.
        
        Returns:
            list: List of tuples containing the resulting rows.
        """
        c = self.conn.cursor()
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        return c.fetchall()

    def execute_read_one_query(self, query, params=None):
        """
        Executes a read query that returns a single matching row.
        
        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): Parameters for SQL query. Defaults to None.
        
        Returns:
            tuple: The first matching row, or None if there are no matches.
        """
        c = self.conn.cursor()
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        return c.fetchone()
