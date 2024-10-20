from client import db_client

# Verificar si un aula existe por su IdAula
async def check_aula(id_aula: int) -> bool:  # Con esta función lo que quiero es verificar si el aula existe 
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT 1 FROM Aula WHERE IdAula = %s"
        cur.execute(query, (id_aula,))
        aula = cur.fetchone()
    except Exception as e:
        return False
    finally:
        conn.close()

    return aula is not None  # Como es un booleano si existe el aula nos devolvera True en caso de que no exista nos devolvera False

# Esto lo hago para poder añadir nuevos cambios, es decir para que los id no sean iguales
