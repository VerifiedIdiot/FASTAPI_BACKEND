from fastapi import FastAPI
import uvicorn
from app.routers.weather import weather_router

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

app.include_router(weather_router.router, prefix="/weather", tags=["weather"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
