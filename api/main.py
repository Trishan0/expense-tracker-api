from fastapi import FastAPI
from api.routers import expenses


app = FastAPI()

app.include_router(expenses.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Expense Tracker API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)