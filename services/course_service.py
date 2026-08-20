from database import get_connection


# ---------------------------------------------------------
# Get All Courses
# ---------------------------------------------------------
# ---------------------------------------------------------
# Get All Courses
# ---------------------------------------------------------
def get_all_courses():

    conn = get_connection()

    rows = conn.execute("""

        SELECT

            Course.*,
            Department.department_name

        FROM Course

        INNER JOIN Department
            ON Department.id = Course.department_id

        ORDER BY
            Course.semester,
            Course.course_code

    """).fetchall()

    conn.close()

    return rows

# ---------------------------------------------------------
# Get One Course
# ---------------------------------------------------------
# ---------------------------------------------------------
# Get Course
# ---------------------------------------------------------
def get_course(id):

    conn = get_connection()

    row = conn.execute("""

        SELECT *

        FROM Course

        WHERE id = ?

    """, (id,)).fetchone()

    conn.close()

    return row
# ---------------------------------------------------------
# Check Duplicate Course Code
# ---------------------------------------------------------
def course_exists(course_code):

    conn = get_connection()

    row = conn.execute("""

        SELECT id
        FROM Course
        WHERE course_code=?

    """, (course_code.upper(),)).fetchone()

    conn.close()

    return row


# ---------------------------------------------------------
# Add Course
# ---------------------------------------------------------
from database import get_connection


# ---------------------------------------------------------
# Add Course
# ---------------------------------------------------------
def add_course(

    course_code,
    course_name,
    regulation,
    course_type,
    semester,
    credits,
    department_id,
    is_active

):

    conn = get_connection()

    conn.execute("""

        INSERT INTO Course
        (

            course_code,
            course_name,
            regulation,
            course_type,
            semester,
            credits,
            department_id,
            is_active

        )

        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        course_code,
        course_name,
        regulation,
        course_type,
        semester,
        credits,
        department_id,
        is_active

    ))

    conn.commit()
    conn.close()

# ---------------------------------------------------------
# Update Course
# ---------------------------------------------------------
# ---------------------------------------------------------
# Update Course
# ---------------------------------------------------------
def update_course(

    id,

    course_code,
    course_name,
    regulation,
    course_type,
    semester,
    credits,
    department_id,
    is_active

):

    conn = get_connection()

    conn.execute("""

        UPDATE Course

        SET

            course_code = ?,
            course_name = ?,
            regulation = ?,
            course_type = ?,
            semester = ?,
            credits = ?,
            department_id = ?,
            is_active = ?,
            updated_at = CURRENT_TIMESTAMP

        WHERE id = ?

    """, (

        course_code,
        course_name,
        regulation,
        course_type,
        semester,
        credits,
        department_id,
        is_active,
        id

    ))

    conn.commit()
    conn.close()

# ---------------------------------------------------------
# Soft Delete
# ---------------------------------------------------------
def delete_course(id):

    conn = get_connection()

    conn.execute("""

        UPDATE Course

        SET

            is_active=0,
            updated_on=CURRENT_TIMESTAMP

        WHERE id=?

    """, (id,))

    conn.commit()
    conn.close()
# ---------------------------------------------------------
# Get Active Courses
# ---------------------------------------------------------
def get_active_courses():

    conn = get_connection()

    rows = conn.execute("""

        SELECT *

        FROM Course

        WHERE is_active = 1

        ORDER BY
            semester,
            course_code

    """).fetchall()

    conn.close()

    return rows

# ==========================================================
# Get Active Course Outcomes
# ==========================================================
def get_active_cos():

    conn = get_connection()

    rows = conn.execute("""

        SELECT *

        FROM CourseOutcome

        WHERE is_active = 1

        ORDER BY course_id, co_code

    """).fetchall()

    conn.close()

    return rows