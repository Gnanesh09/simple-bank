from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

accounts = {}

class Account(BaseModel):
    name:str
    amount: float = 0.0

@app.post("/create")
def create_account(acc:Account):
    if acc.name in accounts:
        return {"message": "account already exsists"}
    
    accounts[acc.name] = acc.amount
    return {"message": "account created", "balance":accounts[acc.name]}


@app.post("/deposit")
def deposit(acc:Account):
    if acc.name in accounts:
        return {"message": "account already exsists"}
    accounts[acc.name]+=acc.amount
    return {"message": "Deposit successful", "balance": accounts[acc.name]}

@app.post("/withdraw")
def withdraw(acc:Account):
    if acc.name in accounts:
        return {"message": "account already exsists"}
    if accounts[acc.name]<acc.amount:
        return{"message":"insufficent balance "}
    
    accounts[acc.name]-=acc.amount
    return {"message": "Withdraw successful", "balance": accounts[acc.name]}



# Check Balance
@app.get("/balance/{name}")
def get_balance(name: str):
    if name not in accounts:
        return {"message": "Account not found"}
    return {"balance": accounts[name]}
