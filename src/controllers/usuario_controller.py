from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.usuario import UsuarioCreate, UsuarioLogin
from src.services.usuario_service import UsuarioService
from src.utils.auth import criar_token_jwt, ACCESS_TOKEN_EXPIRE_MINUTES
from src.utils.database import get_db
from datetime import timedelta

router = APIRouter()

@router.post("/cadastrar/", summary="Cadastrar um novo usuário")
async def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        UsuarioService.cadastrar_usuario(db, usuario.nome, usuario.senha)
        return {"mensagem": "Usuário cadastrado com sucesso!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/token/", summary="Obter token de autenticação")
async def login(form_data: UsuarioLogin, db: Session = Depends(get_db)):
    try:
        usuario = UsuarioService.autenticar_usuario(db, form_data.nome, form_data.senha)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = criar_token_jwt(data={"sub": usuario.nome}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))