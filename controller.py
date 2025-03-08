from flask import Flask, request, jsonify
from config import db  # Importamos el objeto db

app = Flask(__name__)

reservas = []  # Aquí guardarás tus reservas (en memoria, para este ejemplo)

@app.route('/ejemplo')
def ejemplo():
    # Aquí puedes usar db para interactuar con MongoDB
    users = db.usuarios.find({}) # ejemplo de consulta
    return str(list(users))


@app.route('/reservas', methods=['POST'])
def crear_reserva():
    # Aquí manejaremos la creación de una reserva
    data = request.get_json()
    #  Verificamos que la información necesaria está presente
    if not data or 'usuario' not in data or 'vehiculo' not in data or 'fecha' not in data:
       return jsonify({'message':'Información inválida'}), 400

    nueva_reserva = {
        'id': len(reservas) + 1, # Usamos un ID sencillo para este ejemplo
        'usuario': data['usuario'],
        'vehiculo': data['vehiculo'],
        'fecha': data['fecha']
    }
    reservas.append(nueva_reserva)
    return jsonify({'message':'Reserva creada con éxito', 'reserva': nueva_reserva}), 201

@app.route('/reservas/<int:reserva_id>', methods=['DELETE'])
def cancelar_reserva(reserva_id):
    # Aquí manejaremos la cancelación de una reserva
    global reservas
    reservas = [reserva for reserva in reservas if reserva['id'] != reserva_id]
    return jsonify({'message':'Reserva cancelada con éxito'}), 200

if __name__ == '__main__':
    app.run(debug=True)
