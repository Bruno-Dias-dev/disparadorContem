from fastapi import Request, HTTPException

def verificar_usuario_logado(request: Request):
    usuario = request.session.get("usuario")
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return usuario
