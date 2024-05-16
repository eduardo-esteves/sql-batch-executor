import os
from pathlib import Path

from dotenv import load_dotenv
import mysql.connector

# take environment variables from .env.
load_dotenv()

# Database settings
config = {
    'user': os.getenv('dbuser'),
    'password': os.getenv('dbpass'),
    'host': os.getenv('dbhost'),
    'database': os.getenv('dbname'),
    'raise_on_warnings': True
}

BASE_DIR = Path(__file__).resolve().parent


def execute_sql_file(cursor, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()

    commands = []
    delimiter = ";"
    command = ""

    for line in sql_script.splitlines():
        if line.startswith("DELIMITER"):
            delimiter = line.split()[1]
            if command.strip():
                commands.append(command.strip())
                command = ""
        else:
            command += line + "\n"
            if delimiter in command:
                command = command.replace(delimiter, ";")
                commands.append(command.strip())
                command = ""

    if command.strip():
        commands.append(command.strip())

    for command in commands:
        try:
            if command.strip():
                cursor.execute(command)
        except mysql.connector.Error as err:
            print(f"Error executing command: {command}\nError: {err}")


def main():
    # Path to the folder with SQL files
    path = Path(BASE_DIR, 'database')

    # List and sort the files by numeric prefix
    sql_files = sorted(
        (f for f in os.listdir(path) if f.endswith('.sql')),
        key=lambda x: int(x.split('_')[0])
    )

    # Database connection
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Execute each SQL file in order
    for sql_file in sql_files:
        print(f"Executing {sql_file}...")
        execute_sql_file(cursor, os.path.join(path, sql_file))
        cnx.commit()

    cursor.close()
    cnx.close()
    print("ALL SQL scripts have been executed.")


if __name__ == '__main__':
    main()
