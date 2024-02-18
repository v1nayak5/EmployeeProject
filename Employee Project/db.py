from flask_mysqldb import MySQL
from app import app

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_mysql_username'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_database_name'

# Initialize MySQL
mysql = MySQL(app)

def query_db(query, args=(), one=False):
    """
    A utility function to simplify SQL queries. It executes a given SQL query with optional arguments
    and returns all results or just the first one.
    """
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
