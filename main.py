from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import xml.etree.ElementTree as ET
import requests
import os
import asyncio
from timeit import default_timer

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://bryanvalencia.dev" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(name="index.html", context={'request': request})

@app.get("/oplog", response_class=HTMLResponse)
async def oplog(request: Request):
    tree = ET.parse("oplog/oplog.xml")
    entries = tree.findall("entry")
    entries_list = []
    for entry in entries:
        entries_list.append({'id': entry.attrib['id'],'text': entry.attrib['message'], 'date': entry.attrib['date']})

    print(entries_list)
    entries_list.reverse()
    return templates.TemplateResponse(name="oplog.html", context={'request': request, 'data': entries_list})

@app.get("/commits", response_class=HTMLResponse)
async def commits(request: Request):
    token = os.getenv('GITHUB_TOKEN')
    headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {token}',
    'X-GitHub-Api-Version': '2022-11-28',
    }
    query={
        "query": "query {\n  viewer {\n    repositories(first: 50, ownerAffiliations: OWNER) {\n      nodes {\n        name\n        url\n        history: defaultBranchRef {\n          target {\n            ... on Commit {\n              history(first: 10) {\n                nodes {\n                  oid\n                  messageHeadline\n                  committedDate\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}"
        }

    start = default_timer()
    response = requests.post(f'https://api.github.com/graphql', headers=headers, json=query)
    data=response.json()
    print(data['data']['viewer']['repositories']['nodes'])

    # with open("graph.json", "w") as f:
    #     f.write(response.text)

    return templates.TemplateResponse(name="commits.html", context={'request': request, 'data': data['data']['viewer']['repositories']['nodes']})

# def request()