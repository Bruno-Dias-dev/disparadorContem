from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

class RedirectUnauthorizedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if response.status_code == 401:
            return RedirectResponse(url="/login")
        return response
