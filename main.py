import uvicorn
from fastapi import FastAPI

import config
from routers import user

app = FastAPI(
    title = config.settings.APP_NAME,
    version = config.settings.APP_VERSION,
)

app.include_router(user.router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)