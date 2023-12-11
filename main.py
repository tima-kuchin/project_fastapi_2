from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, FileResponse
from public.users import router

app = FastAPI()
app.include_router(router)

@app.get('/', response_class=PlainTextResponse)
async def f_indexH():
    return "Привет"