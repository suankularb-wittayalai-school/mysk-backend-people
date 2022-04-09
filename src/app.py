from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()



@app.get("/")
def healthCheck():
    return {"status": True}

