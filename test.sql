from db_connect import connect_to_database
conn = connect_to_database()
cursor = conn.cursor()
cursor.execute("DESCRIBE Students")
columns = cursor.fetchall()
for column in columns:
    print(column)