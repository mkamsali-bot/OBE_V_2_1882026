import sqlite3
from pathlib import Path

DB_NAME = "obe.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    # Enable foreign key constraint support in SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Department
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Department (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_code TEXT NOT NULL UNIQUE,
            department_name TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)

    # 2. Program Master
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Program (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_code TEXT UNIQUE NOT NULL,
            program_name TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            duration INTEGER DEFAULT 4,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES Department(id) ON DELETE CASCADE
        )
    """)

    # 3. Faculty
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_code TEXT NOT NULL UNIQUE,
            faculty_name TEXT NOT NULL,
            designation TEXT,
            email TEXT,
            mobile TEXT,
            department_id INTEGER,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES Department(id) ON DELETE SET NULL
        )
    """)

    
    # 5. Program Outcome (PO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProgramOutcome (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            po_code TEXT NOT NULL,
            po_description TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES Department(id) ON DELETE CASCADE,
            UNIQUE(department_id, po_code)
        )
    """)

    # 6. Program Specific Outcome (PSO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProgramSpecificOutcome (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pso_code TEXT NOT NULL,
            pso_description TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES Department(id) ON DELETE CASCADE,
            UNIQUE(department_id, pso_code)
        )
    """)

    # 7. Course Outcome (CO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CourseOutcome (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            co_code TEXT NOT NULL,
            co_description TEXT NOT NULL,
            blooms_level TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE,
            UNIQUE(course_id, co_code)
        )
    """)

    # 8. CO - PO / PSO Mapping
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CO_PO_Mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            co_id INTEGER NOT NULL UNIQUE,
            po1 INTEGER DEFAULT 0,
            po2 INTEGER DEFAULT 0,
            po3 INTEGER DEFAULT 0,
            po4 INTEGER DEFAULT 0,
            po5 INTEGER DEFAULT 0,
            po6 INTEGER DEFAULT 0,
            po7 INTEGER DEFAULT 0,
            po8 INTEGER DEFAULT 0,
            po9 INTEGER DEFAULT 0,
            po10 INTEGER DEFAULT 0,
            po11 INTEGER DEFAULT 0,
            po12 INTEGER DEFAULT 0,
            pso1 INTEGER DEFAULT 0,
            pso2 INTEGER DEFAULT 0,
            pso3 INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE,
            FOREIGN KEY (co_id) REFERENCES CourseOutcome(id) ON DELETE CASCADE
        )
    """)

    # 9. CO Weightage Master
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS COWeightage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            co_id INTEGER NOT NULL,
            le_weightage REAL DEFAULT 0,
            se1_weightage REAL DEFAULT 0,
            se2_weightage REAL DEFAULT 0,
            assignment_weightage REAL DEFAULT 0,
            practical_weightage REAL DEFAULT 0,
            viva_weightage REAL DEFAULT 0,
            project_weightage REAL DEFAULT 0,
            total_weightage REAL DEFAULT 100,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE,
            FOREIGN KEY (co_id) REFERENCES CourseOutcome(id) ON DELETE CASCADE,
            UNIQUE(course_id, co_id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database created successfully: {Path(DB_NAME).resolve()}")