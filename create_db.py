import sqlite3

# Conectar a la base de datos
con = sqlite3.connect('instance/site.db')

# Crear un cursor
cur = con.cursor()

# Crear una tabla
cur.execute('''CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL)''')

# Guardar los cambios y cerrar la conexión
con.commit()
con.close()
