from ast import If
from datetime import date, datetime
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
import schedule
import time
import urllib.request
import requests


DATABASE_URL = "postgresql://odmumcfpcfknmp:25e49faabdb52bb57b119eb3718c0657ea9d71f184ebea87b10d80c6c84985bd@ec2-34-194-158-176.compute-1.amazonaws.com:5432/dfml4uo4pr3mme"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

drought_factorsToday = sqlalchemy.Table(
    "drought_factorsToday",
    metadata,
    sqlalchemy.Column("id_faktor", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("maks_temp", sqlalchemy.Float,nullable=True),
    sqlalchemy.Column("avg_annualrain", sqlalchemy.Float,nullable=True),
    sqlalchemy.Column("water_layer", sqlalchemy.Float,nullable=True),
    sqlalchemy.Column("time", sqlalchemy.DateTime,nullable=True),
    sqlalchemy.Column("tinggi muka air", sqlalchemy.Float,nullable=True),
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

inputs_today = sqlalchemy.Table(
    "inputs_today",
    metadata,
    sqlalchemy.Column("id_inputs_today", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("curah_hujan", sqlalchemy.Float,nullable=True),
)
engine  = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

# model  
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
    time: Optional[datetime] = None

class drought_factorTodayIn(BaseModel):
    maks_temp: Optional[float]= None
    avg_annualrain: Optional[float] = None
    water_layer: Optional[float] = None

class input_today(BaseModel):
    id_inputs_today: int
    curah_hujan: Optional[float]= None

class input_todayIn(BaseModel):
    curah_hujan: Optional[float]= None

app = FastAPI()

# timetoday=""
# TMAField1={}
# TMAField2={}
# TMAField3={}
# TMAField4={}
# TMAField5={}
# TMAField6={}
# TMAField7={}
# TMAField8={}
# TMAField9={}
# SuhuHField1={}
# SuhuHField2={}
# SuhuHField3={}
# SuhuHField4={}
# SuhuHField5={}
# SuhuHField6={}
# SuhuHField7={}
# SuhuHField8={}
# SuhuHField9={}
# def job():
#     global timetoday
#     timetoday = datetime.now()

# schedule.every().day.at("00:01").do(job)

# def jobSuhuTMA():
#     global TMAField1
#     global TMAField2
#     global TMAField3
#     global TMAField4 
#     global TMAField5
#     global TMAField6
#     global TMAField7
#     global TMAField8
#     global TMAField9
#     global SuhuHField1
#     global SuhuHField2
#     global SuhuHField3
#     global SuhuHField4
#     global SuhuHField5
#     global SuhuHField6
#     global SuhuHField7
#     global SuhuHField8
#     global SuhuHField9
#     TMAField2 = requests.get("https://api.thingspeak.com/channels/1522263/fields/2.json?api_key=XUFKUIBLFK2IZMT2&results=2")
#     TMAField2 = TMAField2.json()['feeds'][-1]['field2']

# schedule.every().day.at("23:55").do(jobSuhuTMA)
# while 1:
#     schedule.run_pending()
#     time.sleep(1)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# def KBDI(KBDI_sbmnya:result_yesterday,df:drought_factorToday):

@app.post("/input_todaydata", response_model=input_today)
async def create_input_today(it: input_todayIn):
    query = inputs_today.insert().values(curah_hujan=it.curah_hujan)
    last_record_id = await database.fetch_val(query)
    return {**it.dict(),"id_inputs_today": last_record_id}

@app.get("/getdatacurahhujan", response_model=List[input_today])
async def getCurahhujan():
    query = drought_factorsToday.select()
    return await database.fetch_all(query)

@app.get("/drought_factorsToday/" , response_model=List[drought_factorToday])
async def read_drought_factorsToday():
    query = drought_factorsToday.select()
    return await database.fetch_all(query)

@app.post("/drought_factorsTodayInsert/", response_model=drought_factorToday)
async def create_drought_factorsToday(drought_factor :drought_factorTodayIn):
    timeNow = datetime.now()
    query = drought_factorsToday.insert().values(maks_temp = drought_factor.maks_temp,avg_annualrain=drought_factor.avg_annualrain,water_layer=drought_factor.water_layer,time=timeNow)
    last_record_id = await database.execute(query)
    return {**drought_factor.dict(),"id_faktor": last_record_id}    

@app.get("/KBDI", response_model=List[result_today])
async def read_KBDI():
    query = results_today.select()
    return await database.fetch_all(query)

# class Kbdi(BaseModel):
#     vegetasi : Optional[str] = None
#     suhuMaks : Optional[float] = None
#     curahHujan : Optional[float] = None


# contoh
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

#  Koefisien vegetasi 
R0ElninoARapat = 0.6225
R0ElninoCRapat = 5.34
R0ARapat = 0.4386
R0CRapat = 0.5

R0ElninoASedang = 0.8300
R0ElninoCSedang = 7.13
R0ASedang = 0.5848
R0CSedang = 5.02

R0ElninoANon = 0.8300
R0ElninoCNon = 7.13
R0ANon = 0.5848
R0CNon = 5.02
#end

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


     
    
# @app.get("/get-student/{student_id}")
# async def getStudent(student_id:int = Path(None, description="Student ID", gt=0,lt=3)):
#     if student_id not in students:
#         return {"error": "Student not found"}
    
#     return students[student_id]

# @app.get("/get-by-name/{student_id}")
# async def get_student(*, student_id : int, name : Optional[str] = None):
#     for student_id in students:
#         if students[student_id]['name'] == name:
#             return students[student_id]
#     return {"message": "Student not found"}
    
# @app.post("/add-student/{student_id}")
# async def add_student(student_id:int, student: Student):
#     if student_id in students:
#         return {"message": "Student already exists"}
    
#     students[student_id] = student
#     return students[student_id]

# @app.put("/update-student/{student_id}")
# async def update_student(student_id:int, student: UpdateStudent):
#     if student_id not in students:
#         return {"message": "Student not found"}
    
#     if student.name != None:
#         students[student_id].name = student.name
        
#     if student.age != None:
#         students[student_id].age = student.age
        
#     if student.year != None:
#         students[student_id].year = student.year
    
#     return students[student_id]
    
# @app.delete("/delete-student/{student_id}")
# async def delete_student(student_id:int):
#     if student_id not in students:
#         return {"message": "Student not found"}
    
#     del students[student_id]
#     return {"message": "Student deleted"}

# @app.get("/get-students-all")
# async def get_students():
#     return students
