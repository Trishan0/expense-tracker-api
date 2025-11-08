from fastapi import FastAPI
from api.routers import expenses, auth


app = FastAPI()

app.include_router(expenses.router)

#Authentication routes
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Expense Tracker API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)