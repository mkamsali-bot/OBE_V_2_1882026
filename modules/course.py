from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.course_service import (
    get_all_courses,
    get_course,
    course_exists,
    add_course,
    update_course,
    delete_course
)

from services.department_service import (
    get_all_departments
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------
# Course Home
# ---------------------------------------------------------
@router.get("/course")
def course(request: Request):

    courses = get_all_courses()

    departments = get_all_departments()

    return templates.TemplateResponse(
        request=request,
        name="course.html",
        context={
            "title": "Course Master",
            "courses": courses,
            "departments": departments,
            "course": None
        }
    )


# ---------------------------------------------------------
# Save Course
# ---------------------------------------------------------
@router.post("/course/save")
def save_course(

    course_code: str = Form(...),
    course_name: str = Form(...),
    regulation: str = Form(...),

    course_type: str = Form(...),

    semester: int = Form(...),
    credits: float = Form(...),
    department_id: int = Form(...),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    if not course_exists(course_code):

        add_course(

            course_code,
            course_name,
            regulation,

            course_type,

            semester,
            credits,
            department_id,

            active

        )

    return RedirectResponse(

        url="/course",

        status_code=303

    )

@router.get("/course/edit/{id}")
def edit_course(request: Request, id: int):

    course = get_course(id)

    courses = get_all_courses()

    departments = get_active_departments()

    return templates.TemplateResponse(

        request=request,

        name="course.html",

        context={

            "title": "Course",

            "course": course,

            "courses": courses,

            "departments": departments

        }

    )

# ---------------------------------------------------------
# Update Course
# ---------------------------------------------------------
@router.post("/course/update/{id}")
def update_course_route(

    id: int,

    course_code: str = Form(...),
    course_name: str = Form(...),
    regulation: str = Form(...),

    course_type: str = Form(...),

    semester: int = Form(...),
    credits: float = Form(...),
    department_id: int = Form(...),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    update_course(

        id,

        course_code,
        course_name,
        regulation,

        course_type,

        semester,
        credits,
        department_id,

        active

    )

    return RedirectResponse(

        url="/course",

        status_code=303

    )

# ---------------------------------------------------------
# Delete Course (Soft Delete)
# ---------------------------------------------------------
@router.get("/course/delete/{id}")
def delete(id: int):

    delete_course(id)

    return RedirectResponse(
        "/course",
        status_code=303
    )