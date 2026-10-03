from fastapi import (
    APIRouter,
    Form,
    Request,
)

from fastapi.responses import RedirectResponse

from app.database import get_connection

from app.services.auth import (
    hash_password,
    verify_password,
    create_session,
    delete_session,
)


router = APIRouter()


@router.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):

    email = email.strip().lower()

    conn = get_connection()

    try:

        cursor = conn.execute(
            """
            INSERT INTO users(
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                name.strip(),
                email,
                hash_password(password),
            ),
        )

        conn.commit()

        user_id = cursor.lastrowid

    except Exception:

        conn.close()

        return RedirectResponse(
            "/register?error=Email+already+registered",
            status_code=303,
        )

    conn.close()

    token = create_session(
        user_id
    )

    response = RedirectResponse(
        "/dashboard",
        status_code=303,
    )

    response.set_cookie(
        "pocketsmart_session",
        token,
        httponly=True,
        samesite="lax",
    )

    return response


@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
):

    email = email.strip().lower()

    conn = get_connection()

    row = conn.execute(
        """
        SELECT
            id,
            password_hash
        FROM users
        WHERE email=?
        """,
        (email,),
    ).fetchone()

    conn.close()

    if (
        not row
        or not verify_password(
            password,
            row["password_hash"]
        )
    ):

        return RedirectResponse(
            "/login?error=Invalid+email+or+password",
            status_code=303,
        )

    token = create_session(
        row["id"]
    )

    response = RedirectResponse(
        "/dashboard",
        status_code=303,
    )

    response.set_cookie(
        "pocketsmart_session",
        token,
        httponly=True,
        samesite="lax",
    )

    return response


@router.get("/logout")
def logout(
    request: Request
):

    token = request.cookies.get(
        "pocketsmart_session"
    )

    if token:

        delete_session(token)

    response = RedirectResponse(
        "/",
        status_code=303,
    )

    response.delete_cookie(
        "pocketsmart_session"
    )

    return response
