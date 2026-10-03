import hashlib
import hmac
import secrets

from app.database import get_connection


def hash_password(password: str) -> str:

    salt = secrets.token_hex(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        120_000,
    ).hex()

    return f"{salt}${digest}"


def verify_password(
    password: str,
    stored: str
) -> bool:

    try:

        salt, digest = stored.split(
            "$",
            1
        )

        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            120_000,
        ).hex()

        return hmac.compare_digest(
            candidate,
            digest
        )

    except ValueError:

        return False


def create_session(user_id: int) -> str:

    token = secrets.token_urlsafe(32)

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO sessions(token, user_id)
        VALUES (?, ?)
        """,
        (
            token,
            user_id
        ),
    )

    conn.commit()

    conn.close()

    return token


def delete_session(token: str):

    conn = get_connection()

    conn.execute(
        "DELETE FROM sessions WHERE token=?",
        (token,),
    )

    conn.commit()

    conn.close()


def get_user_by_session(
    token: str | None
):

    if not token:
        return None

    conn = get_connection()

    row = conn.execute(
        """
        SELECT
            u.id,
            u.name,
            u.email
        FROM users u
        JOIN sessions s
            ON s.user_id = u.id
        WHERE s.token=?
        """,
        (token,),
    ).fetchone()

    conn.close()

    if row:

        return dict(row)

    return None
