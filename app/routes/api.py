from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)

from app.models.schemas import (
    HomeRequest,
    PartyRequest,
    JewelryRequest,
)

from app.services.auth import (
    get_user_by_session
)

from app.services.gemini import (
    generate
)

from app.services.history import (
    save_history,
)


router = APIRouter(
    prefix="/api"
)


def current_user(
    request: Request
):

    user = get_user_by_session(
        request.cookies.get(
            "pocketsmart_session"
        )
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Please log in first.",
        )

    return user


async def save_result(
    user,
    planner,
    request_obj,
    response
):

    save_history(
        user["id"],
        planner,
        request_obj,
        response.model_dump(),
    )


@router.post(
    "/generate-home"
)
async def generate_home(
    payload: HomeRequest,
    user=Depends(current_user),
):

    result = await generate(
        "home",
        payload
    )

    await save_result(
        user,
        "home",
        payload.model_dump(),
        result,
    )

    return result


@router.post(
    "/generate-party"
)
async def generate_party(
    payload: PartyRequest,
    user=Depends(current_user),
):

    result = await generate(
        "party",
        payload
    )

    await save_result(
        user,
        "party",
        payload.model_dump(),
        result,
    )

    return result


@router.post(
    "/generate-jewelry"
)
async def generate_jewelry(

    budget: float = Form(...),

    occasion: str = Form(
        "wedding"
    ),

    style: str = Form(
        "elegant"
    ),

    outfit_color: str = Form(
        ""
    ),

    notes: str = Form(
        ""
    ),

    outfit_image: UploadFile | None = File(
        None
    ),

    user=Depends(current_user),
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail="Budget must be greater than zero.",
        )

    if outfit_image:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if (
            outfit_image.content_type
            not in allowed_types
        ):

            raise HTTPException(
                status_code=415,
                detail=(
                    "Only JPG, PNG or WEBP "
                    "images are supported."
                ),
            )

    image_bytes = None

    if outfit_image:

        image_bytes = (
            await outfit_image.read()
        )

        if len(image_bytes) > (
            5 * 1024 * 1024
        ):

            raise HTTPException(
                status_code=413,
                detail=(
                    "Image must be "
                    "5 MB or smaller."
                ),
            )

    payload = JewelryRequest(
        budget=budget,
        occasion=occasion,
        style=style,
        outfit_color=outfit_color,
        notes=notes,
    )

    result = await generate(
        "jewelry",
        payload,
        image_bytes,
        (
            outfit_image.content_type
            if outfit_image
            else None
        ),
    )

    await save_result(
        user,
        "jewelry",
        payload.model_dump(),
        result,
    )

    return result


@router.get(
    "/history"
)
def api_history(
    user=Depends(current_user)
):

    from app.services.history import (
        get_history
    )

    return get_history(
        user["id"]
    )


@router.get(
    "/session-info"
)
def session_info(
    user=Depends(current_user)
):

    return {
        "authenticated": True,
        "user": user,
    }