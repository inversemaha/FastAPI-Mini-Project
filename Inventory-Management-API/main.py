from fastapi import FastAPI

#initilize FastAPI app
app = FastAPI()

#Test a text

@app.get("/")
def greet():
    return "This is test text"