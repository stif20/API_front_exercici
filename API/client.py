import mysql.connector

def db_client():  # Con esta función lo que hago es establecer una conexión a la base de datos que he creado en HeidiSQL
    try:                        # Aqui le voy especificando todos los parametros necesarios para realizar la conexión
        dbname = "Alumnat"  
        user = "root" 
        password = "alejandro5" 
        host = "localhost"
        port = "3306"
        collation = "utf8mb4_general_ci"

        return mysql.connector.connect(  # Aqui pasa como parametro las variables que he definido anteriormente
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname,
            collation=collation
        ) 

    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}  # Y en caso de error resiviremos el mensaje de que hubo un error en la conexión

