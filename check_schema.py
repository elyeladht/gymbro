import sqlite3

sql = open("schema.sql", encoding="utf-8").read()
conn = sqlite3.connect(":memory:")  # banco temporário, não mexe no gym.db

for stmt in sql.split(";"):
    if stmt.strip():
        try:
            conn.execute(stmt)
        except sqlite3.Error as e:
            print("ERRO:", e)
            print("No comando:")
            print(stmt)
            break
else:
    print("Schema OK!")