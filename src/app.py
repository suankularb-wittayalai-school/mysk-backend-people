from fastapi import FastAPI, Response

# from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os

from mysk_utils.response import InternalCode

from routes import people, contacts, student

load_dotenv()

app = FastAPI()

app.include_router(people.router, prefix="/people", tags=["people"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
app.include_router(student.router, prefix="/student", tags=["student"])


@app.get("/", status_code=200, response_description="Welcome to MySK API")
def health_check(response: Response):
    response.headers["X-Internal-Code"] = str(InternalCode.IC_GENERIC_SUCCESS.value)
    return {"status": True}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=os.environ.get("HOST"),
        port=int(os.environ.get("PORT")),
        log_level="info",
        reload=True,
    )
