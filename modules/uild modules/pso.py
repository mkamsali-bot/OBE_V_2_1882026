from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.pso_service import (
    get_all_psos,
    get_pso,
    pso_exists,
    add_pso,
    update_pso,
    delete_pso,
    load_default_psos
)

from services.department_service import get_all_departments


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# PSO Master
# ==========================================================
@router.get("/pso")
def pso(request: Request):

    psos = get_all_psos()

    departments = get_all_departments()

    return templates.TemplateResponse(
        request=request,
        name="pso.html",
        context={
            "title": "Program Specific Outcomes",
            "psos": psos,
            "departments": departments,
            "pso": None
        }
    )


# ==========================================================
# Save PSO
# ==========================================================
@router.post("/pso/save")
def save_pso(

    pso_code: str = Form(...),
    pso_description: str = Form(...),
    department_id: int = Form(...),
    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    if not pso_exists(pso_code, department_id):

        add_pso(
            pso_code,
            pso_description,
            department_id,
            active
        )

    return RedirectResponse(
        url="/pso",
        status_code=303
    )


# ==========================================================
# Edit PSO
# ==========================================================
@router.get("/pso/edit/{id}")
def edit_pso(id: int, request: Request):

    pso = get_pso(id)

    psos = get_all_psos()

    departments = get_all_departments()

    return templates.TemplateResponse(
        request=request,
        name="pso.html",
        context={
            "title": "Program Specific Outcomes",
            "pso": pso,
            "psos": psos,
            "departments": departments
        }
    )


# ==========================================================
# Update PSO
# ==========================================================
@router.post("/pso/update/{id}")
def update_pso_record(

    id: int,

    pso_code: str = Form(...),
    pso_description: str = Form(...),
    department_id: int = Form(...),
    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    update_pso(

        id,
        pso_code,
        pso_description,
        department_id,
        active

    )

    return RedirectResponse(
        url="/pso",
        status_code=303
    )


# ==========================================================
# Delete PSO (Soft Delete)
# ==========================================================
@router.get("/pso/delete/{id}")
def delete_pso_record(id: int):

    delete_pso(id)

    return RedirectResponse(
        url="/pso",
        status_code=303
    )


# ==========================================================
# Load Default PSOs
# ==========================================================
@router.get("/pso/load-default/{department_id}")
def load_default_pso(department_id: int):

    load_default_psos(department_id)

    return RedirectResponse(
        url="/pso",
        status_code=303
    )