from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

class RedirectUnauthorizedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        path = request.url.path
        
        # Rotas livres
        if (
            path.startswith("/static/") 
            or path.startswith("/login") 
            or path.startswith("/api")
            or path.startswith("/docs")
            or path.startswith("/cadastrar")
        ):
            return await call_next(request) 
        
        # Se não tiver sessão de usuário
        if not request.session.get("user"):
            return RedirectResponse(url="/login")
        
        print("Sessão atual:", request.session)
        
        # Usuário está logado
        response = await call_next(request)
        if response.status_code == 401:
            return RedirectResponse(url="/login")
        return response
