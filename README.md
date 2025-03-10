# BackendPythonNOSQL
PETICIONES
createreserva
http://127.0.0.1:5000/reservas

{
    "usuario_id": "67cd6e9b634212495ed5bee2",
    "vehiculo_id": "67ce4e57f5d1215eb16175be",
    "fecha_inicio": "2026-08-17",
    "fecha_fin": "2026-03-26",
    "estado": "asdf"
}

cancelar reserva
http://127.0.0.1:5000/reservas/67ce579d44ce121a4fc99511


obtener reservas
http://127.0.0.1:5000/reservas/67cb922c97f80ff80416bf6f


vehiculo_mas_reservado
http://127.0.0.1:5000/vehiculo_mas_reservado

usuario mas cancelaciones
http://127.0.0.1:5000/reservas/usuarios_con_mas_cancelaciones

REFERENCIAS
Se debe instalar mongoDB
https://www.youtube.com/watch?v=2rAIiNgU79w


IMAGEN DE CREACION DE LA BD pero creo que falta en el último campo 
![alt text](image-1.png)


<!-- Si tu base de datos tiene autenticación, deberás modificar la URI de conexión para incluir usuario y contraseña. Por ejemplo: "mongodb://<usuario>:<contraseña>@localhost:27017/". -->