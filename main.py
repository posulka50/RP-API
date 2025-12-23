import uvicorn
from fastapi import FastAPI

import config

app = FastAPI(
    title = config.settings.APP_NAME,
    version = config.settings.APP_VERSION,
)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)