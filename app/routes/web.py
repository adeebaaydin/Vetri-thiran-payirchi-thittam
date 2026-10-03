from fastapi import (
    APIRouter,
    Request,
)

from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from app.services.auth import (
    get_user_by_session
)

from app.services.history import (
    get_history
)


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


def context(
    request: Request,
    **extra
):

    user = get_user_by_session(
        request.cookies.get(
            "pocketsmart_session"
        )
    )

    return {
        "request": request,
        "user": user,
        **extra,
    }


@router.get("/")
def home(
    request: Request
):

    return templates.TemplateResponse(
        "index.html",
        context(request),
    )


@router.get("/login")
def login(
    request: Request
):

    return templates.TemplateResponse(
        "login.html",
        context(
            request,
            error=request.query_params.get(
                "error"
            ),
        ),
    )


@router.get("/register")
def register(
    request: Request
):

    return templates.TemplateResponse(
        "register.html",
        context(
            request,
            error=request.query_params.get(
                "error"
            ),
        ),
    )


@router.get("/dashboard")
def dashboard(
    request: Request
):

    user = get_user_by_session(
        request.cookies.get(
            "pocketsmart_session"
        )
    )

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303,
        )

    return templates.TemplateResponse(
        "dashboard.html",
        context(
            request,
            history=get_history(
                user["id"]
            ),
        ),
    )


@router.get(
    "/planner/{planner}"
)
def planner(
    request: Request,
    planner: str,
):

    if planner not in {
        "home",
        "party",
        "jewelry",
    }:

        return RedirectResponse(
            "/",
            status_code=303,
        )

    return templates.TemplateResponse(
        f"{planner}.html",
        context(request),
    )


@router.get("/history")
def history(
    request: Request
):

    user = get_user_by_session(
        request.cookies.get(
            "pocketsmart_session"
        )
    )

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303,
        )

    return templates.TemplateResponse(
        "history.html",
        context(
            request,
            history=get_history(
                user["id"]
            ),
        ),
    )