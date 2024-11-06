from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class Mensaje(BaseModel):
    id: Optional[int] = None
    user: str
    mensaje: str

app = FastAPI()

mensaje_db = []

#Crear mensaje
@app.post("/mensaje/", response_model=Mensaje)
def crear_mensaje(mensaje: Mensaje):
    mensaje.id = len(mensaje_db) + 1  # Asignar un ID único
    mensaje_db.append(mensaje)  # Agregar el mensaje a la base de datos simulada
    return mensaje

# Obtener mensaje
@app.get("/mensajes/{mensaje_id}", response_model=Mensaje)
def obtener_mensaje(mensaje_id: int):
    for mensaje in mensaje_db:
        if mensaje.id == mensaje_id:
            return mensaje
    raise HTTPException(status_code=404, detail="Mensaje no encontrado")

# Listar todos los mensajes
@app.get("/mensajes/", response_model=List[Mensaje])
def listar_mensajes():
    return mensaje_db

# Actualizar mensaje
@app.put("/mensajes/{mensaje_id}", response_model=Mensaje)
def actualizar_mensaje(mensaje_id: int, mensaje: Mensaje):
    for index, m in enumerate(mensaje_db):
        if m.id == mensaje_id:
            mensaje_db[index] = mensaje  # Reemplazar el mensaje existente
            return mensaje
    raise HTTPException(status_code=404, detail="Mensaje no encontrado")

# Eliminar
@app.delete("/mensajes/{mensaje_id}", response_model=Mensaje)
def eliminar_mensaje(mensaje_id: int):
    for index, m in enumerate(mensaje_db):
        if m.id == mensaje_id:
            deleted_message = mensaje_db.pop(index)  # Eliminar el mensaje
            return {"message": f"Mensaje con ID {mensaje_id} eliminado"}
    raise HTTPException(status_code=404, detail="Mensaje no encontrado")
