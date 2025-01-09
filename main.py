from fastapi import FastAPI
from typing import List
from pydantic import BaseModel,Field

app=FastAPI()

#Post Method pydantic model request body
class Student(BaseModel):
    id:int
    name:str=Field(None,title="name of students",max_length=10)
    subjects:List[str]=[]
    
studentDetails=[]
@app.post("/post_students/")
async def student_data(S1:Student):
    studentDetails.append(S1)#store the data in list
    return {"message":f"name'{S1.name}' has been stored."}

@app.get("/get_students/")#get data 
async def student_datas():
     return studentDetails

@app.get("/")
async def index():
    return {"message":"Hello World"}

#dynamic data show
itemdetails=[{"item_id":1,"name":"anjali","age":22},
             {"item_id":2,"name":"jay","age":23}]
@app.get("/item/{item_id}")
async def item(item_id:int):
    for i in itemdetails:
        if i["item_id"]==item_id:
            return i
    return{"error":"Item is not found"}
    

@app.get("/query/")#query key->value
async def query(skip:int=0,limit:int=10):
    return {"skip":skip,"limit":limit}

#Path Parameters with Types
@app.get("/hello/{name}/{age}")
async def hello(name:str,age:int):
    return{"name":name,"age":age}


#custom object to store data
class Item(BaseModel):
    name:str
    desc:str
    price:float
    tax:float

class ItemStorage:
    def _init_(self):
        self.items=[]
    
    def add_items(self,item:Item):
        self.items.append(item)

    def get_all_items(self):
        return self.items
    
storage=ItemStorage()
@app.post("/create_item/")
async def create_item(item:Item):
    storage.add_items(item)
    return{"message":f"Item'{item.name}'has seen stored"}

@app.get("/get_items/")
async def get_items():
    return storage.items


#respones model
class student(BaseModel):
    id:int
    name:str=Field(None,title="name of students",max_length=10)
    marks:List[int]=[]
    per_marks:float

class percent(BaseModel):
    id:int
    name:str=Field(None,title="name of students",max_length=10)
    per_marks:float

@app.post("/marks",response_model=percent)
async def get_data(S1:student):
    S1.per_marks=sum(S1.marks)/2
    return S1

@app.get("/get_marks")
async def get_marks(S1:percent):
    return S1
