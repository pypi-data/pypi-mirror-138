from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from baguette_bi.server import api, exc, static, views
from baguette_bi.settings import settings

app = FastAPI(debug=settings.debug)
app.mount("/static", StaticFiles(directory=static.path), name="static")

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    same_site="strict",
    max_age=settings.session_max_age,
)

app.include_router(views.router)
app.include_router(api.router, prefix="/api")


@app.exception_handler(exc.WebException)
def handle_web_exception(request: Request, exc: exc.WebException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        request.session["Redirect-After-Login"] = str(request.url)
        return RedirectResponse(
            request.url_for("get_login"),
            status.HTTP_302_FOUND,
        )
    return RedirectResponse(request.url_for("index"), 308)
