from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Student(BaseModel):
    student_id: int
    student_name: str
    course: str
    marks: float = Field(ge=0, le=100)

students = []

#create 
@app.post("/students")
def create_student(student: Student):
    for s in students:
        if s.student_id == student.student_id:
            raise HTTPException(status_code=400, detail="Student already exists")

    students.append(student)
    return {"message": "Student added successfully", "student": student}



@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):
    for s in students:
        if s.student_id == student_id:
            return s

    raise HTTPException(status_code=404, detail="Student not found")


#update
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    for i, s in enumerate(students):
        if s.student_id == student_id:
            if student.student_id != student_id:
                raise HTTPException(status_code=400, detail="Student ID cannot be changed")

            students[i] = student
            return {"message": "Student updated successfully", "student": student}

    raise HTTPException(status_code=404, detail="Student not found")

#delete
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i, s in enumerate(students):
        if s.student_id == student_id:
            deleted = students.pop(i)
            return {"message": "Student deleted successfully", "student": deleted}

    raise HTTPException(status_code=404, detail="Student not found")