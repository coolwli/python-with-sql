import pyodbc

def connect_to_database(server, database):
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database}'
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f'Error: {e}')
        return None

def insert_record(conn, table, columns, values):
    try:
        cursor = conn.cursor()
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in values])})"
        cursor.execute(query, values)
        conn.commit()
        print("Data successfully inserted.")
    except Exception as e:
        print(f'Error: {e}')

def update_record(conn, table, set_values, condition):
    try:
        cursor = conn.cursor()
        query = f"UPDATE {table} SET {', '.join([f'{column} = ?' for column in set_values.keys()])} WHERE {condition}"
        cursor.execute(query, list(set_values.values()))
        conn.commit()
        if cursor.rowcount == 0:
            print("No matching rows found for the given condition.")
        else:
            print("Data successfully updated.")
    except Exception as e:
        print(f'Error: {e}')

def delete_record(conn, table, condition):
    try:
        cursor = conn.cursor()
        query = f"DELETE FROM {table} WHERE {condition}"
        cursor.execute(query)
        conn.commit()
        if cursor.rowcount == 0:
            print("No matching rows found for the given condition.")
        else:
            print("Data successfully deleted.")
    except Exception as e:
        print(f'Error: {e}')

def print_table(conn, table):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        for row in cursor:
            print(row)
    except Exception as e:
        print(f'Error: {e}')

def print_records(conn, table, condition):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {condition}")
        if cursor.rowcount == 0:
            print("No matching rows found for the given condition.")
        else:
            for row in cursor:
                print(row)
    except Exception as e:
        print(f'Error: {e}')

def get_column_value(conn, table, column, column_condition, value):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column} FROM {table} WHERE {column_condition} = ?", value)
        row = cursor.fetchone()
        if row:
            print(f"{column} value for the given condition: {row[0]}")
        else:
            print("No matching rows found for the given condition.")
    except Exception as e:
        print(f'Error: {e}')

def menu():
    server = "your-server-name"
    database = "your-database-name"
    table = "your-table-name"
    conn = connect_to_database(server, database)
    if conn:
        print("\nMenu:")
        print("1. Insert a new record")
        print("2. Update an existing record")
        print("3. Delete a record")
        print("4. Print all records in the table")
        print("5. Print records with specific conditions")
        print("6. Get a column value based on a condition")
        print("0. Exit")

        while True:
            choice = input("Please make your choice (0-6): ")

            if choice == "1":
                columns = input("Enter column names separated by commas: ").split(",")
                values = input("Enter values separated by commas: ").split(",")
                insert_record(conn, table, columns, values)
            elif choice == "2":
                set_values = {}
                while True:
                    column = input("Enter the column name to update (or type 'finish' to exit): ")
                    if column.lower() == "finish":
                        break
                    value = input("Enter the new value: ")
                    set_values[column] = value
                column_condition = input("Enter the column name for update condition: ")
                value = input("Enter the matching value: ")
                condition = f"{column_condition} = '{value}'"
                update_record(conn, table, set_values, condition)
            elif choice == "3":
                column = input("Enter the column name for deletion: ")
                value = input("Enter the matching value: ")
                condition = f"{column} = '{value}'"
                delete_record(conn, table, condition)
            elif choice == "4":
                print_table(conn, table)
            elif choice == "5":
                column = input("Enter the column name for condition: ")
                value = input("Enter the matching value: ")
                condition = f"{column} = '{value}'"
                print_records(conn, table, condition)
            elif choice == "6":
                column = input("Enter the column name to retrieve value: ")
                column_condition = input("Enter the column name for condition: ")
                value = input("Enter the matching value: ")
                get_column_value(conn, table, column, column_condition, value)
            elif choice == "0":
                conn.close()
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select a number from the menu.")

menu()
