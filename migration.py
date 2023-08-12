import mysql.connector

host = 'localhost'
dbname = 'gersgarage'
username = 'root'
password = ''
socket = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'  # Update this with the correct MySQL socket path

sql_file_path = 'gersgarage.sql'

# Connect using mysql.connector
try:
    conn = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=dbname,
        unix_socket=socket
    )
    print("Connected successfully!")

    cursor = conn.cursor()

    # Read and execute SQL queries from the file
    with open(sql_file_path, 'r') as sql_file:
        sql_queries = sql_file.read().split(';')

        for query in sql_queries:
            query = query.strip()
            if query:
                cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

    print("Migration successful!")

except mysql.connector.Error as err:
    print(f"Connection failed: {err}")
