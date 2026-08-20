import sqlite3

DB_NAME = "obe.db"


# ==========================================================
# Database Connection
# ==========================================================
def get_connection():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn


# ==========================================================
# Get All CO Weightages
# ==========================================================
def get_all_co_weightages():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            cw.*,

            c.course_code,
            c.course_name,

            co.co_code,
            co.co_description

        FROM COWeightage cw

        INNER JOIN Course c
            ON cw.course_id = c.id

        INNER JOIN CourseOutcome co
            ON cw.co_id = co.id

        ORDER BY

            c.course_code,
            co.co_code

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# Get CO Weightage By ID
# ==========================================================
def get_co_weightage(weightage_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM COWeightage

        WHERE id = ?

    """, (weightage_id,))

    row = cursor.fetchone()

    conn.close()

    return row


# ==========================================================
# Check Duplicate
# ==========================================================
def weightage_exists(course_id, co_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT id

        FROM COWeightage

        WHERE

            course_id = ?

        AND

            co_id = ?

    """, (

        course_id,
        co_id

    ))

    row = cursor.fetchone()

    conn.close()

    return row is not None


# ==========================================================
# Add CO Weightage
# ==========================================================
def add_co_weightage(

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

    is_active

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO COWeightage(

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

            is_active

        )

        VALUES(

            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?

        )

    """, (

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

        is_active

    ))

    conn.commit()

    conn.close()


# ==========================================================
# Update CO Weightage
# ==========================================================
def update_co_weightage(

    weightage_id,

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

    is_active

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE COWeightage

        SET

            course_id = ?,
            co_id = ?,

            le_weightage = ?,
            se1_weightage = ?,
            se2_weightage = ?,

            assignment_weightage = ?,

            practical_weightage = ?,

            viva_weightage = ?,

            project_weightage = ?,

            total_weightage = ?,

            is_active = ?

        WHERE id = ?

    """, (

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

        is_active,

        weightage_id

    ))

    conn.commit()

    conn.close()


# ==========================================================
# Delete CO Weightage
# ==========================================================
def delete_co_weightage(weightage_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        DELETE

        FROM COWeightage

        WHERE id = ?

    """, (weightage_id,))

    conn.commit()

    conn.close()

    # ==========================================================
# Get Active Courses
# ==========================================================
def get_active_courses():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM Course

        WHERE is_active = 1

        ORDER BY course_code

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows