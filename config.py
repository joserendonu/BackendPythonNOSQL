from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "databaseone" # Reemplaza esto con el nombre de tu base de datos

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Puedes agregar cualquier otra configuración necesaria aquí