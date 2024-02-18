import sqlite3
import psycopg2

# 1. Экспорт данных из SQLite3
def export_data_from_sqlite():
    conn_sqlite = sqlite3.connect('exhibits.db')
    cursor_sqlite = conn_sqlite.cursor()

    cursor_sqlite.execute("SELECT * FROM exhibits")
    data = cursor_sqlite.fetchall()

    conn_sqlite.close()
    print(data)
    return data

# 2. Импорт данных в PostgreSQL
def import_data_to_postgresql(data):
    conn_postgresql = psycopg2.connect(database='exhibits', user='postgres', password='Aa01011991TrumaA', host='localhost')
    cursor_postgresql = conn_postgresql.cursor()

    for row in data:
        cursor_postgresql.execute(
            "INSERT INTO exhibits (name, quantity, obtaining, discovery, description, assignment, number, collection, fund) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            row
        )
    conn_postgresql.commit()
    conn_postgresql.close()

# 3. Выполнение миграции данных
def migrate_data():
    data = export_data_from_sqlite()
    import_data_to_postgresql(data)

# Запуск миграции данных
migrate_data()
