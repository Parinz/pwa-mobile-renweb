from fastapi import FastAPI, Depends, Response 
from fastapi.middleware.cors import CORSMiddleware
from authenticate import Login, globalGetData, gradeBook 

# Defining Api Settings
app = FastAPI() 

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


##########################################################################################################

# Check Server Status
@app.get("/")
async def root():
    return [{"Server": True}, {"Renweb-Servers": True}, {"Authentication": True}, {"Data_Transmission": True}, {"Frontend": False}]

# Authentication Protocol
@app.get("/auth/{Client_Code}/{Username}/{Password}")
async def logon(Client_Code, Username, Password):
    Status = Login(Client_Code, Username, Password)
    if Status == -1:
        return {"Status": "Wrong Username/Password"}
    elif Status == -2:
        return {"Status": "Network Error or Wrong District Code"}
    else:
        return {"Status": Status}

@app.get('/auth/{Client_Code}/{Username}/{Password}/getData')
async def get_data(Client_Code, Username, Password):
    
    Grade_List =  globalGetData(Client_Code, Username, Password)
    
    Data_dict = {"Grades": Grade_List}
    return Data_dict 

@app.get('/auth/{Client_Code}/{Username}/{Password}/getData/grade_book')
async def get_grade_book(Client_Code, Username, Password):
    return gradeBook(Client_Code, Username, Password)


