# Router para endpoints relacionados con USUARIOS

from fastapi import APIRouter, HTTPException

# Crear el router
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/")
async def crear_usuario(nombre: str, email: str):
    """HU-03: Registra un nuevo usuario"""
    from main import registrar_usuario

    try:
        nuevo_usuario = registrar_usuario(nombre=nombre, email=email)
        return {
            "message": "Usuario registrado correctamente",
            "usuario": {
                "id": nuevo_usuario.id,
                "nombre": nuevo_usuario.nombre,
                "email": nuevo_usuario.email
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def listar_usuarios():
    """HU-03: Obtiene todos los usuarios registrados"""
    from main import consultar_usuarios

    try:
        usuarios = consultar_usuarios()

        usuarios_dict = [
            {
                "id": u.id,
                "nombre": u.nombre,
                "email": u.email
            }
            for u in usuarios
        ]

        return {
            "total": len(usuarios_dict),
            "usuarios": usuarios_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))