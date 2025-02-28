from fastapi import FastAPI, HTTPException
from executor import execute_python_code
from schemas import CodeRequest, CodeResponse

app = FastAPI(title="FastAPI Code Executor using Docker")

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Docker Code Executor!"}

@app.post("/execute", response_model=CodeResponse)
async def execute_code(request: CodeRequest):
    return execute_python_code(request.code)
