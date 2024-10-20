def alumne_schema(fetchalumne) -> dict:  # En esta función lo que hago es convertir los datos de los alumnos
                                    # en un diccionario donde a cada campo se le asigna su posición
    return {
        "NomAlumne": fetchalumne[0],
        "Cicle": fetchalumne[1],
        "Curs": fetchalumne[2],
        "Grup": fetchalumne[3],  # Adapto el alumne_schema con los campos que nos pide en la práctica 2
        "DescAula": fetchalumne[4],
        
    }

def alumnes_schema(alumnes) -> list:
    return [alumne_schema(alumne) for alumne in alumnes] 
# Esta función convierte la lista de los alumnos en una lista de diccionarios como la función de arriba
