import csv
from client import db_client
from typing import List, Tuple, Any, Dict
from pydantic import BaseModel
from typing import Optional


async def read() -> List[Tuple[Any]]: # Aqui lo que hacemos es leer todos los registros de la tabla Alumne
    try:
        conn = db_client()  # Establecemos la conexión con la base de datos y realizamos la consulta sql
        cur = conn.cursor()
        cur.execute("SELECT * FROM Alumne")
        alumnes = cur.fetchall() # Con esto recuperamos los resultados de la consulta
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        conn.close() # Con esto cerramos la conexión con la base de datos
    return alumnes

async def read_id(id: int) -> Tuple[Any]: # Leemos los alumnos por su ID y hacemos la consulta sql
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM Alumne WHERE IdAlumne = %s"
        value = (id,)
        cur.execute(query, value)
        alumne = cur.fetchone()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        conn.close()
    return alumne



async def create(alumne: BaseModel): # Esta función sirve para añadir un nuevo INSERT de alumno
    try:
        conn = db_client()
        cur = conn.cursor()
        
       # Agregamos el nuevo alumno en la tabla Alumno
        query = """
        INSERT INTO Alumne (IdAula, NomAlumne, Cicle, Curs, Grup, CreatedAt, UpdatedAt)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """
        values = (alumne.IdAula, alumne.NomAlumne, alumne.Cicle, alumne.Curs, alumne.Grup)
        cur.execute(query, values)
        conn.commit() # Esto lo que hace es aplicar los cambios en la base de datos
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    
    finally:
        conn.close()

    return {"status": 1, "message": "L' alumne s'ha afegit correctament"} # Cuando se aplican los cambios nos devuelve este mensaje




# En esta función lo que estoy haciendo es actualizar a un alumno que ya existe
async def update_alumne(id: int, updated_alumne: Dict[str, Any]) -> Dict[str, Any]:
    try:
        conn = db_client()
        cursor = conn.cursor()
        
        # Esta es la consulta sql para actualizar a un alumno
        sql = """
        UPDATE Alumne 
        SET IdAula = %s, NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s, UpdatedAt = NOW() 
        WHERE IdAlumne = %s
        """
        values = (
            updated_alumne["IdAula"],
            updated_alumne["NomAlumne"],
            updated_alumne["Cicle"],
            updated_alumne["Curs"],
            updated_alumne["Grup"],
            id
        )
        
        cursor.execute(sql, values)
        conn.commit()

        # Con esto comprobamos si se actualizó alguna fila
        if cursor.rowcount == 0:
            return {"status": 0, "message": "No s'ha trobat l'alumne que vols actualitzar"}

        cursor.close()
        conn.close()

        return {"status": 1, "message": "S’ha modificat correctament"}
    
    except Exception as e:
        return {"status": -1, "message": str(e)}
    


# En esta función lo que hago es eliminar a un alumno por su id
async def delete(id: int):
    try:
        conn = db_client()
        cursor = conn.cursor()

        # Esta es la consulta sql para eliminar a un alumno según el id que nosotros le especifiquemos
        sql = "DELETE FROM alumne WHERE IdAlumne = %s"
        cursor.execute(sql, (id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return {"status": 0, "message": "No s'ha trobat l'alumne que heu indicat"}
        
        cursor.close()
        conn.close()

        return {"status": 1, "message": "S’ha esborrat correctament l'alumne indicat"}
    except Exception as e:
        return {"status": -1, "message": str(e)}
    

# En esta última función lo que hago es listar a todos los alumnos junto a DescAula  
async def list_all_alumnes(orderby: Optional[str] = None, contain: Optional[str] = None, skip: Optional[int] = 0, limit: Optional[int] = 100):
    try:
        conn = db_client()  # Conexión a la base de datos
        cursor = conn.cursor()

       # Esta es la consulta sql que añade la información del aula a cada alumno
        sql = """
        SELECT 
            a.NomAlumne,
            a.Cicle,
            a.Curs,
            a.Grup,
            au.DescAula
        FROM alumne a
        LEFT JOIN aula au ON a.IdAula = au.IdAula
        """

        if contain:
            contain_valor = "%" + contain + "%"
            sql += " WHERE a.NomAlumne LIKE '" + contain_valor + "'"

        if orderby == "asc":
            sql += " ORDER BY a.NomAlumne ASC"
        if orderby == "desc":
            sql += " ORDER BY a.NomAlumne DESC"
        
        sql += " LIMIT " + str(limit) + " OFFSET " + str(skip)

        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        # Y retornamos los resultados en forma de lista de diccionarios para que se vea mejor visualmente
        return [{
            "NomAlumne": alumne[0],
            "Cicle": alumne[1],
            "Curs": alumne[2],
            "Grup": alumne[3],
            "DescAula": alumne[4]
        } for alumne in result]

    except Exception as e:
        print("Error en la base de datos:", str(e))
        return {"status": -1, "message": str(e)}


async def load_alumnes_from_csv(file_path: str) -> Dict[str, str]:
    try:
        conn = db_client()
        cursor = conn.cursor()

        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  

            for row in reader:
                desc_aula, edifici, pis, nom_alumne, cicle, curs, grup = row

                # Verificamos si el aula existe
                cursor.execute("SELECT IdAula FROM aula WHERE DescAula = %s", (desc_aula,))
                aula = cursor.fetchone()

                if not aula:
                    # En caso de que no exista insertamos el aula
                    cursor.execute("""
                        INSERT INTO aula (DescAula, Edifici, Pis)
                        VALUES (%s, %s, %s)
                    """, (desc_aula, edifici, pis))

                 # Verificamos si el alumno ya existe
                cursor.execute("""
                    SELECT IdAlumne FROM alumne 
                    WHERE NomAlumne = %s AND Cicle = %s AND Curs = %s AND Grup = %s
                """, (nom_alumne, cicle, curs, grup))
                alumne = cursor.fetchone()

                if not alumne:
                    # En caso de que no exista insertamos el alumno
                    cursor.execute("""
                        INSERT INTO alumne (NomAlumne, Cicle, Curs, Grup, IdAula, createdAt, updatedAt)
                        VALUES (%s, %s, %s, %s, (SELECT IdAula FROM aula WHERE DescAula = %s), CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())
                    """, (nom_alumne, cicle, curs, grup, desc_aula))

        conn.commit()
        return {"status": "success", "message": "Carga masiva completada."}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()