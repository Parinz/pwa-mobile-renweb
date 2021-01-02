from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse
from authenticate import Login, globalGetData, globalGetGradeBook 

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
@app.get("/", response_class=ORJSONResponse)
async def root():
    return [{"Server": True}, {"Renweb-Servers": True}, {"Authentication": True}, {"Data_Transmission": True}, {"Frontend": False}]

# Authentication Protocol
@app.get("/auth/{Client_Code}/{Username}/{Password}", response_class=ORJSONResponse)
async def logon(Client_Code, Username, Password):
    Status = Login(Client_Code, Username, Password)
    if Status == -1:
        return {"Status": "Wrong Username/Password"}
    elif Status == -2:
        return {"Status": "Network Error or Wrong District Code"}
    else:
        return {"Name": Status}

@app.get('/auth/{Client_Code}/{Username}/{Password}/getData', response_class=ORJSONResponse)
async def get_data(Client_Code, Username, Password):
    
    Grade_List, Urls_list =  globalGetData(Client_Code, Username, Password)
    
    Data_dict = [{"Grades": Grade_List}, {"Urls": Urls_list}]
    return Data_dict 

@app.get('/auth/{Client_Code}/{Username}/{Password}/reportCard/{Subject}', response_class=HTMLResponse)
async def report(Client_Code, Username, Password, Subject: int):
    return globalGetGradeBook(Client_Code, Username, Password, Subject)
