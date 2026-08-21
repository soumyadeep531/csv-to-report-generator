from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    name: str
    age: int
    course: str


students = [
    {
        "id": 1,
        "name": "Rahul",
        "age": 20,
        "course": "Python"
    },
    {
        "id": 2,
        "name": "Priya",
        "age": 22,
        "course": "FastAPI"
    }
]


@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management API"
    }


@app.get("/students")
def get_students():
    return {
        "students": students
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    return {
        "message": "Student not found"
    }


@app.post("/students")
def add_student(student: Student):

    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "age": student.age,
        "course": student.course
    }

    students.append(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }


@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    for student in students:

        if student["id"] == student_id:

            student["name"] = updated_student.name
            student["age"] = updated_student.age
            student["course"] = updated_student.course

            return {
                "message": "Student updated successfully",
                "student": student
            }

    return {
        "message": "Student not found"
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:

        if student["id"] == student_id:

            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    return {
        "message": "Student not found"
    }