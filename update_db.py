import os
from pathlib import Path

import mysql.connector
import conf
from functions.user_choices import get_user_option


def execute_sql_file(cursor: mysql.connector.cursor, file_path: str, ignore_drop: bool = False) -> None:
    """
    Reads an SQL fiel and executes its commands using the provided cursor.

    Args:
        cursor (mysql.connector.cursor): The database cursor.
        file_path (str): The path to the SQL file.
        ignore_drop (bool): If True, ignore SQL commands that start with "DROP TABLE".

    @author Eduardo Esteves
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()

    commands = []
    delimiter = ";"
    command = ""
    sql_file = Path(file_path).name

    for line in sql_script.splitlines():
        if line.lower().startswith("delimiter"):
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
        if ignore_drop and command.strip().lower().startswith("drop table"):
            print(f"Ignoring command: {command.strip()} in {sql_file}\n")
            break
        try:
            if command.strip():
                cursor.execute(command)
        except mysql.connector.Error as err:
            match err.errno:
                case 1060:
                    print(f"Warning: {err.errno} {err.sqlstate} {err.msg} in {sql_file}\n")
                case _:
                    print(f"Error executing command: {command}\nError: {err} in {sql_file}\n")


def main(option: int) -> None:
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
    total = 0

    # Execute each SQL file in order
    for sql_file in sql_files:
        print(f"Executing {sql_file}...")

        if option == 1:
            execute_sql_file(cursor, os.path.join(path, sql_file))
        else:
            execute_sql_file(cursor, os.path.join(path, sql_file), ignore_drop=True)
        cnx.commit()
        total += 1

    cursor.close()
    cnx.close()
    print(f"\nALL {total} SQL scripts have been executed.")


if __name__ == '__main__':
    user_option = get_user_option()
    main(user_option)
