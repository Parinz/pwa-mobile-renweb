from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse
from authenticate import Login, getSubjectGradeBook, getAllClassesList

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



# Check Server Status
@app.get("/", response_class=ORJSONResponse)
async def root():
    return [{"Server": True}, {"Renweb-Servers": True}, {"Authentication": True}, {"Data_Transmission": True}, {"Frontend": False}]

# Authentication Protocol
@app.get("/auth/{Client_Code}/{Username}/{Password}", response_class=ORJSONResponse)
async def logon(Client_Code, Username, Password):
    Status, Calendar = Login(Client_Code, Username, Password)
    if Status == -1:
        return {"Status": "Wrong Username/Password"}
    elif Status == -2:
        return {"Status": "Network Error or Wrong District Code"}
    else:
        return {"Name": Status, "Calendar": Calendar}


@app.get('/auth/{Client_Code}/{Username}/{Password}/gradebook', response_class=ORJSONResponse)
async def get_data(Client_Code, Username, Password):
    Grade_List = getAllClassesList(Client_Code, Username, Password)
    Data_dict = {"Grades": Grade_List}
    return Data_dict


@app.get('/auth/{Client_Code}/{Username}/{Password}/reportCard/{Student}/{Subject}/{Term}', response_class=HTMLResponse)
async def report(Client_Code, Username, Password, Student: int, Subject: int, Term: int):
    return getSubjectGradeBook(Client_Code, Username, Password, Student, Subject, Term)
