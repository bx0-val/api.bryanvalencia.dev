from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import xml.etree.ElementTree as ET

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/oplog", response_class=HTMLResponse)
async def index(request: Request):
    tree = ET.parse("oplog/oplog.xml")
    entries = tree.findall("entry")
    entries_list = []
    for entry in entries:
        entries_list.append({'id': entry.attrib['id'],'text': entry.attrib['message'], 'date': entry.attrib['date']})

    print(entries_list)
    entries_list.reverse()
    return templates.TemplateResponse(name="index.html", context={'request': request, 'data': entries_list})
