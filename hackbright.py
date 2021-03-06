"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    if row == None:
        print "Student github is not in database."
    else:
        print "Student: %s %s\nGithub account: %s" % (
            row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """
            INSERT INTO Students VALUES (?,?,?)
            """
    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """
        SELECT title, description, max_grade
        FROM Projects
        WHERE title = ?
        """
    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    if row == None:
        print "Project is not in database."
    else:
        print "Project Title: %s \nDescription: %s \nMax Grade: %d" % (
            row[0], row[1], row[2])

def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """
            SELECT grade 
            FROM Grades
            WHERE student_github = ? AND project_title = ?
            """
    db_cursor.execute(QUERY, (github, title))
    row = db_cursor.fetchone()
    if row == None:
        print "Student github and project title combination is not in database."
    else:
        print "The student with github name %s got %d on the %s project." % (github, row[0], title)



def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    INSERT = """
            INSERT INTO Grades (student_github, project_title, grade) 
            VALUES (?, ?, ?)
        """
    grade = int(grade)
    db_cursor.execute(INSERT, (github, title, grade))
    db_connection.commit()

    print "Successfully added grade %d for github: %s, Project: %s" % (grade, github, title)



def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        if len(tokens) == 0:
            tokens = ['','']
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            if len(args) != 1:
                print "Enter the correct number of arguments"
            else:
                github = args[0]
                get_student_by_github(github)

        elif command == "project_info":
            if len(args) != 1:
                print "Enter the correct number of arguments"
            else:
                title = args[0]
                get_project_by_title(title)

        elif command == "new_student":
            if len(args) != 3:
                print "Enter the correct number of arguments"
            else:
                first_name, last_name, github = args   # unpack!
                make_new_student(first_name, last_name, github)

        elif command == "grade_info":
            if len(args) != 2:
                print "Enter the correct number of arguments"
            else:
                github = args[0]
                title = args[1]
                get_grade_by_github_title(github, title)

        elif command == "add_grade":
            if len(args) != 3:
                print "Enter the correct number of arguments"
            else:
                github, title, grade = args 
                assign_grade(github, title, grade)

        else:
            print """Invalid command. Try one of these commands:
            student <github>
            project_info <project_title>
            new_student <firstname> <lastname> <github>
            grade_info <github> <project_title>
            add_grade <github> <project_title> <grade> 
            """


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
