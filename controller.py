from flask import Flask, request, jsonify
from config import db  # Importamos el objeto db
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

reservas = []  # Aquí guardarás tus reservas (en memoria, para este ejemplo)

@app.route('/ejemplo')
def ejemplo():
    # Aquí puedes usar db para interactuar con MongoDB
    users = db.usuarios.find({}) # ejemplo de consulta
    return str(list(users))


@app.route('/reservas', methods=['POST'])
def crear_reserva():
    # Aquí manejamos la creación de una reserva
    data = request.get_json()

    # Verificamos que la información necesaria esté presente
    if not data or "usuario" not in data or "vehiculo" not in data:
        return jsonify(message="Información Inválida"), 400
    
    #Verificamos que el usuario, vehiculo y fecha sean valores validos
    if not isinstance(data["usuario"], str) or not isinstance(data["vehiculo"], str):
        return jsonify(message="Formato de datos inválido"), 400
    
    nueva_reserva = {
        "_id": ObjectId(),
        "usuario_id": data["usuario"],
        "vehiculo_id": data["vehiculo"],
        "fecha_inicio": data["fecha_inicio"],
        "fecha_fin": data["fecha_fin"],
        "estado": "reservado"
    }

     # Verificar si ya existe una reserva para el vehículo en el mismo rango de fechas
    fecha_inicio_nueva = datetime.strptime(data["fecha_inicio"], "%Y-%m-%d")
    fecha_fin_nueva = datetime.strptime(data["fecha_fin"], "%Y-%m-%d")

    
    reserva_existe = db.reservas.find_one({
    "usuario_id": data["usuario"],
    "vehiculo_id": data["vehiculo"],
    "$or": [
        {
            "fecha_inicio": {"$lte": fecha_inicio_nueva},
            "fecha_fin": {"$gte": fecha_inicio_nueva}
        },
        {
            "fecha_inicio": {"$lte": fecha_fin_nueva},
            "fecha_fin": {"$gte": fecha_fin_nueva}
        },
        {
            "fecha_inicio": {"$gte": fecha_inicio_nueva},
            "fecha_fin": {"$lte": fecha_fin_nueva}
        }
    ]
    })

    if reserva_existe:
        return jsonify(message="Vehículo ya reservado en este rango de fechas"), 400
    
    db.reservas.insert_one(nueva_reserva)

    # Convertimos el id a string para la respuesta JSON
    nueva_reserva["_id"] = str(nueva_reserva["_id"])
    return jsonify(message="Reserva creada con exito", nueva_reserva=nueva_reserva), 201

@app.route('/reservas/<id_reserva>', methods=['DELETE'])
def cancelar_reserva(id_reserva):
  # Aquí manejaremos la cancelación de una reserva
  global reservas

  # Buscar la reserva en la base de datos
  reserva_a_cancelar = db.reservas.find_one({"_id": ObjectId(id_reserva)})

  if reserva_a_cancelar:
    # Eliminar la reserva de la base de datos
    db.reservas.delete_one({"_id": ObjectId(id_reserva)})
    return jsonify(message="Reserva cancelada con exito"), 200
  else:
      return jsonify(message="Reserva no encontrada"), 404

if __name__ == '__main__':
    app.run(debug=True)
