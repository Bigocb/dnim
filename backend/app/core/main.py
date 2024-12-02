#!/usr/bin/env python3
from fastapi import FastAPI, Depends
import uvicorn
from data.db import Database, Page
from core import config

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)


import frontend
from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

# Redirect the root to the gui
@app.get('/')
async def root_redirect():
    response = RedirectResponse(url='/gui')
    return response


@app.get('/api/v1')
async def read_root():
    return {'Hello': 'World'}

app.include_router(pages.router,prefix="/api/v1")

frontend.init(app)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8668)