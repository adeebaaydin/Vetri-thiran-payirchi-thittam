import json

from app.database import get_connection


def save_history(
    user_id: int,
    planner: str,
    request_obj,
    response_obj
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO history(
            user_id,
            planner,
            request_json,
            response_json
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            planner,
            json.dumps(
                request_obj,
                default=str
            ),
            json.dumps(
                response_obj,
                default=str
            ),
        ),
    )

    conn.commit()

    conn.close()


def get_history(
    user_id: int,
    limit: int = 30
):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            id,
            planner,
            request_json,
            response_json,
            created_at
        FROM history
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            user_id,
            limit
        ),
    ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]