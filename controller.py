from flask import Flask, request, jsonify
from config import db  # Importamos el objeto db
from bson.objectid import ObjectId
from datetime import datetime,timedelta

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
    if not data or "usuario_id" not in data or "vehiculo_id" not in data:
        return jsonify(message="Información Inválida"), 400
    
    #Verificamos que el usuario, vehiculo y fecha sean valores validos
    if not isinstance(data["usuario_id"], str) or not isinstance(data["vehiculo_id"], str):
        return jsonify(message="Formato de datos inválido"), 400
    
    nueva_reserva = {
        "_id": ObjectId(),
        "usuario_id": data["usuario_id"],
        "vehiculo_id": data["vehiculo_id"],
        "fecha_inicio": data["fecha_inicio"],
        "fecha_fin": data["fecha_fin"],
        "estado": "reservado"
    }

     # Verificar si ya existe una reserva para el vehículo en el mismo rango de fechas
    fecha_inicio_nueva = datetime.strptime(data["fecha_inicio"], "%Y-%m-%d")
    fecha_fin_nueva = datetime.strptime(data["fecha_fin"], "%Y-%m-%d")

    
    reserva_existe = db.reservas.find_one({
    "usuario_id": data["usuario_id"],
    "vehiculo_id": data["vehiculo_id"],
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
    """Aquí manejamos la cancelación de una reserva"""
    # Buscar la reserva en la base de datos
    reserva_a_cancelar = db.reservas.find_one({"_id": ObjectId(id_reserva)})

    if reserva_a_cancelar:
        # Obtener la fecha actual
        hoy = datetime.now().date()
        hoyS = datetime.now().date().strftime('%Y-%m-%d')
        # Convertir la fecha_fin a un objeto date
        fecha_fin_reserva = datetime.strptime(reserva_a_cancelar['fecha_fin'], '%Y-%m-%d').date()

        # Verificar que la fecha fin sea igual a hoy o anterior
        if fecha_fin_reserva >= hoy:
            # Actualizar el estado a cancelado
            db.reservas.update_one({"_id": ObjectId(id_reserva)}, {"$set": {"estado": "cancelado"}})
            db.reservas.update_one({"_id": ObjectId(id_reserva)}, {"$set": {"fecha_fin": hoyS}})
            # Eliminar la reserva de la base de datos
            # db.reservas.delete_one({"_id": ObjectId(id_reserva)})
            fecha_inicio_semana = datetime.combine((datetime.today() - timedelta(days=datetime.today().weekday())), datetime.min.time()).strftime('%Y-%m-%d')
            fecha_fin_semana = datetime.combine((datetime.today() - timedelta(days=datetime.today().weekday()-6)), datetime.max.time()).strftime('%Y-%m-%d')
            # ...
            print("***************************************************************")
            print( fecha_inicio_semana)
            print( fecha_fin_semana)
            print(reserva_a_cancelar.get("usuario_id"))
            reservas_canceladas = list(db.reservas.find({
                "usuario_id": reserva_a_cancelar.get("usuario_id"),
                "$and": [
                    {"fecha_fin": {"$gte": fecha_inicio_semana}},
                    {"fecha_fin": {"$lte": fecha_fin_semana}},
                ],
                "estado": "cancelado"
            }))
            print(len(reservas_canceladas))
            if len(reservas_canceladas) >= 2:
                return jsonify({"message": "Has sido penalizado por cancelar tres reservas en una semana."}), 400
            else:
                return jsonify(message="Reserva cancelada con éxito"), 200
        else:
            return jsonify(message="La reserva solo se puede cancelar en la fecha de finalización o antes"), 400
    else:
        return jsonify(message="Reserva no encontrada"), 404


if __name__ == '__main__':
    app.run(debug=True)
