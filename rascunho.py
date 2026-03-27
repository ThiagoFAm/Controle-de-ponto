import sqlite3

conn = sqlite3.connect('instance/banco.db')

conn.execute("ALTER TABLE registros ADD COLUMN tipo TEXT")

conn.commit()
conn.close()

print("Coluna 'tipo' adicionada")
