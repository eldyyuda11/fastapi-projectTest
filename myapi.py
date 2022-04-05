from ast import If
from importlib.metadata import metadata
from tokenize import Double
from fastapi import FastAPI, Path
from typing import Optional
from typing import List 
from pydantic import BaseModel
import databases
import uvicorn
import math
import sqlalchemy
from urllib import response
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse



app = FastAPI()

DATABASE_URL = "postgresql://odmumcfpcfknmp:25e49faabdb52bb57b119eb3718c0657ea9d71f184ebea87b10d80c6c84985bd@ec2-34-194-158-176.compute-1.amazonaws.com:5432/dfml4uo4pr3mme"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
engine  = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

drought_factors = sqlalchemy.Table(
    "drought_factorsToday",
    metadata,
    sqlalchemy.Column("id_faktor", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("maks_temp", sqlalchemy.Float,nullable=True),
    sqlalchemy.Column("avg_annualrain", sqlalchemy.Float,nullable=True),
    sqlalchemy.Column("water_layer", sqlalchemy.Float,nullable=True),
    sqlalchemy.Column("time", sqlalchemy.Float,nullable=True),
)
results_yesterday = sqlalchemy.Table(
    "results_yesterday",
    metadata,
    sqlalchemy.Column("id_results_yesterday", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("kbdi_sebelumnya", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("temp_sebelumnnya", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("faktorKekeringan_sebelumnnya", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("curahHujan_sebelumnya", sqlalchemy.Float, nullable=True),
    )

results_today = sqlalchemy.Table(
    "results_today",
    metadata,
    sqlalchemy.Column("id_results_today", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("kbdi_today", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("tempMaks_today", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("faktor_kekeringanToday", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("curahHujan_today", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("faktor_hujanToday", sqlalchemy.Float, nullable=True),
)

class result_today(BaseModel):
    id_results_today: int
    kbdi_today: Optional[float]= None
    tempMaks_today: Optional[float] = None
    faktor_kekeringanToday: Optional[float] = None 
    curahHujan_today: Optional[float] = None
    faktor_hujanToday: Optional[float] = None


class result_yesterday(BaseModel):
    id_results_yesterday: int
    kbdi_sebelumnya: Optional[float]= None
    temp_sebelumnnya: Optional[float] = None
    faktorKekeringan_sebelumnnya: Optional[float] = None 
    curahHujan_sebelumnya: Optional[float] = None

class drought_factorToday(BaseModel):
    id_faktor: int
    maks_temp: Optional[float]= None
    avg_annualrain: Optional[float] = None
    water_layer: Optional[float] = None
    time: Optional[float] = None

class drought_factorTodayIn(BaseModel):
    maks_temp: Optional[float]= None
    avg_annualrain: Optional[float] = None
    water_layer: Optional[float] = None
    time: Optional[float] = None

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/drought_factorsToday/" , response_model=List[drought_factorToday])
async def read_drought_factorsToday():
    query = drought_factors.select()
    return await database.fetch_all(query)


@app.post("/drought_factorsTodayInsert/", response_model=drought_factorToday)
async def create_drought_factorsToday(drought_factorToday:drought_factorTodayIn):
    query = drought_factors.insert().values(maks_temp = drought_factorToday.maks_temp,avg_annualrain=drought_factorToday.avg_annualrain,water_layer=drought_factorToday.water_layer,time=drought_factorToday.time)
    last_record_id = await database.execute(query)
    return {**drought_factorToday.dict(),"id_faktor": last_record_id}


students ={
    1:{
        "name":"John",
        "age":20,
        "year" : "12th"
    }
}
# class Kbdi(BaseModel):
#     vegetasi : Optional[str] = None
#     suhuMaks : Optional[float] = None
#     curahHujan : Optional[float] = None

class Student(BaseModel):
    name : str
    age : int
    year : str

class UpdateStudent(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    year : Optional[str] = None


    
@app.get("/")
async def index():
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
# @app.post("/index/post")
# async def create_Kbdi(Kbdi: Kbdi):
#     return Kbdi


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
async def getStudent(student_id:int = Path(None, description="Student ID", gt=0,lt=3)):
    if student_id not in students:
        return {"error": "Student not found"}
    
    return students[student_id]

@app.get("/get-by-name/{student_id}")
async def get_student(*, student_id : int, name : Optional[str] = None):
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]
    return {"message": "Student not found"}
    
@app.post("/add-student/{student_id}")
async def add_student(student_id:int, student: Student):
    if student_id in students:
        return {"message": "Student already exists"}
    
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
async def update_student(student_id:int, student: UpdateStudent):
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
async def delete_student(student_id:int):
    if student_id not in students:
        return {"message": "Student not found"}
    
    del students[student_id]
    return {"message": "Student deleted"}

@app.get("/get-students-all")
async def get_students():
    return students
