from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Supabase + FastAPI Student Database (ID-based)")

# Pydantic model for students
class Student(BaseModel):
    name: str
    email: str
    age: int
    course: str


@app.get("/")
def home():
    return {"message": "Welcome to Student Database API"}


# ✅ CREATE multiple students
@app.post("/students/")
def create_students(students: List[Student] = Body(...)):
    try:
        data_to_insert = [s.dict() for s in students]
        response = supabase.table("students").insert(data_to_insert).execute()
        return {"message": f"{len(students)} students added successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ READ all students
@app.get("/students/")
def get_students():
    try:
        response = supabase.table("students").select("*").execute()
        return {"students": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ READ single student by ID
@app.get("/students/id/{id}")
def get_student_by_id(id: int):
    try:
        response = supabase.table("students").select("*").eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
        return {"student": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ UPDATE student details by ID
@app.put("/students/id/{id}")
def update_student(id: int, student: Student):
    try:
        response = supabase.table("students").update({
            "name": student.name,
            "email": student.email,
            "age": student.age,
            "course": student.course
        }).eq("id", id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")

        return {"message": "Student updated successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ DELETE student by ID
@app.delete("/students/id/{id}")
def delete_student(id: int):
    try:
        response = supabase.table("students").delete().eq("id", id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")

        return {"message": f"Student with ID {id} deleted successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
