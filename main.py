from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
from database.database import engine, Base
from models.models import User
from routes import auth

app = FastAPI(title='My Shop')
app.include_router(auth.app_router)

app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")

HOST = '127.0.0.1'
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print('Starting server')
    uvicorn.run('main:app', port=8000, host=HOST, reload=True)
    print('Server stopped')