#!/usr/bin/env python3
from fastapi import FastAPI
import uvicorn
from frontend import frontend
from starlette.responses import RedirectResponse

app = FastAPI(
    title="dnim", docs_url="/api/docs", openapi_url="/api"
)


# Redirect the root to the gui
@app.get('/')
async def root_redirect():
    response = RedirectResponse(url='/gui')
    return response


@app.get('/api/v1')
async def read_root():
    return {'Hello': 'World'}

frontend.init(app)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8678)
