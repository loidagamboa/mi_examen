from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumnos.db'
db = SQLAlchemy(app)

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    aprobado = db.Column(db.Boolean, nullable=False)
    nota = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "aprobado": self.aprobado,
            "nota": self.nota,
            "fecha": self.fecha.isoformat()
        }

def crear_base_de_datos():
    # Conexión a la base de datos (se creará si no existe)
    conn = sqlite3.connect('alumnos.db')
    cur = conn.cursor()
    
    # Crear la tabla 'alumnos' si no existe
    cur.execute('''
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        aprobado BOOLEAN NOT NULL,
        nota REAL NOT NULL,
        fecha TIMESTAMP NOT NULL
    )
    ''')

    # Lista de alumnos a insertar
    alumnos = [
        ('Juan', 'Pérez', True, 7.5, '2024-09-01 00:00:00'),
        ('María', 'López', False, 4.2, '2024-09-02 00:00:00'),
        ('Carlos', 'García', True, 8.9, '2024-09-03 00:00:00'),
        ('Lucía', 'Martínez', True, 9.1, '2024-09-04 00:00:00'),
        ('Sofía', 'Fernández', False, 5.0, '2024-09-05 00:00:00')
    ]

    # Insertar los registros en la tabla 'alumnos'
    cur.executemany('''
        INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha)
        VALUES (?, ?, ?, ?, ?)
    ''', alumnos)

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

@app.route('/alumnos', methods=['POST'])
def agregar_alumno():
    data = request.json
    nuevo_alumno = Alumno(
        nombre=data['nombre'],
        apellido=data['apellido'],
        aprobado=data['aprobado'],
        nota=data['nota'],
        fecha=data['fecha']
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    return jsonify(nuevo_alumno.to_dict()), 201

@app.route('/alumnos', methods=['GET'])
def obtener_alumnos():
    alumnos = Alumno.query.all()
    return jsonify([alumno.to_dict() for alumno in alumnos])

if __name__ == "__main__":
    db.create_all()  # Crea la base de datos y las tablas
    crear_base_de_datos()  # Llama a la función para crear y llenar la base de datos
    app.run(debug=True)