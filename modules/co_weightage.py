from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.co_weightage_service import (
    get_all_co_weightages,
    get_co_weightage,
    weightage_exists,
    add_co_weightage,
    update_co_weightage,
    delete_co_weightage
)

from services.course_service import (
    get_active_courses
)

from services.co_service import (
    get_active_cos
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# CO Weightage Home
# ==========================================================
@router.get("/co-weightage")
def co_weightage(request: Request):

    weightages = get_all_co_weightages()

    courses = get_active_courses()

    cos = get_active_cos()

    return templates.TemplateResponse(
        request=request,
        name="co_weightage.html",
        context={
            "title": "CO Weightage",
            "weightage": None,
            "weightages": weightages,
            "courses": courses,
            "cos": cos
        }
    )


# ==========================================================
# Save CO Weightage
# ==========================================================
@router.post("/co-weightage/save")
def save_co_weightage(

    course_id: int = Form(...),
    co_id: int = Form(...),

    le_weightage: float = Form(...),
    se1_weightage: float = Form(...),
    se2_weightage: float = Form(...),

    assignment_weightage: float = Form(...),
    practical_weightage: float = Form(...),
    viva_weightage: float = Form(...),
    project_weightage: float = Form(...),

    total_weightage: float = Form(...),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    if not weightage_exists(course_id, co_id):

        add_co_weightage(

            course_id,
            co_id,

            le_weightage,
            se1_weightage,
            se2_weightage,

            assignment_weightage,
            practical_weightage,
            viva_weightage,
            project_weightage,

            total_weightage,

            active

        )

    return RedirectResponse(
        url="/co-weightage",
        status_code=303
    )
# ==========================================================
# Edit CO Weightage
# ==========================================================
@router.get("/co-weightage/edit/{id}")
def edit_co_weightage(request: Request, id: int):

    weightage = get_co_weightage(id)

    weightages = get_all_co_weightages()

    courses = get_active_courses()

    cos = get_active_cos()

    return templates.TemplateResponse(
        request=request,
        name="co_weightage.html",
        context={
            "title": "CO Weightage",
            "weightage": weightage,
            "weightages": weightages,
            "courses": courses,
            "cos": cos
        }
    )


# ==========================================================
# Update CO Weightage
# ==========================================================
@router.post("/co-weightage/update/{id}")
def update_co_weightage_route(

    id: int,

    course_id: int = Form(...),
    co_id: int = Form(...),

    le_weightage: float = Form(...),
    se1_weightage: float = Form(...),
    se2_weightage: float = Form(...),

    assignment_weightage: float = Form(...),
    practical_weightage: float = Form(...),
    viva_weightage: float = Form(...),
    project_weightage: float = Form(...),

    total_weightage: float = Form(...),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    update_co_weightage(

        id,

        course_id,
        co_id,

        le_weightage,
        se1_weightage,
        se2_weightage,

        assignment_weightage,
        practical_weightage,
        viva_weightage,
        project_weightage,

        total_weightage,

        active

    )

    return RedirectResponse(
        url="/co-weightage",
        status_code=303
    )


# ==========================================================
# Delete CO Weightage
# ==========================================================
@router.get("/co-weightage/delete/{id}")
def delete_co_weightage_route(id: int):

    delete_co_weightage(id)

    return RedirectResponse(
        url="/co-weightage",
        status_code=303
    )
