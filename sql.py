import mysql.connector
from datetime import datetime

# Connect to MySQL
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gsbarkan2003gs",
    database="marvel1"
)

cursor = cnx.cursor()

# Check if table exists
cursor.execute("SHOW TABLES LIKE 'MarvelMovies'")
result = cursor.fetchone()

# If table does not exist, create it
if not result:
    create_table_query = """
    CREATE TABLE MarvelMovies (
        ID INT,
        MOVIE VARCHAR(255),
        DATE DATE,
        MCU_PHASE VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)

# Open the file and read lines
with open("marvel.txt", "r") as file:
    lines = file.readlines()

# Skip the first line (header line)
for i, line in enumerate(lines[1:], start=2):  # start=2 because we skipped the first line
    # Split line into parts
    parts = line.split('\t')

    # Check if parts has less than 4 elements
    if len(parts) < 4:
        print(f"Line {i} has less than 4 parts: {line}")
        continue

    # Format date
    date = datetime.strptime(parts[2], '%B%d,%Y').date()

    # Prepare insert query
    insert_query = "INSERT INTO MarvelMovies (ID, MOVIE, DATE, MCU_PHASE) VALUES (%s, %s, %s, %s)"

    # Insert data
    cursor.execute(insert_query, (int(parts[0]), parts[1], date, parts[3].strip()))

    # Prepare insert query
    insert_query = "INSERT INTO MarvelMovies (ID, MOVIE, DATE, MCU_PHASE) VALUES (%s, %s, %s, %s)"

    # Insert data
    cursor.execute(insert_query, (int(parts[0]), parts[1], date, parts[3].strip()))

# Commit changes
cnx.commit()
