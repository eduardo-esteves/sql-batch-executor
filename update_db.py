import os
from pathlib import Path

import mysql.connector
import conf


def execute_sql_file(cursor: mysql.connector.cursor, file_path: str) -> None:
    """
    Reads an SQL fiel and executes its commands using the provided cursor.

    Args:
        cursor (mysql.connector.cursor): The database cursor.
        file_path (str): The path to the SQL file.

    @author Eduardo Esteves
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()

    commands = []
    delimiter = ";"
    command = ""
    sql_file = Path(file_path).name

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
            match err.errno:
                case 1060:
                    print(f"\nWarning: {err.errno} {err.sqlstate} {err.msg} in {sql_file}\n")
                case _:
                    print(f"\nError executing command: {command}\nError: {err} in {sql_file}\n")


def main():
    """
    Main function to execute SQL scripts from a specified directory in order.

    - Connects to the database using the configuration from enviroment variables.
    - Lists and sorts SQL files in the specified directory.
    - Executes each SQL file in order.

    @author Eduardo Esteves
    """

    # Path to the folder with SQL files
    path = Path(conf.BASE_DIR, 'database')

    # List and sort the files by numeric prefix
    sql_files = sorted(
        (f for f in os.listdir(path) if f.endswith('.sql')),
        key=lambda x: int(x.split('_')[0])
    )

    # Database connection
    cnx = mysql.connector.connect(**conf.config)
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
