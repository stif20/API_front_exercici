from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from typing import Dict, List, Optional
from pydantic import BaseModel
import db_alumnes  
import alumnes  
import db_aula
from fastapi.middleware.cors import CORSMiddleware
import csv
from fastapi.responses import JSONResponse


app = FastAPI() # Inicializo la aplicación FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Creo un modelo  Pydantic para la creación de Alumne 
class AlumneCreate(BaseModel):
    IdAula: int
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str

class AlumneUpdate(BaseModel): # Creo otro modelo Pydantic igual que el anterior pero en este caso lo voy a utilizar para realizar la operación Update
    IdAula: int
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str

# Y este lo utilizo para listar todos los registros del alumne junto a los registros del aula
class Alumne(BaseModel):
    IdAlumne: int
    IdAula: int
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str
    CreatedAt: str
    UpdatedAt: str

# Este BaseModel lo utilizo para la adaptación del endpoint de listAll
class tablaAlumne(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str
    DescAula: str


@app.get("/alumne/list", response_model=List[Alumne]) # Esta sera la ruta para obtener la lista de los alumnos /alumne/list
async def list_alumnes():
    alumnes_data = await db_alumnes.read() # Lee los alumnos y los llama
    if isinstance(alumnes_data, dict) and alumnes_data.get("status") == -1:
        raise HTTPException(status_code=500, detail=alumnes_data["message"]) # En caso de error lanza un error 500
    return alumnes.alumnes_schema(alumnes_data)



@app.post("/alumne/add") # Esta sera la ruta para añadir nuevos alumnos 
async def add_alumne(new_alumne: AlumneCreate):  # Uso el modelo pydantic que he creado especificamente para este apartado el cual es AlumneCreate
    aula_exists = await db_aula.check_aula(new_alumne.IdAula) # Compruebo si el aula existe en la base de datos
    if not aula_exists:
        raise HTTPException(status_code=400, detail="L'IdAula proporcionada no existeix.")

    result = await db_alumnes.create(new_alumne)
    
    if isinstance(result, dict) and result.get("status") == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    
    return {"message": "S’ha afegit correctament"}



@app.get("/alumne/show/{id}", response_model=Alumne) # Esta es la ruta para buscar un alumno segun su id
async def show_alumne(id: int):
    alumne_data = await db_alumnes.read_id(id) # Si el id esta bein se mostrara al alumno que tenga ese id
    if alumne_data:
        return alumnes.alumne_schema(alumne_data)
    else:
        raise HTTPException(status_code=404, detail=f"Alumne amb ID {id} no s'ha trobat")




@app.put("/alumne/update/{id}") # Esta es la ruta para actualizar a un alumno
async def update_alumne_endpoint(id: int, updated_alumne: AlumneUpdate): # Utilizo el modelo Pydantic que he creado para actualizar los datos de un alumno
    result = await db_alumnes.update_alumne(id, updated_alumne.dict())
    if result.get("status") == -1:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.delete("/alumne/delete/{id}") # Esta es la ruta para eliminar a un alumno
async def delete_alumne(id: int):
    
    result = await db_alumnes.delete(id)  # Llama a la función para eliminar el alumno
    
    if isinstance(result, dict) and result.get("status") == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    
    if result.get("status") == 0:
        raise HTTPException(status_code=404, detail="Alumne no trobat")

    return {"message": result["message"]}



@app.get("/alumne/listAll", response_model=List[tablaAlumne]) # Esta es la ruta para listar la información de los alumnos junto a su aula
async def list_all_alumnes(
    orderby: Optional[str] = Query(None, regex="^(asc|desc)$"),
    contain: Optional[str] = None,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100
    ):
    result = await db_alumnes.list_all_alumnes(orderby=orderby, contain=contain, skip=skip, limit=limit) # Llama a la función y devuelve los resultados
    
    if isinstance(result, dict) and result.get("status") == -1:
        raise HTTPException(status_code=500, detail=result["message"])

    return result # Devuelve la lista de los alumnos con toda su información

@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)) -> Dict[str, str]:
    try:
        contents = await file.read()
        with open("alumnos.csv", "wb") as f:
            f.write(contents)

        result = await db_alumnes.load_alumnes_from_csv("uploaded_file.csv")
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=400)
    

@app.get("/") # Esta es la ruta por defecto la cual nos devuelve el mensaje Hello World
def read_root():
    return {"Hello": "World"}
