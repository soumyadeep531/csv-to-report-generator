from fastapi import FastAPI
app=FastAPI()
students=[
    {
        "id":1,
        "name":"Rahul",
        "age":20,
        "course":"python"
    },
    {
            "id":2,
            "name":"priya",
            "age":22,
            "course":"FastAPI"
        }
]

@app.get("/")
def home():
    return{
        "message":"Welcome to student management api"
    }

@app.get("/students")
def get_students():
    return {
        "students":students
    }