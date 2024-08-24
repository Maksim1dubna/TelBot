import sqlite3

connection = sqlite3.connect("goods.db")
cursor = connection.cursor()
def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
    )
    ''')
def get_all_products():
    cursor.execute("SELECT * FROM Products;")
    # print(cursor.fetchall())
    result = cursor.fetchall()
    print(result[1][1])
    return result

connection.commit()
# connection.close()
