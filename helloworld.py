# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return "hello flask"




from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    return "hello fastapi"

if __name__=="__main__":
    # app.run(debug=True)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)