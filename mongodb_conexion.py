from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
import os

load_dotenv()


class ConexionMongoDB:

    def __init__(self):
        self.connection_string = os.getenv("MONGO_URI")
        self.database_name = os.getenv("MONGO_DB")
        self.client = None
        self.db = None

    def conectar(self):
        if not self.connection_string or not self.database_name:
            print("Error: revisa las variables del archivo .env")
            return False

        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=10000
            )

            self.client.admin.command("ping")
            self.db = self.client[self.database_name]

            print("Conexión exitosa a MongoDB en Clever Cloud")
            return True

        except PyMongoError as e:
            print(f"Error de conexión: {e}")
            return False

    def insertar_estudiante(self, datos):
        resultado = self.db.estudiantes.insert_one(datos)
        print(f"Estudiante insertado con ID: {resultado.inserted_id}")

    def listar_estudiantes(self):
        estudiantes = self.db.estudiantes.find()

        print("\nLISTA DE ESTUDIANTES")
        encontrado = False

        for est in estudiantes:
            encontrado = True
            print(
                f"Nombre: {est.get('nombre', 'N/D')}, "
                f"Email: {est.get('email', 'N/D')}, "
                f"Carrera: {est.get('carrera', 'N/D')}"
            )

        if not encontrado:
            print("No existen estudiantes registrados.")

    def buscar_por_carrera(self, carrera):
        estudiantes = self.db.estudiantes.find({
            "carrera": carrera
        })

        print(f"\nESTUDIANTES DE {carrera}")
        encontrado = False

        for est in estudiantes:
            encontrado = True
            print(
                f"Nombre: {est.get('nombre', 'N/D')}, "
                f"Edad: {est.get('edad', 'N/D')}"
            )

        if not encontrado:
            print("No se encontraron estudiantes.")

    def cerrar(self):
        if self.client is not None:
            self.client.close()


def main():
    mongo_db = ConexionMongoDB()

    if not mongo_db.conectar():
        return

    try:
        while True:
            print("\n===== MENÚ MONGODB =====")
            print("1. Insertar estudiante")
            print("2. Listar todos los estudiantes")
            print("3. Buscar por carrera")
            print("4. Salir")

            opcion = input("Selecciona opción: ")

            try:
                if opcion == "1":
                    nombre = input("Nombre: ")
                    email = input("Email: ")
                    edad = int(input("Edad: "))
                    carrera = input("Carrera: ")

                    estudiante = {
                        "nombre": nombre,
                        "email": email,
                        "edad": edad,
                        "carrera": carrera,
                        "activo": True
                    }

                    mongo_db.insertar_estudiante(estudiante)

                elif opcion == "2":
                    mongo_db.listar_estudiantes()

                elif opcion == "3":
                    carrera = input("Carrera a buscar: ")
                    mongo_db.buscar_por_carrera(carrera)

                elif opcion == "4":
                    print("Cerrando aplicación...")
                    break

                else:
                    print("Opción no válida.")

            except ValueError:
                print("Error: la edad debe ser un número entero.")

            except PyMongoError as e:
                print(f"Error en MongoDB: {e}")

    finally:
        mongo_db.cerrar()


if __name__ == "__main__":
    main()