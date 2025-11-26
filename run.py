import uvicorn
from backend.app.config import settings



if __name__=="__main__":
    uvicorn.run("backend.app.main:app",
                host="127.0.0.1",
                reload = settings.debug,
                port=8000
                ) 