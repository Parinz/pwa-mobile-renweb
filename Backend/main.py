from fastapi import FastAPI, Depends, Response 
from fastapi.middleware.cors import CORSMiddleware
from authenticate import Login

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
    return [{"Server": True}, {"Renweb-Servers": True}, {"Authentication": True}, {"Frontend": False}]

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

@app.get('/auth/{Client_Code}/{Username}/{Password}/grade')
async def get_grade(Client_Code, Username, Password):

