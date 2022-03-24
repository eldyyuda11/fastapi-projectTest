from ast import If
from tokenize import Double
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
import uvicorn
import math

app = FastAPI()

students ={
    1:{
        "name":"John",
        "age":20,
        "year" : "12th"
    }
}

class Student(BaseModel):
    name : str
    age : int
    year : str

class UpdateStudent(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    year : Optional[str] = None
    
@app.get("/index")
def index():
    return {
        "data" : [
        {
            "lama_dering": 5,
            "jenis_dering" : "sedang"
        },
        {
            "lama_dering" : 12,
            "jenis_dering": "lama"
        }
        ]
        }


# @app.get("/KBDI")
# def KBDI(KBDItMin:Double,DF:Double,RT):
#     if(RT>=5.1): 
#         if(RT == ):
#             return RT-5.1
#     elif(RT<5.1):
#         RFResult = 0
#         return RFResult     


#     KBDI =  KBDItMin+DF-RF
#     return KBDI


    
    
@app.get("/get-student/{student_id}")
def getStudent(student_id:int = Path(None, description="Student ID", gt=0,lt=3)):
    if student_id not in students:
        return {"error": "Student not found"}
    
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student(*, student_id : int, name : Optional[str] = None, test : int):
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]
    return {"message": "Student not found"}
    
@app.post("/add-student/{student_id}")
def add_student(student_id:int, student: Student):
    if student_id in students:
        return {"message": "Student already exists"}
    
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id:int, student: UpdateStudent):
    if student_id not in students:
        return {"message": "Student not found"}
    
    if student.name != None:
        students[student_id].name = student.name
        
    if student.age != None:
        students[student_id].age = student.age
        
    if student.year != None:
        students[student_id].year = student.year
    
    return students[student_id]
    
@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        return {"message": "Student not found"}
    
    del students[student_id]
    return {"message": "Student deleted"}

@app.get("/get-students-all")
def get_students():
    return students
