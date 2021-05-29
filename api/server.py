from fastapi import FastAPI
import controllers
import uvicorn

app = FastAPI()

app.include_router(router=controllers.router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)