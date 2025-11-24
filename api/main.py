from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
accounts = {}

class Account(BaseModel):
    name: str
    amount: float = 0.0

@app.post("/create")
def create_account(acc: Account):
    if acc.name in accounts:
        return {"success": False, "message": "Account already exists"}
    
    accounts[acc.name] = acc.amount
    return {"success": True, "message": "Account created", "balance": accounts[acc.name]}

@app.post("/deposit")
def deposit(acc: Account):
    # LOGIC FIX: Check if name is NOT in accounts
    if acc.name not in accounts:
        return {"success": False, "message": "Account does not exist"}
    
    accounts[acc.name] += acc.amount
    return {"success": True, "message": "Deposit successful", "balance": accounts[acc.name]}

@app.post("/withdraw")
def withdraw(acc: Account):
    # LOGIC FIX: Check if name is NOT in accounts
    if acc.name not in accounts:
        return {"success": False, "message": "Account does not exist"}
    
    if accounts[acc.name] < acc.amount:
        return {"success": False, "message": "Insufficient balance"}
    
    accounts[acc.name] -= acc.amount
    return {"success": True, "message": "Withdraw successful", "balance": accounts[acc.name]}

@app.get("/balance/{name}")
def get_balance(name: str):
    if name not in accounts:
        return {"success": False, "message": "Account not found"}
    return {"success": True, "message": "Balance fetched", "balance": accounts[name]}