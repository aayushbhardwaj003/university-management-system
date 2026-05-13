import mysql.connector
from mysql.connector import Error

# ─────────────────────────────────────────────
#  Helper – pretty horizontal rule
# ─────────────────────────────────────────────
def line(ch="─", n=65):
    print(ch * n)

# ─────────────────────────────────────────────
#  1. Show ALL Student Records
# ─────────────────────────────────────────────
def show_students(cursor):
    cursor.execute("SELECT * FROM student ORDER BY ID")
    rows = cursor.fetchall()
    line()
    print(f"{'ID':<10} {'Name':<25} {'Dept':<20} {'Tot_Cred'}")
    line()
    count = 0
    for r in rows:
        print(f"{r[0]:<10} {r[1]:<25} {r[2]:<20} {r[3]}")
        count += 1
    line()
    print(f"Total rows selected: {count}")

# ─────────────────────────────────────────────
#  2. Add Student Record
# ─────────────────────────────────────────────
def add_student(cursor, conn):
    print("\nEnter Student Details:")
    sid      = input("  Student ID   : ").strip()
    name     = input("  Name         : ").strip()
    dept     = input("  Dept_name    : ").strip()
    tot_cred = input("  Tot_cred     : ").strip()
    try:
        cursor.execute(
            "INSERT INTO student VALUES (%s, %s, %s, %s)",
            (sid, name, dept, int(tot_cred))
        )
        conn.commit()
        print(f"\n✔  {cursor.rowcount} row(s) inserted successfully.")
        show_students(cursor)
    except Error as e:
        print(f"✘  Error: {e}")
        conn.rollback()

# ─────────────────────────────────────────────
#  3. Delete Student Record
# ─────────────────────────────────────────────
def delete_student(cursor, conn):
    sid = input("\nEnter Student ID to delete: ").strip()
    try:
        # Check student exists first
        cursor.execute("SELECT name FROM student WHERE ID = %s", (sid,))
        row = cursor.fetchone()
        if not row:
            print("✘  No student found with that ID.")
            return

        print(f"\n  Found student: {row[0]}")

        # Delete from child tables first (foreign key order)
        cursor.execute("DELETE FROM advisor WHERE s_ID = %s", (sid,))
        print(f"  ➜  Removed from advisor : {cursor.rowcount} row(s)")

        cursor.execute("DELETE FROM takes WHERE ID = %s", (sid,))
        print(f"  ➜  Removed from takes   : {cursor.rowcount} row(s)")

        # Now safe to delete from student
        cursor.execute("DELETE FROM student WHERE ID = %s", (sid,))
        print(f"  ➜  Removed from student : {cursor.rowcount} row(s)")

        conn.commit()
        print(f"\n✔  Student {sid} deleted successfully.")
        show_students(cursor)
    except Error as e:
        print(f"✘  Error: {e}")
        conn.rollback()

# ─────────────────────────────────────────────
#  4. Update Student Information
# ─────────────────────────────────────────────
def update_student(cursor, conn):
    sid = input("\nEnter Student ID to update: ").strip()
    print("  4.1 – Update Name")
    print("  4.2 – Update Dept_name")
    print("  4.3 – Update Tot_cred")
    ch1 = input("Enter choice (1/2/3): ").strip()
    try:
        if ch1 == "1":
            new_val = input("Enter new Name: ").strip()
            cursor.execute("UPDATE student SET name = %s WHERE ID = %s", (new_val, sid))
        elif ch1 == "2":
            new_val = input("Enter new Dept_name: ").strip()
            cursor.execute("UPDATE student SET dept_name = %s WHERE ID = %s", (new_val, sid))
        elif ch1 == "3":
            new_val = input("Enter new Tot_cred: ").strip()
            cursor.execute("UPDATE student SET tot_cred = %s WHERE ID = %s", (int(new_val), sid))
        else:
            print("✘  Invalid sub-choice. Please enter 1, 2, or 3.")
            return
        conn.commit()
        if cursor.rowcount:
            print(f"✔  {cursor.rowcount} row(s) updated successfully.")
        else:
            print("✘  No student found with that ID.")
        show_students(cursor)
    except Error as e:
        print(f"✘  Error: {e}")
        conn.rollback()

# ─────────────────────────────────────────────
#  5. Show Instructor Details
# ─────────────────────────────────────────────
def show_instructor(cursor):
    iid = input("\nEnter Instructor ID: ").strip()
    cursor.execute("SELECT * FROM instructor WHERE ID = %s", (iid,))
    rows = cursor.fetchall()
    line()
    print(f"{'ID':<10} {'Name':<25} {'Dept':<20} {'Salary'}")
    line()
    if rows:
        for r in rows:
            print(f"{r[0]:<10} {r[1]:<25} {r[2]:<20} {r[3]:.2f}")
    else:
        print("  No instructor found with that ID.")
    line()

# ─────────────────────────────────────────────
#  6. Show Course Details with Enrolled Students
# ─────────────────────────────────────────────
def show_course_enrolled(cursor):
    cid = input("\nEnter Course ID: ").strip()

    # Course details
    cursor.execute("SELECT * FROM course WHERE course_id = %s", (cid,))
    course = cursor.fetchone()
    line()
    if not course:
        print("  No course found with that ID.")
        line()
        return
    print(f"Course ID   : {course[0]}")
    print(f"Title       : {course[1]}")
    print(f"Dept        : {course[2]}")
    print(f"Credits     : {course[3]}")
    line()

    # Enrolled students via takes
    cursor.execute("""
        SELECT s.ID, s.name, t.semester, t.year
        FROM   student s
        JOIN   takes   t ON s.ID = t.ID
        WHERE  t.course_id = %s
        ORDER BY s.ID
    """, (cid,))
    students = cursor.fetchall()
    print(f"\n  Enrolled Students:")
    print(f"  {'ID':<10} {'Name':<25} {'Semester':<12} {'Year'}")
    line("·")
    if students:
        for r in students:
            print(f"  {r[0]:<10} {r[1]:<25} {r[2]:<12} {r[3]}")
    else:
        print("  No students enrolled in this course.")
    line()

# ─────────────────────────────────────────────
#  7. Show Course Details taken by Instructor
# ─────────────────────────────────────────────
def show_courses_by_instructor(cursor):
    iid = input("\nEnter Instructor ID: ").strip()
    cursor.execute("""
        SELECT i.ID, i.name,
               c.course_id, c.title, c.dept_name, c.credits,
               t.sec_id, t.semester, t.year
        FROM   instructor i
        JOIN   teaches    t ON i.ID = t.ID
        JOIN   course     c ON c.course_id = t.course_id
        WHERE  i.ID = %s
        ORDER BY t.year, t.semester
    """, (iid,))
    rows = cursor.fetchall()
    line()
    if not rows:
        print("  No courses found for that instructor ID.")
        line()
        return
    print(f"Instructor: {rows[0][0]} – {rows[0][1]}")
    line()
    print(f"{'Course ID':<12} {'Title':<30} {'Dept':<20} {'Cred':<6} {'Sec':<6} {'Sem':<10} {'Year'}")
    line("·")
    for r in rows:
        print(f"{r[2]:<12} {r[3]:<30} {r[4]:<20} {r[5]:<6} {r[6]:<6} {r[7]:<10} {r[8]}")
    line()

# ─────────────────────────────────────────────
#  8. Deposit HRA to Salary  (+15%)
# ─────────────────────────────────────────────
def deposit_hra(cursor, conn):
    iid = input("\nEnter Instructor ID: ").strip()
    try:
        cursor.execute("SELECT salary FROM instructor WHERE ID = %s", (iid,))
        row = cursor.fetchone()
        if not row:
            print("✘  No instructor found with that ID.")
            return
        old_salary = float(row[0])
        hra        = old_salary * 0.15
        new_salary = old_salary + hra
        cursor.execute(
            "UPDATE instructor SET salary = %s WHERE ID = %s",
            (new_salary, iid)
        )
        conn.commit()
        print(f"\n  Old Salary : ₹{old_salary:,.2f}")
        print(f"  HRA (15%)  : ₹{hra:,.2f}")
        print(f"  New Salary : ₹{new_salary:,.2f}")
        print(f"\n✔  HRA deposited successfully.")
        # Show updated instructor details
        show_instructor_by_id(cursor, iid)
    except Error as e:
        print(f"✘  Error: {e}")
        conn.rollback()

# ─────────────────────────────────────────────
#  9. Deduct TDS from Salary  (−20%)
# ─────────────────────────────────────────────
def deduct_tds(cursor, conn):
    iid = input("\nEnter Instructor ID: ").strip()
    try:
        cursor.execute("SELECT salary FROM instructor WHERE ID = %s", (iid,))
        row = cursor.fetchone()
        if not row:
            print("✘  No instructor found with that ID.")
            return
        old_salary = float(row[0])
        tds        = old_salary * 0.20
        new_salary = old_salary - tds
        cursor.execute(
            "UPDATE instructor SET salary = %s WHERE ID = %s",
            (new_salary, iid)
        )
        conn.commit()
        print(f"\n  Old Salary : ₹{old_salary:,.2f}")
        print(f"  TDS (20%)  : ₹{tds:,.2f}")
        print(f"  New Salary : ₹{new_salary:,.2f}")
        print(f"\n✔  TDS deducted successfully.")
        show_instructor_by_id(cursor, iid)
    except Error as e:
        print(f"✘  Error: {e}")
        conn.rollback()

# ─────────────────────────────────────────────
#  Internal helper – show instructor by ID
# ─────────────────────────────────────────────
def show_instructor_by_id(cursor, iid):
    cursor.execute("SELECT * FROM instructor WHERE ID = %s", (iid,))
    rows = cursor.fetchall()
    line()
    print(f"{'ID':<10} {'Name':<25} {'Dept':<20} {'Salary'}")
    line()
    for r in rows:
        print(f"{r[0]:<10} {r[1]:<25} {r[2]:<20} {r[3]:,.2f}")
    line()

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    # ── Connection settings ──────────────────
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "university"       # change if your DB name differs
    DB_USER = "root"             # change to your MySQL username
    DB_PASS = "Aayushbh@sql"    # change to your MySQL password

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        if conn.is_connected():
            print("✔  Connected to the database!\n")
    except Error as e:
        print(f"✘  Connection failed: {e}")
        return

    cursor = conn.cursor()

    while True:
        line("═")
        print("       ★  University Management System  ★")
        line("═")
        print(" 1.  Show Student Records")
        print(" 2.  Add Student Record")
        print(" 3.  Delete Student Record")
        print(" 4.  Update Student Information")
        print(" 5.  Show Instructor Details")
        print(" 6.  Show Course Details with Enrolled Students")
        print(" 7.  Show Course Details taken by Instructor")
        print(" 8.  Deposit HRA to Salary")
        print(" 9.  Deduct TDS from Salary")
        print(" 10. Exit the Program")
        line()

        try:
            ch = int(input("Enter your choice (1-10): ").strip())
        except ValueError:
            print("✘  Please enter a valid integer between 1 and 10.")
            continue

        if   ch == 1:  show_students(cursor)
        elif ch == 2:  add_student(cursor, conn)
        elif ch == 3:  delete_student(cursor, conn)
        elif ch == 4:  update_student(cursor, conn)
        elif ch == 5:  show_instructor(cursor)
        elif ch == 6:  show_course_enrolled(cursor)
        elif ch == 7:  show_courses_by_instructor(cursor)
        elif ch == 8:  deposit_hra(cursor, conn)
        elif ch == 9:  deduct_tds(cursor, conn)
        elif ch == 10:
            print("\n  Goodbye! Have a great day. 👋")
            break
        else:
            print("✘  Invalid choice. Please enter a number between 1 and 10.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
